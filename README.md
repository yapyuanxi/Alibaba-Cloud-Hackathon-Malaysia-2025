# Alibaba-Cloud-Hackathon-Malaysia-2025 (Finalist !) 
# 📊 Revolutionizing MSMEs financial assistance through AI passport

This project analyzes sales data from a Malaysian home-based bakery to assess **microloan repayment ability** and generate actionable financial insights. It calculates risk scores, repayment ratios, and uses a language model (LLM) to provide tailored loan eligibility advice. Data is also uploaded into a MySQL database for BI/dashboard integration.

---

## 🚀 Features

- 📈 Extracts financial metrics from raw sales CSV
- 💰 Calculates monthly repayment ability for requested loan
- ⚖️ Generates risk score and loan eligibility interpretation
- 🧠 Uses LLM (OpenAI-compatible) to provide personalized financial guidance
- 🗃️ Uploads insights to MySQL for dashboard visualization

---
# 📊 Microloan Eligibility Analyzer

This project includes two main Python scripts designed to assess a small business's microloan eligibility using sales data and generate insights with the help of a language model.

---

## 🔧 Code Function Overview

### 1️⃣ `generate_sales_summary.py`

**Function**:  
Processes a 1-month sales invoice CSV to generate structured financial summaries.

**What it does:**
- Loads and cleans the CSV data
- Aggregates:
  - Daily total sales
  - Monthly total sales
  - Average daily sales
  - Top 3 best-selling products
- Outputs a structured dictionary (can be redirected to JSON)

---

### 2️⃣ `microloan_eligibility_analyzer.py`

**Function**:  
Analyzes financial data to determine loan repayment ability and generate loan insights.

**What it does:**
- Calculates:
  - Net profit estimate
  - Monthly repayment amount
  - Repayment ability ratio
  - Risk score (scaled from ratio)
- Interprets risk using a scoring model
- Sends structured data to a language model (LLM)
  - Returns financial health summary
  - Provides tips to improve eligibility
- Saves results to MySQL:
  - Sales summary
  - Repayment analysis
  - Risk interpretation
  - LLM-generated insights

---

## 🧾 Input File

- `Kak_Zaria_s_1-Month_Sales_Invoices.csv` — sales data for analysis

---

## 🖼️ Presentation

- `Hackathon Slides.pptx` — contains project pitch and results summary

---

## ✅ Usage Tip

Run the scripts in order:

```bash
python generate_sales_summary.py
python microloan_eligibility_analyzer.py

