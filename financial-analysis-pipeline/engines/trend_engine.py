import pandas as pd
from .schema_validator import validate_engine_output

def trend_engine(ratios_list):
    """
    AFAP Phase 3 — Locked Trend Engine
    Evaluates directional trends in key financial ratios.
    """

    df = pd.DataFrame(ratios_list)

    if df.empty:
        return []

    results = []

    ratios = [
        "current_ratio",
        "gross_margin",
        "net_margin",
        "asset_turnover",
        "debt_equity",
        "roe"
    ]

    for company, grp in df.groupby("Company"):
        grp = grp.sort_values("Year")

        if len(grp) < 2:
            continue  # cannot compute trend

        start_year = int(grp.iloc[0]["Year"])
        end_year = int(grp.iloc[-1]["Year"])

        for ratio in ratios:
            if ratio not in grp.columns:
                continue

            trend_value = grp[ratio].iloc[-1] - grp[ratio].iloc[0]

            flags = {
                "deteriorating_trend": trend_value < 0
            }

            severity = (
                "watch" if trend_value < 0 else "stable"
            )

            results.append({
                "engine": "trend_engine",
                "Company": company,
                "Year": end_year,  # 🔑 anchor to most recent year
                "metrics": {
                    "ratio": ratio,
                    "trend_value": trend_value,
                    "from_year": start_year,
                    "to_year": end_year
                },
                "flags": flags,
                "severity": severity,
                "explanation": (
                    f"Negative trend observed in {ratio}."
                    if severity == "watch"
                    else f"{ratio} trend stable or improving."
                )
            })

    validate_engine_output(results, "trend_engine")
    return results
