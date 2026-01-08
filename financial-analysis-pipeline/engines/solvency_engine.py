import pandas as pd
from .schema_validator import validate_engine_output

def solvency_engine(ratios_list):
    """
    AFAP Phase 3 — Locked Solvency Engine
    Evaluates capital structure and coverage metrics.
    """

    # Convert input to DataFrame
    df = pd.DataFrame(ratios_list)

    if df.empty:
        return []

    required_cols = ["Company", "Year", "debt_equity", "interest_coverage"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    results = []

    for company, grp in df.groupby("Company"):
        grp = grp.sort_values("Year")

        for _, row in grp.iterrows():
            flags = {
                "high_leverage": row["debt_equity"] > 1.5,
                "weak_coverage": row["interest_coverage"] < 1.5
            }

            count = sum(flags.values())

            severity = (
                "action" if count == 2
                else "watch" if count == 1
                else "stable"
            )

            results.append({
                "engine": "solvency_engine",
                "Company": company,
                "Year": int(row["Year"]),
                "metrics": {
                    "debt_equity": row["debt_equity"],
                    "interest_coverage": row["interest_coverage"]
                },
                "flags": flags,
                "severity": severity,
                "explanation": (
                    "Capital structure shows solvency risk."
                    if severity != "stable"
                    else "Solvency position acceptable."
                )
            })

    # ✅ Schema validation stays INSIDE the engine
    validate_engine_output(results, "solvency_engine")

    return results
