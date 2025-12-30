import pandas as pd

def cash_flow_engine(financials: pd.DataFrame) -> list:
    """
    AFAP Phase 2 — Cash Flow Health Engine (Proxy-Based)

    Assesses sustainability using operating profit consistency
    and coverage proxies when cash flow statements are unavailable.
    """

    results = []

    for (company, year), group in financials.groupby(["Company", "Year"]):

        def get_amount(category, subcategory):
            row = group[
                (group["FS Category"] == category) &
                (group["FS Subcategory"] == subcategory)
            ]
            return row["Amount"].sum() if not row.empty else None

        revenue = get_amount("Revenue", "Revenue")
        cogs = get_amount("Expenses", "COGS")
        opex = get_amount("Expenses", "Operating Expenses")
        finance_costs = get_amount("Expenses", "Finance Costs")

        operating_profit = (
            revenue - cogs - opex
            if None not in (revenue, cogs, opex)
            else None
        )

        coverage_proxy = (
            operating_profit / finance_costs
            if operating_profit is not None and finance_costs not in (None, 0)
            else None
        )

        # ---- Flags ----
        flags = {
            "negative_operating_profit": (
                operating_profit is not None and operating_profit < 0
            ),
            "weak_coverage": (
                coverage_proxy is not None and coverage_proxy < 1
            )
        }

        # ---- Severity ----
        if all(flags.values()):
            severity = "action"
        elif any(flags.values()):
            severity = "watch"
        else:
            severity = "stable"

        # ---- Explanation ----
        if severity == "action":
            explanation = (
                "Operating activities do not appear to generate sufficient "
                "cash to cover financing obligations."
            )
        elif severity == "watch":
            explanation = (
                "Cash generation shows signs of pressure and warrants monitoring."
            )
        else:
            explanation = (
                "Operating activities appear sufficient to sustain financing needs."
            )

        results.append({
            "engine": "cash_flow_engine",
            "Company": company,
            "Year": year,
            "metrics": {
                "operating_profit": operating_profit,
                "coverage_proxy": coverage_proxy
            },
            "flags": {
                **flags,
                "severity": severity
            },
            "explanation": explanation
        })

    return results
