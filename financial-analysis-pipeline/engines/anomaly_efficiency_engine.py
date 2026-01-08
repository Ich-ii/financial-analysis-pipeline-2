import pandas as pd
from .schema_validator import validate_engine_output

def anomaly_efficiency_engine(ratios_list):
    """
    AFAP Phase 3 — Locked Efficiency Anomaly Engine
    Detects abnormal ROA changes year-over-year.
    """

    df = pd.DataFrame(ratios_list)

    if df.empty:
        return []

    required_cols = ["Company", "Year", "roa"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    results = []

    for company, grp in df.groupby("Company"):
        grp = grp.sort_values("Year").reset_index(drop=True)
        grp["roa_yoy"] = grp["roa"].pct_change()

        for _, row in grp.iterrows():
            flags = {
                "roa_shock": (
                    row["roa_yoy"] < -0.4
                    if pd.notna(row["roa_yoy"])
                    else False
                )
            }

            count = sum(flags.values())

            severity = (
                "high" if count >= 2
                else "watch" if count == 1
                else "normal"
            )

            results.append({
                "engine": "anomaly_efficiency_engine",
                "Company": row["Company"],
                "Year": int(row["Year"]),
                "metrics": {
                    "roa_yoy": row["roa_yoy"]
                },
                "flags": flags,
                "severity": severity,
                "explanation": (
                    "Abnormal efficiency change detected."
                    if severity != "normal"
                    else "Efficiency metrics stable."
                )
            })

    # ✅ Validation MUST be inside the function
    validate_engine_output(results, "anomaly_efficiency_engine")

    return results
