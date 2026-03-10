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

## 📊 Vysvetlenie metrík

### RSI (Relative Strength Index)
- Meria silu kupujúcich vs predávajúcich (0-100)
- **nad 70** = akcia prekúpená → možný pokles
- **pod 30** = akcia prepredaná → možný rast
- **stúpajúci RSI** = bullish signál (viac ľudí kupuje)
- **klesajúci RSI** = bearish signál (viac ľudí predáva)

### Moving Averages (MA50, MA200)
- Priemerná cena za posledných 50/200 dní
- **MA50 stúpa nad MA200** = golden cross → silný bullish signál
- **MA50 klesá pod MA200** = death cross → bearish signál

### Sentiment
- Analýza titulkov správ pomocou VADER algoritmu (-1 až +1)
- **+1** = extrémne pozitívne správy
- **-1** = extrémne negatívne správy
- Sledujeme či sentiment predpovedá pohyb ceny o 3 dni

## 🔍 Kľúčové zistenia
- Cena MSFT (400) je pod MA50 (450) aj MA200 (470) — bearish signál
- RSI pre MSFT stúpal z 40 na 60 za posledných 10 dní — mierne bullish momentum
- Sentiment MSFT klesol z +0.13 na -0.10 medzi 4.3 a 8.3 — zhoršujúci sa sentiment napriek rastúcemu RSI

## 📊 Dashboard
![Dashboard](dashboard.png)