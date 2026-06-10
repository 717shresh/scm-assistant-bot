import pandas as pd

df = pd.read_csv("supplier_performance_data.csv")

# Clean disruptions
df['Active_Disruptions'] = df['Active_Disruptions'].fillna('None').astype(str)
df['Active_Disruptions'] = df['Active_Disruptions'].replace('nan', 'None')

lines = []

# ── Q1 ──────────────────────────────────────────────
q1 = df[
    (df['Contract_Tier'] == 'Tier-3') &
    (df['Risk_Level'] == 'High') &
    (df['Active_Disruptions'] != 'None')
][['Supplier_Name', 'Active_Disruptions']].drop_duplicates(
    subset='Supplier_Name'
).sort_values('Supplier_Name')

lines.append("Q1: TIER-3 SUPPLIERS WITH ACTIVE DISRUPTION FLAG AND POLICY RESPONSE LEVEL")
lines.append(f"Total: {len(q1)} Tier-3 High Risk suppliers with active disruption flags.")
lines.append("Supplier list:")
for _, row in q1.iterrows():
    lines.append(f"- {row['Supplier_Name']} | Disruption: {row['Active_Disruptions']}")
lines.append("")
lines.append("Per Policy Section 9 all High Risk suppliers with any active disruption")
lines.append("flag require Level 3 Activate response which means:")
lines.append("- Immediate escalation to CPO")
lines.append("- Alternate supplier activated at minimum 40 percent of volume within 10 business days")
lines.append("- Safety stock adjusted upward by 50 percent")
lines.append("- Full Root Cause Analysis required within 15 business days")
lines.append("")

# ── Q2 ──────────────────────────────────────────────
q2 = df[
    (df['Contract_Tier'] == 'Tier-1') &
    (df['OTD_Rate_Pct'] >= 93) &
    (df['Defect_Rate_Pct'] < 0.5) &
    (df['Sustainability_Score'] >= 85)
][['Supplier_Name']].drop_duplicates().sort_values('Supplier_Name')

lines.append("Q2: VOLUME REBATE QUALIFIED SUPPLIERS")
lines.append("Per Policy Section 4.2 qualifying criteria:")
lines.append("Contract Tier must be Tier-1 AND OTD Rate 93 percent or above")
lines.append("AND Defect Rate below 0.5 percent AND Sustainability Score 85 or above.")
lines.append(f"Total qualifying suppliers: {len(q2)}")
lines.append("Supplier list:")
for name in q2['Supplier_Name']:
    lines.append(f"- {name}")
lines.append("")

# ── Q3 ──────────────────────────────────────────────
# Drop nan regions
df_clean = df.dropna(subset=['Region'])
regional = df_clean.groupby('Region')['PO_Value_USD'].sum().sort_values(ascending=False)
total = df['PO_Value_USD'].sum()
top_region = regional.index[0]
top_value = regional.iloc[0]
top_pct = (top_value / total) * 100

lines.append("Q3: REGIONAL PO VALUE CONCENTRATION")
lines.append(f"Total network PO value: ${total:,.2f}")
lines.append("Breakdown by region:")
for region, value in regional.items():
    pct = (value / total) * 100
    status = "BREACHES the 45 percent cap" if pct > 45 else "within the 45 percent limit"
    lines.append(f"- {region}: ${value:,.2f} ({pct:.1f}%) — {status}")
lines.append("")
lines.append(f"Highest region: {top_region} at ${top_value:,.2f} ({top_pct:.1f}% of total spend).")
if top_pct > 45:
    lines.append(f"{top_region} BREACHES the 45 percent regional concentration cap")
    lines.append("per Policy Section 5.3.")
    lines.append("A Diversification Plan must be submitted within 60 days.")
else:
    lines.append(f"{top_region} at {top_pct:.1f}% is within the 45 percent concentration limit.")
    lines.append("Per Policy Section 5.3 no breach — no Diversification Plan required.")
lines.append("")

# ── Q4 ──────────────────────────────────────────────
q4 = df[
    df['Compliance_Score'] < 60
][['Supplier_Name', 'Compliance_Score']].drop_duplicates(
    subset='Supplier_Name'
).sort_values('Supplier_Name')

lines.append("Q4: SUPPLIER WATCH LIST STATUS")
lines.append("Criteria: Compliance Score below 60.")
lines.append("Per Policy Section 3.4 SWL status restricts new PO issuance")
lines.append("to 20 percent of prior quarter volume.")
lines.append(f"Total unique SWL suppliers: {len(q4)}")
lines.append("Supplier list:")
for _, row in q4.iterrows():
    lines.append(f"- {row['Supplier_Name']} (Compliance Score: {int(row['Compliance_Score'])})")
lines.append("")

# ── Q5 ──────────────────────────────────────────────
cat_stats = df.groupby('Product_Category').agg(
    avg_defect=('Defect_Rate_Pct', 'mean'),
    po_count=('PO_ID', 'count')
).sort_values('avg_defect', ascending=False)

top_cat = cat_stats.index[0]
top_rate = cat_stats.iloc[0]['avg_defect']
top_count = int(cat_stats.iloc[0]['po_count'])

lines.append("Q5: PRODUCT CATEGORY DEFECT RATES")
lines.append("Average defect rate by product category:")
for cat, row in cat_stats.iterrows():
    status = "EXCEEDS Tier-2 limit" if row['avg_defect'] > 2.5 else "within Tier-2 limit"
    lines.append(
        f"- {cat}: {row['avg_defect']:.2f}% average across {int(row['po_count'])} POs — {status}"
    )
lines.append("")
lines.append(f"Highest defect category: {top_cat}")
lines.append(f"Average defect rate: {top_rate:.2f}% across {top_count} POs.")
lines.append("Per Policy Section 3.2 the Tier-2 maximum defect ceiling is 2.50 percent.")
if top_rate > 2.5:
    lines.append(f"{top_cat} at {top_rate:.2f}% BREACHES the Tier-2 limit.")
else:
    lines.append(
        f"{top_cat} at {top_rate:.2f}% is below the Tier-2 ceiling of 2.50 percent — no breach.")
    lines.append("However it is approaching the limit and requires monitoring.")

# ── WRITE ────────────────────────────────────────────
text = "\n".join(lines)

with open("computed_answers.txt", "w", encoding="utf-8") as f:
    f.write(text)

print(text)
print()
print("✅ Created computed_answers.txt — upload this to Flowise Document Store")