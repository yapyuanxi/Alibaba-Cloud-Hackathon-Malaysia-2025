import os
import json
import re
import pandas as pd
from sqlalchemy import create_engine
from openai import OpenAI

mysql_host = os.getenv("MYSQL_HOST")
mysql_port = int(os.getenv("MYSQL_PORT", 3306))
mysql_db = os.getenv("MYSQL_DB")
mysql_user = os.getenv("MYSQL_USER")
mysql_pass = os.getenv("MYSQL_PASS")

engine = create_engine(f"mysql+pymysql://{mysql_user}:{mysql_pass}@{mysql_host}:{mysql_port}/{mysql_db}")

# === Load sales data ===
sales_data = {
    "daily_sales_summary": [
        {"Date": "2025-04-17", "Total_Quantity": 5, "Total_Sales": 49.0},
        {"Date": "2025-04-18", "Total_Quantity": 4, "Total_Sales": 14.0},
        {"Date": "2025-04-19", "Total_Quantity": 2, "Total_Sales": 24.0},
        {"Date": "2025-04-20", "Total_Quantity": 1, "Total_Sales": 5.0},
        {"Date": "2025-04-21", "Total_Quantity": 2, "Total_Sales": 24.0},
        {"Date": "2025-04-22", "Total_Quantity": 3, "Total_Sales": 25.0},
        {"Date": "2025-04-23", "Total_Quantity": 5, "Total_Sales": 48.0},
        {"Date": "2025-04-24", "Total_Quantity": 5, "Total_Sales": 44.0},
        {"Date": "2025-04-25", "Total_Quantity": 6, "Total_Sales": 38.0},
        {"Date": "2025-04-26", "Total_Quantity": 4, "Total_Sales": 44.0},
        {"Date": "2025-04-27", "Total_Quantity": 3, "Total_Sales": 24.0},
        {"Date": "2025-04-28", "Total_Quantity": 6, "Total_Sales": 34.0},
        {"Date": "2025-04-29", "Total_Quantity": 5, "Total_Sales": 19.0},
        {"Date": "2025-04-30", "Total_Quantity": 3, "Total_Sales": 24.0},
        {"Date": "2025-05-01", "Total_Quantity": 3, "Total_Sales": 29.0},
        {"Date": "2025-05-02", "Total_Quantity": 8, "Total_Sales": 58.0},
        {"Date": "2025-05-03", "Total_Quantity": 7, "Total_Sales": 68.0},
        {"Date": "2025-05-04", "Total_Quantity": 1, "Total_Sales": 5.0},
        {"Date": "2025-05-05", "Total_Quantity": 6, "Total_Sales": 49.0},
        {"Date": "2025-05-06", "Total_Quantity": 6, "Total_Sales": 34.0},
        {"Date": "2025-05-07", "Total_Quantity": 6, "Total_Sales": 49.0},
        {"Date": "2025-05-08", "Total_Quantity": 6, "Total_Sales": 49.0},
        {"Date": "2025-05-09", "Total_Quantity": 4, "Total_Sales": 44.0},
        {"Date": "2025-05-10", "Total_Quantity": 4, "Total_Sales": 29.0},
        {"Date": "2025-05-11", "Total_Quantity": 1, "Total_Sales": 5.0},
        {"Date": "2025-05-12", "Total_Quantity": 8, "Total_Sales": 58.0},
        {"Date": "2025-05-13", "Total_Quantity": 2, "Total_Sales": 24.0},
        {"Date": "2025-05-14", "Total_Quantity": 9, "Total_Sales": 58.0},
        {"Date": "2025-05-15", "Total_Quantity": 8, "Total_Sales": 43.0},
        {"Date": "2025-05-16", "Total_Quantity": 7, "Total_Sales": 43.0}
    ],
    "total_monthly_sales": 1061.0,
    "average_daily_sales": 35.37,
    "top_3_selling_products": [
        {"Item": "Banana Cake Slice", "Total_Quantity_Sold": 40, "Total_Sales_Value": 140.0},
        {"Item": "Kek Batik Mini Tray", "Total_Quantity_Sold": 33, "Total_Sales_Value": 264.0},
        {"Item": "Roti Jala with Curry (set)", "Total_Quantity_Sold": 28, "Total_Sales_Value": 280.0}
    ]
}

# === Repayment calculation ===
def calculate_repayment_ability(total_monthly_sales, profit_margin=0.20, loan_amount=1000, annual_interest_rate=0.08, loan_term_months=12):
    net_profit = total_monthly_sales * profit_margin
    total_repayment = loan_amount + (loan_amount * annual_interest_rate)
    monthly_repayment = total_repayment / loan_term_months
    ratio = net_profit / monthly_repayment
    return {
        "Net_Profit": round(net_profit, 2),
        "Monthly_Repayment": round(monthly_repayment, 2),
        "Repayment_Ability_Ratio": round(ratio, 2)
    }

# === Risk score ===
def scale_risk_score(rar):
    if rar <= 0:
        return 0
    elif rar >= 2.0:
        return 100
    else:
        return int(rar * 50)

