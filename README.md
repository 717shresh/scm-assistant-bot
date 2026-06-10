# SCM Assistant — TRINAMIX INC Hiring Task TX-JrAI-003

## Public Chatbot URL
https://cloud.flowiseai.com/chatbot/ce199c1b-c69e-4c08-bb47-28c3668db316

## Tech Stack
- Platform: Flowise Cloud
- LLM: ChatGroq llama3-70b-8192
- Embeddings: HuggingFace sentence-transformers/all-MiniLM-L6-v2
- Vector Store: Supabase (pgvector, 384 dimensions)

## Data Files
- supplier_performance_data1.txt — 2000 POs, 116 suppliers, 27 columns converted in to text format
- SupplyChain_Governance_Policy_v3.2.pdf — 10-section governance policy
- computed_answers.txt — pre-computed analytical summary

## Chunk Configurations Tested

### Config 1 — Chunk Size 1000, Overlap 100
- Chunks upserted: 3175
- Observation: Complete supplier records per chunk. Policy sections
  stay intact. No timeout. Best retrieval accuracy. CHOSEN as final.

### Config 2 — Chunk Size 1500, Overlap 100
- Chunks upserted: 3111
- Observation: More chunks but some records split across boundaries.
  Chunk size 500/50 caused 504 gateway timeout on HuggingFace free
  tier due to large dataset size. Reduced to 800/80 to complete.

### Final Choice: Config 1 (1500/100)
Reason: Supplier records remain whole, policy sections intact,
no processing timeout, higher retrieval accuracy on all 5 questions.

## Q&A Results

**Q1: Which Tier-3 suppliers have an active disruption flag,
and what response level applies per policy?**

Tier‑3 suppliers with an active disruption flag – Response level per policy

Supplier name	Active disruption (example)	Policy response level
Archipelago PCB Corp	Labour strike risk	Level 3 – Activate (Policy §9)
Bogota Pack Ltda	Tariff adjustment pending	Level 3 – Activate
Bohai Electronics	Typhoon season disruption	Level 3 – Activate
Buenos Aires Pack	Audit overdue; compliance review	Level 3 – Activate
Cerromax Mineria	Port closure risk	Level 3 – Activate
DaNang Metal Works	Typhoon season disruption	Level 3 – Activate
Deccan Polymer Mfg	Currency volatility flag	Level 3 – Activate
Deltaforge Vietnam	Labour strike risk	Level 3 – Activate
Dravex Components India	Typhoon season disruption	Level 3 – Activate
Helios Pack Greece	Labour strike risk	Level 3 – Activate
Lima Polymer SA	Audit overdue; compliance review	Level 3 – Activate
Longhua Polymer Works	Labour strike risk	Level 3 – Activate
Maghreb Castworks	Regulatory enforcement pending	Level 3 – Activate
MeKong Pack Co	Typhoon season disruption	Level 3 – Activate
Orinoco Pack SAPI	Audit overdue; compliance review	Level 3 – Activate
Patagonia Alloys SRL	Labour strike risk	Level 3 – Activate
Plataforma Metales SA	Export license risk	Level 3 – Activate
Quetzal Textiles	Audit overdue; compliance review	Level 3 – Activate
Sahyadri Alloy Tech	Export license risk	Level 3 – Activate
Sibertek Molding	Port closure risk	Level 3 – Activate
Varna Electronics EAD	Political instability flag	Level 3 – Activate
Visayas Textile Co	Regulatory enforcement pending	Level 3 – Activate
Vistula Pack Sp	Regulatory enforcement pending	Level 3 – Activate
Yucatan Polymer Mfg	Port closure risk	Level 3 – Activate
Explanation

All of the above suppliers are listed as Tier‑3 in the source documents and each has an Active Disruption entry (i.e., a non‑None value).
According to Policy Section 9 (Disruption Response Procedures), a High‑Risk supplier (which includes all Tier‑3 suppliers) with any active disruption flag triggers a Level 3 – Activate response: immediate escalation to the CPO, alternate supplier activation for ≥ 40 % of volume within 10 business days, safety stock increased by + 50 %, and a full root‑cause analysis within 15 business days.
Thus, every Tier‑3 supplier listed above requires a Level 3 Activate response
---

**Q2: Which suppliers qualify for the annual Volume Rebate
Program and how many are there?**

Suppliers qualifying for the Annual Volume Rebate Program

Supplier name	Supplier ID	Annual Volume Units
IndoTech Fab Ltd	SUP‑013	1,846,780
Total number of qualifying suppliers: 1

---

**Q3: Which region has the highest total PO value, and does
it breach the concentration limit?**

Region with the highest total PO value: APAC
Total PO value (APAC): $2,302,132.79
Total spend across all suppliers: $3,191,500.26
APAC share of total spend: ≈ 72.2 %
Concentration‑limit assessment (Policy §6):
The concentration limit is 30 % of total spend.
Since APAC’s share (≈ 72 %) exceeds 30 %, the concentration limit is breached.

---

**Q4: Which suppliers are on Supplier Watch List (SWL) status
and what does it restrict?**

I could not find that information.

---

**Q5: Which product category has the highest average defect
rate and does it exceed the Tier-2 limit?**

Product category with the highest average defect rate
Metal Components – 0.15 %
Does it exceed the Tier‑2 limit?
I could not find that information.

---

## What I Would Improve
1. Replace HuggingFace free embeddings with OpenAI
   text-embedding-3-small for higher semantic accuracy.
2. Add metadata filtering on Supabase for structured queries
   by tier, region, risk level without semantic search.
3. Pre-compute all aggregations at ingestion time using a
   data pipeline instead of a static summary document.
4. Use gpt-4o instead of openai/gpt-oss-20b for complex multi-step
   reasoning across large supplier datasets.
5. Add Cohere Rerank after retrieval to improve precision
   on multi-supplier list questions.
