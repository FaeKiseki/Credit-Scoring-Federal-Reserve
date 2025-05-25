# US Credit Card Trends Dashboard (2012–2024)

**Interactive Dashboard built with Streamlit + Plotly**  
Analyzing the evolution of consumer credit card behavior in the United States using data from the Federal Reserve Bank of Philadelphia.

---

## 🔍 Project Objective

This project provides an interactive visual analysis of quarterly aggregated credit card data from 2012 to 2024.  
The dashboard aims to help analysts, banks, or policymakers monitor:

- Credit balances and debt evolution  
- Credit utilization trends (P50, P75, P90)  
- Median credit scores  
- Payment behavior (full vs partial vs minimum payments)  
- Delinquency trends (30+, 60+, 90+ days)

---

## 📊 Data Source

- [Federal Reserve Bank of Philadelphia – Credit Card Data](https://www.philadelphiafed.org/surveys-and-data/large-bank-credit-card-and-mortgage-data)
- Dataset used: **Credit Card Balances – Q4 2024**
- Data is **aggregated** (no personal data) and updated quarterly.

---

## ⚙️ Technologies Used

| Tool         | Purpose                     |
|--------------|-----------------------------|
| Python       | Data preparation            |
| Pandas       | Cleaning & preprocessing    |
| Streamlit    | Web app interface           |
| Plotly       | Interactive data visualizations |
| VS Code + Jupyter | Development & analysis |

---

## 🚀 How to Run the Dashboard

1. Clone this repository  
2. Make sure required packages are installed:

```bash
pip install streamlit pandas plotly
streamlit run app/simulateur.py
