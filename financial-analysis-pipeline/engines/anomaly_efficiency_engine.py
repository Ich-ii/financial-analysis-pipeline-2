import pandas as pd


def anomaly_efficiency_engine(df: pd.DataFrame) -> list:
    """
    Detects anomalies and efficiency issues using ratio-based signals only.
    Input: ratio_engine_core output as DataFrame
    """

    results = []

    df = (
        df.sort_values(["Company", "Year"])
        .copy()
    )

    # --- YoY changes on ratios ---
    ratio_cols = [
        "operating_margin",
        "net_margin",
        "asset_turnover",
        "roa",
        "roe"
    ]

    for col in ratio_cols:
        df[f"{col}_yoy"] = df.groupby("Company")[col].pct_change()

    for _, row in df.iterrows():

        flags = {
            "margin_anomaly": (
                row["operating_margin"] < df["operating_margin"].mean() * 0.7
            ),

            "profitability_shock": (
                row["net_margin_yoy"] < -0.30
                if pd.notna(row["net_margin_yoy"])
                else False
            ),

            "efficiency_drop": (
                row["asset_turnover_yoy"] < -0.25
                if pd.notna(row["asset_turnover_yoy"])
                else False
            ),

            "roa_shock": (
                row["roa_yoy"] < -0.40
                if pd.notna(row["roa_yoy"])
                else False
            ),

            "roe_stress": (
                row["roe"] < 0
            )
        }

        anomaly_count = sum(flags.values())

        if anomaly_count >= 2:
            severity = "high"
        elif anomaly_count == 1:
            severity = "watch"
        else:
            severity = "normal"

        explanation = (
            "Multiple efficiency or profitability anomalies detected across periods."
            if severity == "high"
            else "Some operational ratios show abnormal movement."
            if severity == "watch"
            else "Efficiency and profitability ratios appear stable."
        )

        results.append({
            "engine": "anomaly_efficiency_engine",
            "Company": row["Company"],
            "Year": row["Year"],
            "metrics": {
                "operating_margin_yoy": row["operating_margin_yoy"],
                "net_margin_yoy": row["net_margin_yoy"],
                "asset_turnover_yoy": row["asset_turnover_yoy"],
                "roa_yoy": row["roa_yoy"],
                "roe": row["roe"]
            },
            "flags": flags,
            "severity": severity,
            "explanation": explanation
        })

    return results
