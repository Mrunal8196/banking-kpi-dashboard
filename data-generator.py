"""
data-generator.py
Reproducible synthetic-data pipeline for the Banking KPI Dashboard.

Produces:
  data/branches.csv           -- DimBranch (branch master)
  data/fact_kpi_monthly.csv   -- FactKPIMonthly (branch x product x month)

Deterministic: seeded RNG, so every run yields identical data.
No real customer or bank data is used.

Usage:
  python data-generator.py
"""
import csv
import math
import os
import random
import datetime

SEED = 42
OUT_DIR = "data"

REGIONS = {
    "North": ["Berlin", "Hamburg", "Hannover"],
    "South": ["Munich", "Stuttgart", "Nuremberg"],
    "West":  ["Cologne", "Frankfurt", "Dusseldorf"],
    "East":  ["Leipzig", "Dresden", "Erfurt"],
}
PRODUCTS = ["Retail Banking", "Corporate Banking", "Wealth Management",
            "SME Lending", "Cards & Payments"]
PMIX = {"Retail Banking": 1.0, "Corporate Banking": 1.8, "Wealth Management": 1.3,
        "SME Lending": 0.9, "Cards & Payments": 0.5}
GROWTH = {"North": 1.010, "South": 1.014, "West": 1.008, "East": 1.006}
SUFFIX = ["Central", "Nord", "Sud", "West", "Ost"]


def month_range(start, n):
    months, d = [], start
    for _ in range(n):
        months.append(d)
        y = d.year + (d.month // 12)
        m = d.month % 12 + 1
        d = datetime.date(y, m, 1)
    return months


def build_branches(rng):
    branches, bid = [], 1000
    for region, cities in REGIONS.items():
        for city in cities:
            for k in range(rng.randint(2, 3)):
                bid += 1
                branches.append({
                    "BranchID": bid,
                    "BranchName": f"{city} {SUFFIX[k] if k < len(SUFFIX) else k}",
                    "City": city,
                    "Region": region,
                    "OpenedYear": rng.randint(1998, 2019),
                    "_scale": rng.uniform(0.6, 1.6),
                })
    return branches


def build_facts(rng, branches, months):
    rows = []
    for b in branches:
        for p in PRODUCTS:
            seed_dep = rng.uniform(20, 60) * b["_scale"] * PMIX[p]
            seed_loan = rng.uniform(15, 50) * b["_scale"] * PMIX[p]
            for idx, mo in enumerate(months):
                g = GROWTH[b["Region"]] ** idx
                season = 1 + 0.05 * math.sin((mo.month / 12) * 2 * math.pi)
                deposits = round(seed_dep * g * season * rng.uniform(0.97, 1.03), 2)
                loans = round(seed_loan * g * season * rng.uniform(0.96, 1.04), 2)
                nim = round(rng.uniform(2.4, 3.6), 2)
                interest = round(loans * (nim / 100) / 12 * 1000, 2)
                fee = round(deposits * rng.uniform(0.001, 0.004) * 1000, 2)
                revenue = round(interest + fee, 2)
                opex = round(revenue * rng.uniform(0.45, 0.62), 2)
                npa = round(max(0.4, rng.gauss(2.1, 0.6)), 2)
                new_cust = int(max(0, rng.gauss(120, 40) * b["_scale"] * PMIX[p] / 2))
                active = int(seed_dep * g * 180 * PMIX[p])
                csat = round(min(5, max(3.2, rng.gauss(4.2, 0.3))), 2)
                rows.append({
                    "Month": mo.isoformat(), "BranchID": b["BranchID"],
                    "Region": b["Region"], "Product": p,
                    "Deposits_EURm": deposits, "Loans_EURm": loans, "NIM_pct": nim,
                    "InterestIncome_EURk": interest, "FeeIncome_EURk": fee,
                    "Revenue_EURk": revenue, "Opex_EURk": opex, "NPA_pct": npa,
                    "NewCustomers": new_cust, "ActiveCustomers": active, "CSAT": csat,
                })
    return rows


def write_csv(path, fieldnames, rows):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow({k: r[k] for k in fieldnames})


def main():
    rng = random.Random(SEED)
    months = month_range(datetime.date(2024, 1, 1), 30)
    branches = build_branches(rng)
    facts = build_facts(rng, branches, months)

    write_csv(f"{OUT_DIR}/branches.csv",
              ["BranchID", "BranchName", "City", "Region", "OpenedYear"], branches)
    write_csv(f"{OUT_DIR}/fact_kpi_monthly.csv",
              ["Month", "BranchID", "Region", "Product", "Deposits_EURm", "Loans_EURm",
               "NIM_pct", "InterestIncome_EURk", "FeeIncome_EURk", "Revenue_EURk",
               "Opex_EURk", "NPA_pct", "NewCustomers", "ActiveCustomers", "CSAT"], facts)

    print(f"Wrote {len(branches)} branches and {len(facts)} fact rows "
          f"({months[0]} -> {months[-1]}).")


if __name__ == "__main__":
    main()
