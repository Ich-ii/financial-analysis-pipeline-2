import pandas as pd
from .schema_validator import validate_engine_output
from engines.data_normalizer import normalize_financial_df
from engines.ratio_validator import validate_ratios

def ratio_engine(input_df: pd.DataFrame) -> list[dict]:
    """
    AFAP Phase 3 — Locked Deterministic Ratio Engine
    Outputs canonical AFAP format with 'metrics', 'flags', 'severity', and 'explanation'.
    """

    required_cols = [
        "Company",
        "Year",
        "FS Category",
        "FS Subcategory", 
        "Amount"
    ]
    input_df = normalize_financial_df(input_df)
    missing = [c for c in required_cols if c not in input_df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    results = []

    for company, grp in input_df.groupby("Company"):
        grp = grp.sort_values("Year")

        for year, year_grp in grp.groupby("Year"):

            def get_amount(category, subcategory):
                row = year_grp[
                    (year_grp["FS Category"] == category) &
                    (year_grp["FS Subcategory"] == subcategory)
                ]
                return row["Amount"].sum() if not row.empty else None

            # ---- Core values ----
            current_assets = get_amount("Assets", "Current Assets")
            non_current_assets = get_amount("Assets", "Non-Current Assets")
            inventory = get_amount("Assets", "Inventory")

            current_liabilities = get_amount("Liabilities", "Current Liabilities")
            non_current_liabilities = get_amount("Liabilities", "Non-Current Liabilities")

            revenue = get_amount("Revenue", "Revenue")
            cogs = get_amount("Expenses", "COGS")
            opex = get_amount("Expenses", "Operating Expenses")
            finance_costs = get_amount("Expenses", "Finance Costs")
            tax = get_amount("Expenses", "Tax")

            equity = get_amount("Equity", "Equity")

            total_assets = (
                (current_assets or 0) + (non_current_assets or 0)
                if current_assets is not None or non_current_assets is not None
                else None
            )

            total_liabilities = (
                (current_liabilities or 0) + (non_current_liabilities or 0)
                if current_liabilities is not None or non_current_liabilities is not None
                else None
            )

            operating_profit = (
                revenue - cogs - opex
                if revenue is not None and cogs is not None and opex is not None
                else None
            )

            net_income = (
                operating_profit - finance_costs - tax
                if operating_profit is not None and finance_costs is not None and tax is not None
                else None
            )

            # ---- Ratios wrapped in metrics ----
            metrics = {
                "current_ratio": (
                    current_assets / current_liabilities
                    if current_assets is not None and current_liabilities not in (None, 0)
                    else None
                ),
                "quick_ratio": (
                    (current_assets - (inventory or 0)) / current_liabilities
                    if current_assets is not None and current_liabilities not in (None, 0)
                    else None
                ),
                "gross_margin": (
                    (revenue - cogs) / revenue
                    if revenue not in (None, 0) and cogs is not None
                    else None
                ),
                "operating_margin": (
                    operating_profit / revenue
                    if operating_profit is not None and revenue not in (None, 0)
                    else None
                ),
                "net_margin": (
                    net_income / revenue
                    if net_income is not None and revenue not in (None, 0)
                    else None
                ),
                "debt_equity": (
                    total_liabilities / equity
                    if total_liabilities is not None and equity not in (None, 0)
                    else None
                ),
                "interest_coverage": (
                    operating_profit / finance_costs
                    if operating_profit is not None and finance_costs not in (None, 0)
                    else None
                ),
                "asset_turnover": (
                    revenue / total_assets
                    if revenue is not None and total_assets not in (None, 0)
                    else None
                ),
                "roa": (
                    net_income / total_assets
                    if net_income is not None and total_assets not in (None, 0)
                    else None
                ),
                "roe": (
                    net_income / equity
                    if net_income is not None and equity not in (None, 0)
                    else None
                )
            }
# Validation gate
            metrics = validate_ratios(metrics, company, year)
            results.append({
                "engine": "ratio_engine",
                "Company": company,
                "Year": int(year),
                "metrics": metrics,
                "flags": {},           # no flags for ratio engine
                "severity": "stable",  # base ratios are stable
                "explanation": "Canonical financial ratios"
            })

    validate_engine_output(results, "ratio_engine")
    
    return results
