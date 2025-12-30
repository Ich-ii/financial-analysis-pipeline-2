import numpy as np
import pandas as pd

def anomaly_efficiency_engine(ratios_df: pd.DataFrame) -> list:
    """
    Detects anomalies and efficiency signals using ratio behavior only.
    Expects multi-year ratio data sorted by Company, Year.
    """

    ratios_df = ratios_df.sort_values(["Company", "Year"])
    results = []

    for company, group in ratios_df.groupby("Company"):
        group = group.reset_index(drop=True)

        for i, row in group.iterrows():
            anomalies = []
            efficiency_flags = {}

            if i == 0:
                results.append({
                    "engine": "anomaly_efficiency_engine",
                    "Company": company,
                    "Year": row["Year"],
                    "anomalies": None,
                    "flags": None,
                    "severity": "info",
                    "explanation": "Insufficient historical data for anomaly detection."
                })
                continue

            prev = group.loc[i - 1]

            # ---- YoY anomaly detection ----
            def pct_change(curr, prev):
                if prev == 0 or pd.isna(prev):
                    return None
                return (curr - prev) / abs(prev)

            ratio_checks = {
                "operating_margin": 0.30,
                "net_margin": 0.30,
                "roa": 0.30,
                "roe": 0.30,
                "debt_equity": 0.25,
                "asset_turnover": 0.25
            }

            yoy_changes = {}

            for ratio, threshold in ratio_checks.items():
                change = pct_change(row[ratio], prev[ratio])
                yoy_changes[ratio] = change

                if change is not None and abs(change) >= threshold:
                    anomalies.append(f"Sharp change detected in {ratio.replace('_',' ')}.")

            # ---- Structural efficiency logic ----
            efficiency_flags["liquidity_vs_profitability"] = (
                row["current_ratio"] > 2.0 and row["net_margin"] < 0
            )

            efficiency_flags["activity_without_returns"] = (
                row["asset_turnover"] > prev["asset_turnover"]
                and row["roa"] < 0
            )

            efficiency_flags["leverage_pressure"] = (
                row["debt_equity"] > prev["debt_equity"]
                and row["interest_coverage"] < 1.0
            )

            # ---- Severity logic ----
            anomaly_count = len(anomalies)
            flag_count = sum(efficiency_flags.values())

            if anomaly_count + flag_count >= 3:
                severity = "action"
            elif anomaly_count + flag_count >= 1:
                severity = "watch"
            else:
                severity = "stable"

            # ---- Explanation ----
            explanation_parts = []

            if anomalies:
                explanation_parts.append("Unusual year-over-year ratio movements detected.")

            if efficiency_flags["liquidity_vs_profitability"]:
                explanation_parts.append("Strong liquidity exists alongside weak profitability.")

            if efficiency_flags["activity_without_returns"]:
                explanation_parts.append("Operational activity is not translating into asset returns.")

            if efficiency_flags["leverage_pressure"]:
                explanation_parts.append("Leverage is increasing while coverage remains weak.")

            explanation = (
                " ".join(explanation_parts)
                if explanation_parts
                else "No significant anomalies or efficiency concerns detected."
            )

            results.append({
                "engine": "anomaly_efficiency_engine",
                "Company": company,
                "Year": row["Year"],
                "anomalies": anomalies if anomalies else None,
                "flags": efficiency_flags,
                "severity": severity,
                "explanation": explanation
            })

    return results
