import pandas as pd

# Change this to your actual CSV filename
CSV_FILE = "supplier_performance_data.csv"

df = pd.read_csv(CSV_FILE)

print(f"Loaded {len(df)} rows")
print(f"Columns: {list(df.columns)}")

records = []

for _, row in df.iterrows():
    block = f"""SUPPLIER RECORD
Supplier ID: {row.get('Supplier_ID', 'N/A')}
Supplier Name: {row.get('Supplier_Name', 'N/A')}
Region: {row.get('Region', 'N/A')}
Country: {row.get('Country', 'N/A')}
Product Category: {row.get('Product_Category', 'N/A')}
Product SKU: {row.get('Product_SKU', 'N/A')}
Contract Tier: {row.get('Contract_Tier', 'N/A')}
OTD Rate: {row.get('OTD_Rate_Pct', 'N/A')}%
Defect Rate: {row.get('Defect_Rate_Pct', 'N/A')}%
Compliance Score: {row.get('Compliance_Score', 'N/A')}
Risk Level: {row.get('Risk_Level', 'N/A')}
Active Disruptions: {row.get('Active_Disruptions', 'N/A')}
Certifications: {row.get('Certifications', 'N/A')}
Sustainability Score: {row.get('Sustainability_Score', 'N/A')}
Annual Volume Units: {row.get('Annual_Volume_Units', 'N/A')}
PO Value USD: {row.get('PO_Value_USD', 'N/A')}
Payment Terms Days: {row.get('Payment_Terms_Days', 'N/A')}
Lead Time Days: {row.get('Lead_Time_Days', 'N/A')}
MOQ Units: {row.get('MOQ_Units', 'N/A')}
Last Audit Date: {row.get('Last_Audit_Date', 'N/A')}
Alternate Supplier ID: {row.get('Alt_Supplier_ID', 'N/A')}
PO Quarter: {row.get('PO_Quarter', 'N/A')}
Units Ordered: {row.get('Units_Ordered', 'N/A')}
Units Delivered On Time: {row.get('Units_Delivered_On_Time', 'N/A')}
Units Rejected: {row.get('Units_Rejected', 'N/A')}
PO ID: {row.get('PO_ID', 'N/A')}
Unit Cost USD: {row.get('Unit_Cost_USD', 'N/A')}"""

    records.append(block)

output = "\n\n===END OF RECORD===\n\n".join(records)

with open("supplier_performance_data1.txt", "w", encoding="utf-8") as f:
    f.write(output)

print(f"Done. Created supplier_performance_data1.txt with {len(records)} records")