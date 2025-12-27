import pandas as pd

def ratio_engine(financials: pd.DataFrame) -> list:
    """
    Deterministic Ratio Engine (AFAP Phase 2)

    Input:
        financials DataFrame with columns:
        Company, Year, FS Category, FS Subcategory, Statement, Amount

    Output:
        List of dictionaries:
        - metrics
        - flags
        - plain-English explanations
    """

    results = []

    # Loop per company-year (real client structure)
    for (company, year), group in financials.groupby(["Company", "Year"]):

        def get_amount(category, subcategory):
            row = group[
                (group["FS Category"] == category) &
                (group["FS Subcategory"] == subcategory)
            ]
            return row["Amount"].sum() if not row.empty else None

        # ---- Extract core values ----
        current_assets = get_amount("Assets", "Current Assets")
        current_liabilities = get_amount("Liabilities", "Current Liabilities")
        revenue = get_amount("Revenue", "Revenue")
        cogs = get_amount("Expenses", "COGS")
        equity = get_amount("Equity", "Equity")
        total_liabilities = (
            get_amount("Liabilities", "Current Liabilities") or 0
        ) + (
            get_amount("Liabilities", "Non-Current Liabilities") or 0
        )

        # ---- Compute ratios (safe) ----
        current_ratio = (
            current_assets / current_liabilities
            if current_assets is not None and current_liabilities not in (None, 0)
            else None
        )

        gross_margin = (
            (revenue - cogs) / revenue
            if revenue not in (None, 0) and cogs is not None
            else None
        )

        debt_to_equity = (
            total_liabilities / equity
            if equity not in (None, 0)
            else None
        )

        # ---- Flags ----
        liquidity_risk = current_ratio is not None and current_ratio < 1
        leverage_risk = debt_to_equity is not None and debt_to_equity > 2

        # ---- Explanations ----
        explanations = {}

        if current_ratio is None:
            explanations["current_ratio"] = "Insufficient data to assess liquidity."
        elif liquidity_risk:
            explanations["current_ratio"] = "Current liabilities exceed current assets."
        else:
            explanations["current_ratio"] = "Liquidity position appears adequate."

        if gross_margin is None:
            explanations["gross_margin"] = "Revenue or cost data missing."
        elif gross_margin < 0:
            explanations["gross_margin"] = "Costs exceed revenue."
        else:
            explanations["gross_margin"] = "Core operations are generating margin."

        if debt_to_equity is None:
            explanations["debt_to_equity"] = "Equity or liability data missing."
        elif leverage_risk:
            explanations["debt_to_equity"] = "Company is highly leveraged."
        else:
            explanations["debt_to_equity"] = "Leverage is within a reasonable range."

        # ---- Final output ----
        results.append({
            "Company": company,
            "Year": year,
            "metrics": {
                "current_ratio": current_ratio,
                "gross_margin": gross_margin,
                "debt_to_equity": debt_to_equity
            },
            "flags": {
                "liquidity_risk": liquidity_risk,
                "leverage_risk": leverage_risk
            },
            "explanations": explanations
        })

    return results
