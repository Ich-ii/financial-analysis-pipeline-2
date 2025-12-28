import pandas as pd

def trend_engine(ratios_df: pd.DataFrame) -> list:
    """
    Calculates YoY trends and volatility for ratio metrics.
    Expects a flat ratios DataFrame.
    """

    results = []

    ratios = [
        "current_ratio",
        "gross_margin",
        "net_margin",
        "debt_equity",
        "asset_turnover",
        "roa",
        "roe"
    ]

    for company, grp in ratios_df.groupby("Company"):
        grp = grp.sort_values("Year")

        for _, row in grp.iterrows():
            year = row["Year"]

            trends = {}

            prev = grp[grp["Year"] == year - 1]

            for r in ratios:
                if not prev.empty:
                    prev_val = prev.iloc[0][r]
                    curr_val = row[r]

                    if pd.notna(prev_val) and pd.notna(curr_val):
                        trends[r] = {
                            "value": curr_val,
                            "yoy_change": curr_val - prev_val,
                            "trend": (
                                "up" if curr_val > prev_val
                                else "down" if curr_val < prev_val
                                else "flat"
                            )
                        }
                    else:
                        trends[r] = None
                else:
                    trends[r] = None

            results.append({
                "engine": "trend_engine",
                "Company": company,
                "Year": year,
                "trends": trends
            })

    return results
