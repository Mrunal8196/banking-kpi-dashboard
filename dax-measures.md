# DAX Measures — Banking KPI Dashboard

Create a dedicated `_Measures` table (Enter Data → empty table) and add each measure below.
All measures assume the star schema in `docs/data-model.md`.

> Units: `Revenue`, `Opex`, `InterestIncome`, `FeeIncome` are stored in **EUR thousands**;
> `Deposits`, `Loans` in **EUR millions**.

---

## Core totals

```dax
Total Revenue = SUM ( FactKPIMonthly[Revenue_EURk] )

Total Opex = SUM ( FactKPIMonthly[Opex_EURk] )

Interest Income = SUM ( FactKPIMonthly[InterestIncome_EURk] )

Fee Income = SUM ( FactKPIMonthly[FeeIncome_EURk] )

Total Deposits = SUM ( FactKPIMonthly[Deposits_EURm] )

Total Loans = SUM ( FactKPIMonthly[Loans_EURm] )
```

## Profitability & efficiency

```dax
Net Interest Margin % =
AVERAGE ( FactKPIMonthly[NIM_pct] )

Cost to Income % =
DIVIDE ( [Total Opex], [Total Revenue] ) * 100

Operating Profit =
[Total Revenue] - [Total Opex]

Loan to Deposit % =
DIVIDE ( [Total Loans], [Total Deposits] ) * 100
```

## Asset quality & customers

```dax
NPA Ratio % =
AVERAGE ( FactKPIMonthly[NPA_pct] )

Active Customers =
SUM ( FactKPIMonthly[ActiveCustomers] )

New Customers =
SUM ( FactKPIMonthly[NewCustomers] )

Avg CSAT =
AVERAGE ( FactKPIMonthly[CSAT] )
```

## Time intelligence (require a marked Date table)

```dax
Revenue PM =
CALCULATE ( [Total Revenue], DATEADD ( DimDate[Date], -1, MONTH ) )

Revenue MoM % =
VAR curr = [Total Revenue]
VAR prev = [Revenue PM]
RETURN DIVIDE ( curr - prev, prev ) * 100

Revenue YTD =
TOTALYTD ( [Total Revenue], DimDate[Date] )

Revenue Rolling 3M =
CALCULATE (
    [Total Revenue],
    DATESINRANGE ( DimDate[Date], EDATE ( MAX ( DimDate[Date] ), -2 ), MAX ( DimDate[Date] ) )
)
```

## Dynamic KPI status (for conditional formatting / cards)

```dax
NPA Status =
SWITCH (
    TRUE (),
    [NPA Ratio %] < 2,   "🟢 Healthy",
    [NPA Ratio %] < 2.8, "🟡 Watch",
    "🔴 Elevated"
)

CIR Status =
IF ( [Cost to Income %] <= 55, "🟢 Efficient", "🔴 Above target" )
```

## Ranking (branch league table)

```dax
Branch Revenue Rank =
RANKX ( ALL ( DimBranch[BranchName] ), [Total Revenue],, DESC, DENSE )
```

---

### Notes
- Wrap ratio measures in `DIVIDE()` to avoid divide-by-zero errors.
- Mark the Date table via **Table tools → Mark as date table** so time-intelligence functions work.
- For per-branch security, add a **row-level security** role: `[Region] = USERPRINCIPALNAME()` mapping,
  or a bridge table of user→branch.
