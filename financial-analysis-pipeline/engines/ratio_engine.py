import pandas as pd


def ratio_engine(financials: pd.DataFrame) -> list[dict]:
    """
    AFAP Phase 2 — Locked Deterministic Ratio Engine

    Purpose:
    - Compute financial ratios ONLY
    - No configs
    - No flags
    - No explanations
    - Fully deterministic & testable

    Input:
    - Standardized financial statements dataframe

    Output:
    - List of dicts, one per Company-Year
    """

    results = []

    for (company, year), group in financials.groupby(["Company", "Year"]):

        def get_amount(category, subcategory):
            row = group[
                (group["FS Category"] == category) &
                (group["FS Subcategory"] == subcategory)
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

        # ---- Ratios (strict guards, no truthiness bugs) ----
        ratios = {
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

        results.append({
            "Company": company,
            "Year": year,
            **ratios
        })

    return results
