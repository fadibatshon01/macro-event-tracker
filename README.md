# Macro Event Impact Tracker

A fully automated Python analytics engine that measures how financial markets react to major macroeconomic releases. This project ingests economic event data (starting with CPI), aligns it with historical market prices, and quantifies how equity indices respond before and after each announcement. The pipeline computes reaction metrics, generates structured datasets, and produces visual insights used for macro-driven trading research.

This repository showcases:
- event-level financial analysis  
- clean data engineering architecture  
- statistical return computations  
- a modular and reproducible research pipeline  
- polished outputs ready for dashboards, slides, or quant reports  

---

## 🚀 What This System Does

### **1. Loads macroeconomic releases**
The pipeline reads a curated dataset of CPI releases including:
- event timestamp  
- actual inflation print  
- consensus forecast  
- computed inflation surprise (`actual − consensus`)

### **2. Pulls historical market prices**
Using `yfinance`, the engine automatically fetches SPY (or any ticker) market data. It handles:
- multi-index OHLCV structures  
- date alignment around intraday events  
- missing data during market holidays  

### **3. Builds event windows**
For each CPI announcement, the system constructs a ±5-day window of price data and computes:
- **before-event return**  
- **after-event return**  

### **4. Creates a full CPI reaction dataset**
A research-ready table combining:
- event timestamp  
- actual vs. consensus CPI  
- inflation surprise  
- before/after SPY returns  

### **5. Generates visual analytics**
Clean, publication-ready graphics showing how SPY reacts across CPI releases.

---

## 🔄 Inputs → Processing → Outputs  
A fully automated end-to-end pipeline.

**Inputs**  
- CPI dataset (timestamps, actual, consensus)  
- Market data (SPY or any ticker via yfinance)  

**Processing**  
- event alignment  
- window construction  
- return computation  
- surprise calculation  

**Outputs**  
- structured CPI reaction dataset  
- visual analytics for interpretation  

---

## 🛠️ Tech Stack

- Python  
- pandas  
- yfinance  
- matplotlib  
- PyYAML  
- Git & GitHub  

---

## 📈 Example Use Cases

This engine enables you to:

- quantify how markets price inflation surprises  
- measure volatility around macro announcements  
- develop macro-sensitive trading strategies  
- build macro dashboards for PMs and investors  
- extend to new datasets (FOMC, NFP, PCE, GDP, rate decisions)  

This system forms the backbone of a scalable macro analytics suite.

---

## 👤 Author

Built by **Fadi Batshon** — combining data engineering, financial modeling, and market microstructure insights to create automated tools for real-world macro research.