def interpret_score(score):
    if score < 40:
        return "High risk – unlikely to repay without financial improvement."
    elif score < 60:
        return "Moderate risk – borderline eligibility."
    elif score < 80:
        return "Low risk – likely to qualify for small loan."
    else:
        return "Very low risk – excellent financial health."

# === Input values ===
loan_amount_requested = 2300
repayment_result = calculate_repayment_ability(sales_data["total_monthly_sales"], loan_amount=loan_amount_requested)
repayment_ratio = repayment_result["Repayment_Ability_Ratio"]
risk_score = scale_risk_score(repayment_ratio)
risk_interpretation = interpret_score(risk_score)

llm_input = {
    **sales_data,
    "loan_amount_requested": loan_amount_requested,
    "repayment_analysis": repayment_result,
    "risk_score": risk_score,
    "risk_score_interpretation": risk_interpretation
}

# === Call LLM ===
try:
    client = OpenAI(
        api_key="API_KEY",
        base_url="https://dashscope-intl.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {"role": "system", "content": "You are a financial assistant analyzing repayment ability for microloans in Malaysia."},
            {"role": "user", "content": f"""
Below is financial data from a Malaysian home bakery.

{json.dumps(llm_input, indent=2)}

Please evaluate the financial health, explain what the repayment ability ratio and risk score imply, and provide suggestions to improve their loan eligibility, please make it concise.

Format your answer as a bullet-point list, with clear section titles:
- Summary of Financial Health
- Risk Score Interpretation
- Recommendations to Improve Eligibility
"""}
        ],
        max_tokens=512
    )

    llm_response = completion.choices[0].message.content

    print(f"\n💰 Loan Amount Requested: RM {loan_amount_requested}")
    print(f"📉 Monthly Repayment: RM {repayment_result['Monthly_Repayment']}")
    print(f"📊 Repayment Ability Ratio: {repayment_result['Repayment_Ability_Ratio']}")
    print(f"🛡️ Risk Score: {risk_score} ({risk_interpretation})")

    print("\n🧠 Raw LLM Response:\n")
    print(llm_response)

    def extract_section(text, section_title):
        # Normalize and match section header with optional bolding and whitespace
        pattern = rf"-\s*\*+{re.escape(section_title)}\*+\s*\n((?:\s*-\s+.+\n?)*)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            lines = match.group(1).strip().split("\n")
            return [re.sub(r"^\s*-\s*", "", line).strip() for line in lines if line.strip()]
        return []


    summary_points = extract_section(llm_response, "Summary of Financial Health")
    risk_points = extract_section(llm_response, "Risk Score Interpretation")
    recommendations = extract_section(llm_response, "Recommendations to Improve Eligibility")

    df_summary = pd.DataFrame({"Summary of Financial Health": summary_points})
    df_risk = pd.DataFrame({"Risk Score Interpretation": risk_points})
    df_recommend = pd.DataFrame({"Recommendations to Improve Eligibility": recommendations})

    df_sales = pd.DataFrame(sales_data["daily_sales_summary"])
    df_top_products = pd.DataFrame(sales_data["top_3_selling_products"])
    df_repayment = pd.DataFrame([{
        **repayment_result,
        "Loan_Amount_Requested": loan_amount_requested
    }])
    df_risk_eval = pd.DataFrame([{
        "Loan_Amount_Requested": loan_amount_requested,
        "Monthly_Repayment": repayment_result["Monthly_Repayment"],
        "Repayment_Ability_Ratio": repayment_result["Repayment_Ability_Ratio"],
        "Risk_Score": risk_score,
        "Interpretation": risk_interpretation
    }])
    df_llm = pd.DataFrame([{"LLM_Insight": llm_response}])

    # === Upload all to MySQL ===
    df_sales.to_sql("daily_sales_summary", con=engine, if_exists="replace", index=False)
    df_top_products.to_sql("top_3_selling_products", con=engine, if_exists="replace", index=False)
    df_repayment.to_sql("repayment_analysis", con=engine, if_exists="replace", index=False)
    df_risk_eval.to_sql("risk_evaluation", con=engine, if_exists="replace", index=False)
    df_llm.to_sql("llm_insight", con=engine, if_exists="replace", index=False)
    df_summary.to_sql("summary_of_financial_health", con=engine, if_exists="replace", index=False)
    df_risk.to_sql("risk_score_interpretation", con=engine, if_exists="replace", index=False)
    df_recommend.to_sql("recommendations_to_improve_eligibility", con=engine, if_exists="replace", index=False)

    print("\n✅ Data uploaded to MySQL:")
    print("- daily_sales_summary")
    print("- top_3_selling_products")
    print("- repayment_analysis")
    print("- risk_evaluation")
    print("- llm_insight")
    print("- summary_of_financial_health")
    print("- risk_score_interpretation")
    print("- recommendations_to_improve_eligibility")

except Exception as e:
    print(f"❌ Error: {e}")
