import pandas as pd
import json

# Load CSV
df = pd.read_csv("Kak_Zaria_s_1-Month_Sales_Invoices.csv")

# Parse date and convert numeric fields
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df['Quantity'] = pd.to_numeric(df['Quantity'])
df['Total'] = pd.to_numeric(df['Total'])

# 1. Daily sales summary per item
daily_sales_by_item = df.groupby(['Date', 'Item']).agg(
    Quantity_Sold=('Quantity', 'sum'),
    Total_Sales=('Total', 'sum')
).reset_index()

# 2. Total sales per day (all items)
total_daily_sales = df.groupby('Date').agg(
    Total_Quantity=('Quantity', 'sum'),
    Total_Sales=('Total', 'sum')
).reset_index()

# 3. Total monthly sales
total_monthly_sales = df['Total'].sum()

# 4. Average daily sales
average_daily_sales = round(total_daily_sales['Total_Sales'].mean(), 2)

# 5. Top 3 selling products by quantity sold
top_3_products = df.groupby('Item').agg(
    Total_Quantity_Sold=('Quantity', 'sum'),
    Total_Sales_Value=('Total', 'sum')
).sort_values(by='Total_Quantity_Sold', ascending=False).head(3).reset_index()

# 6. Build final result dictionary
result = {
    "daily_sales_summary": total_daily_sales.to_dict(orient='records'),
    "total_monthly_sales": round(total_monthly_sales, 2),
    "average_daily_sales": average_daily_sales,
    "top_3_selling_products": top_3_products.to_dict(orient='records')
}

# 7. Print JSON output (pretty formatted)
print(json.dumps(result, indent=2, default=str))
