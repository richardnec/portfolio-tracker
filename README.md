# 📊 Financial Intelligence Tracker

Automatizovaný systém na sledovanie finančných trhov a sentiment analýzu správ.

## 🏗️ Architektúra
`Yahoo Finance / NewsAPI` → `Python` → `GitHub Actions` → `Google BigQuery` → `Power BI`

## 🛠️ Technológie
- **Python** — sťahovanie dát (yfinance, NewsAPI, VADER sentiment)
- **GitHub Actions** — automatické spúšťanie každú noc o 22:00 UTC
- **Google BigQuery** — cloudová databáza
- **SQL** — Moving Averages, RSI, Sentiment Lag Analysis
- **Power BI** — interaktívny dashboard

## 📈 Sledované symboly
AAPL, TSLA, MSFT, BTC-USD, ETH-USD

## 🔍 Kľúčové zistenia
- MSFT RSI stúpa od 40 na 60 — mierne bullish
- MSFT sentiment klesol z +0.1 na -0.1 okolo 8.3
- Cena stabilná okolo 400

## 📊 Dashboard
![Dashboard](dashboard.png)