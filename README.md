# 🏦 Banking Performance KPI Dashboard (Power BI)

An executive-level **Power BI** report tracking the performance of a retail & commercial bank across
regions, product lines, and branches. Built to demonstrate end-to-end BI delivery: KPI definition,
star-schema data modeling, DAX measure authoring, and dashboard storytelling.

**Author:** Mrunal — Senior Data Analyst · Data & Business Intelligence
**Stack:** Power BI Desktop · DAX · Star Schema · Python (data generation)

> 🔗 **Live interactive demo:** open [`banking-kpi-dashboard.html`](./banking-kpi-dashboard.html) in a browser
> (a client-side replica of the Power BI report — no install needed). Host it free on GitHub Pages to get a
> shareable link for your resume.

--

## 📊 What it shows

The report answers the questions a Head of Retail Banking or CFO asks every month:

- **Are we growing?** Revenue vs. operating cost trend, MoM growth.
- **Is the balance sheet healthy?** Deposits vs. loans, loan-to-deposit ratio.
- **How efficient are we?** Cost-to-income ratio, net interest margin.
- **Where is the risk?** Non-performing asset (NPA) ratio by region.
- **Who is performing?** Branch-level league table with drill-through.
- **What's driving income?** Revenue split by product line.

### KPIs tracked

| KPI | Definition | Why it matters |
|-----|-----------|----------------|
| Total Revenue | Interest income + fee income | Top-line growth |
| Net Interest Margin (NIM) | (Interest income / earning assets), annualized | Core lending profitability |
| Cost-to-Income Ratio (CIR) | Operating cost / total revenue | Operational efficiency |
| Deposits & Loans (book) | End-of-period balances | Balance-sheet strength |
| Loan-to-Deposit Ratio | Loans / Deposits | Liquidity & funding |
| NPA Ratio | Non-performing assets / total loans | Asset quality / credit risk |
| Active Customers | Distinct active customers in period | Franchise scale |
| CSAT | Avg. customer satisfaction (1–5) | Service quality |

---

## 🗂️ Repository structure

```
banking-kpi-dashboard/
├── README.md                     ← this file
├── banking-kpi-dashboard.html    ← live browser demo of the report            
├── fact_kpi_monthly.csv          ← fact: monthly KPIs 
├── data-model.md                 ← star schema + data dictionary
├── dax-measures.md               ← all DAX measures, documented
├── data-generator.py             ← reproducible synthetic-data pipeline

## 🧱 Data model (star schema)

A classic star schema keeps DAX simple and the model fast:

```
        DimDate                 DimBranch
           │                        │
           └──────►  FactKPIMonthly ◄──────  DimProduct
```

- **FactKPIMonthly** — one row per branch × product × month (grain).
- **DimBranch** — branch, city, region, opened year.
- **DimProduct** — product line.
- **DimDate** — standard calendar (marked as date table).

Full field-level detail in [`docs/data-model.md`](./data-model.md).

---

## 🔁 Reproduce the data

```bash
python scripts/data-generator.py        # writes branches.csv + fact_kpi_monthly.csv
```

Deterministic (seeded) — anyone who runs it gets the identical dataset. The browser demo uses the same
generation logic in JavaScript, so the HTML and the Power BI model stay in sync.

---

## 🛠️ How to rebuild in Power BI Desktop

1. **Get Data → Text/CSV** → load `branches.csv` and `fact_kpi_monthly.csv`.
2. In **Model view**, create relationships: `FactKPIMonthly[BranchID] → DimBranch[BranchID]`, and a
   `DimDate[Date] → FactKPIMonthly[Month]` relationship (create a Date table with `CALENDAR`).
3. Paste the measures from [`dax/dax-measures.md`](./dax-measures.md) into a dedicated **_Measures** table.
4. Build visuals: KPI cards, line charts (Revenue vs Opex, Deposits vs Loans), donut (Revenue by Product),
   bar (Revenue by Region), and a table for the branch league.
5. Add slicers for **Region**, **Product**, and a **date-range** slider. Enable **drill-through** to a
   branch detail page.

---

## 📈 Results this pattern delivers (talking points for interviews)

- Replaced static monthly spreadsheets with a self-serve report → **decisions in minutes, not days**.
- Standardized KPI definitions across regions → **one source of truth** for revenue, NIM, and NPA.
- Drill-through + row-level security ready → **each branch manager sees only their book**.

---

*Synthetic data only — no real customer or bank information is used anywhere in this project.*
