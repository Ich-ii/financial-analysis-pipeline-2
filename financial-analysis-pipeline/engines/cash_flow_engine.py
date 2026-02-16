import pandas as pd
from .schema_validator import validate_engine_output
from .data_normalizer import normalize_financial_df  # ✅ import normalizer

def cash_flow_engine(financials: pd.DataFrame) -> list:
    """
    AFAP Phase 3 — Cash Flow Health Engine
    Produces top-level severity for composite risk scoring.
    Automatically normalizes raw Amount data.
    """

    # ✅ Normalize financials at the start
    financials = normalize_financial_df(financials)

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

        # Flags
        flags = {
            "negative_operating_profit": (
                operating_profit is not None and operating_profit < 0
            ),
            "weak_coverage": (
                coverage_proxy is not None and coverage_proxy < 1
            )
        }

        # Top-level severity
        if all(flags.values()):
            severity = "action"
        elif any(flags.values()):
            severity = "watch"
        else:
            severity = "stable"

        # Explanation
        explanation = (
            "Operating activities do not appear to generate sufficient cash to cover financing obligations."
            if severity == "action"
            else "Cash generation shows signs of pressure and warrants monitoring."
            if severity == "watch"
            else "Operating activities appear sufficient to sustain financing needs."
        )

        # ✅ Append AFAP Phase-3 compliant row
        results.append({
            "engine": "cash_flow_engine",
            "Company": company,
            "Year": year,
            "metrics": {
                "operating_profit": operating_profit,
                "coverage_proxy": coverage_proxy
            },
            "flags": flags,
            "severity": severity,
            "explanation": explanation
        })

    # ✅ Validation inside the function
    validate_engine_output(results, "cash_flow_engine")
    return results
