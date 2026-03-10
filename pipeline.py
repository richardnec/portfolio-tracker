import yfinance as yf
import pandas as pd
from google.cloud import bigquery
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from newsapi import NewsApiClient
import os
from datetime import datetime, timedelta

# Nastavenie kľúča
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_key.json"

# Nastavenia
PROJECT_ID = "portfolio-tracjer"
DATASET = "market_data"
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY")

# Symboly a ich názvy pre vyhľadávanie správ
SYMBOLS = ["AAPL", "TSLA", "MSFT", "BTC-USD", "ETH-USD"]
SEARCH_TERMS = {
    "AAPL": "Apple stock",
    "TSLA": "Tesla stock",
    "MSFT": "Microsoft stock",
    "BTC-USD": "Bitcoin",
    "ETH-USD": "Ethereum"
}

def download_prices():
    print("📈 Sťahujem ceny...")
    all_data = []
    for symbol in SYMBOLS:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1d")
        df["symbol"] = symbol
        df = df.reset_index()
        df = df[["Date", "symbol", "Open", "High", "Low", "Close", "Volume"]]
        df.columns = ["date", "symbol", "open", "high", "low", "close", "volume"]
        df["date"] = df["date"].dt.date
        all_data.append(df)
    return pd.concat(all_data, ignore_index=True)

def download_sentiment():
    print("📰 Sťahujem sentiment správ...")
    newsapi = NewsApiClient(api_key=NEWSAPI_KEY)
    analyzer = SentimentIntensityAnalyzer()
    
    results = []
    today = datetime.now().date()
    week_ago = today - timedelta(days=7)
    
    for symbol, term in SEARCH_TERMS.items():
        articles = newsapi.get_everything(
            q=term,
            from_param=week_ago.isoformat(),
            to=today.isoformat(),
            language="en",
            sort_by="publishedAt"
        )
        
        for article in articles["articles"]:
            title = article["title"] or ""
            score = analyzer.polarity_scores(title)["compound"]
            pub_date = article["publishedAt"][:10]  # len dátum
            
            results.append({
                "date": pub_date,
                "symbol": symbol,
                "headline": title,
                "sentiment_score": score
            })
    
    df = pd.DataFrame(results)
    
    # Priemer sentimentu za deň a symbol
    df_avg = df.groupby(["date", "symbol"])["sentiment_score"].mean().reset_index()
    df_avg.columns = ["date", "symbol", "avg_sentiment"]
    
    return df_avg

def upload_to_bigquery(df, table_name):
    print(f"☁️  Nahrávam {table_name} do BigQuery...")
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{DATASET}.{table_name}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    print(f"✅ Hotovo! Nahraných {len(df)} riadkov do {table_id}")

if __name__ == "__main__":
    # Ceny
    df_prices = download_prices()
    upload_to_bigquery(df_prices, "raw_prices")
    
    # Sentiment
    df_sentiment = download_sentiment()
    print(df_sentiment.head())
    upload_to_bigquery(df_sentiment, "raw_sentiment")
    
    print("\n🎉 Pipeline hotový!")