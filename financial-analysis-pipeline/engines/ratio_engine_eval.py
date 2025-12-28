# engines/ratio_engine_eval.py

import pandas as pd

DEFAULT_CONFIG = {
    # Liquidity
    "liquidity_min": 1.2,
    "quick_ratio_min": 1.0,

    # Profitability
    "gross_margin_min": 0.2,
    "operating_margin_min": 0.1,
    "net_margin_min": 0.05,

    # Leverage & coverage
    "debt_equity_max": 1.5,
    "interest_coverage_min": 1.5,

    # Efficiency & returns
    "asset_turnover_min": 0.5,
    "roa_min": 0.05,
    "roe_min": 0.10
}


def evaluate_ratios(ratios_df: pd.DataFrame, config: dict | None = None) -> list:
    """
    Evaluates locked ratio outputs against client configuration.
    Adds flags, severity, and explanation.
    """

    cfg = DEFAULT_CONFIG.copy()
    if config:
        cfg.update(config)

    results = []

    for _, row in ratios_df.iterrows():

        flags = {
            "liquidity_risk": (
                row["current_ratio"] < cfg["liquidity_min"]
                or row["quick_ratio"] < cfg["quick_ratio_min"]
            ),

            "profitability_risk": (
                row["gross_margin"] < cfg["gross_margin_min"]
                or row["operating_margin"] < cfg["operating_margin_min"]
                or row["net_margin"] < cfg["net_margin_min"]
            ),

            "leverage_risk": (
                row["debt_equity"] > cfg["debt_equity_max"]
            ),

            "coverage_risk": (
                row["interest_coverage"] < cfg["interest_coverage_min"]
            ),

            "efficiency_risk": (
                row["asset_turnover"] < cfg["asset_turnover_min"]
            ),

            "return_risk": (
                row["roa"] < cfg["roa_min"]
                or row["roe"] < cfg["roe_min"]
            )
        }

        # ---- Severity logic ----
        risk_count = sum(flags.values())

        if risk_count >= 3:
            severity = "action"
        elif risk_count >= 1:
            severity = "watch"
        else:
            severity = "stable"

        # ---- Plain-English explanation ----
        explanation_parts = []

        if flags["liquidity_risk"]:
            explanation_parts.append("Liquidity metrics fall below acceptable thresholds.")

        if flags["profitability_risk"]:
            explanation_parts.append("Profitability margins are under pressure.")

        if flags["leverage_risk"]:
            explanation_parts.append("Leverage levels exceed the preferred range.")

        if flags["coverage_risk"]:
            explanation_parts.append("Interest coverage is weak relative to financing costs.")

        if flags["efficiency_risk"]:
            explanation_parts.append("Asset utilization appears inefficient.")

        if flags["return_risk"]:
            explanation_parts.append("Returns on assets or equity are below expectations.")

        explanation = (
            " ".join(explanation_parts)
            if explanation_parts
            else "All core financial ratios are within configured thresholds."
        )

        results.append({
            "engine": "ratio_engine",
            "Company": row["Company"],
            "Year": row["Year"],
            "metrics": {
                "current_ratio": row["current_ratio"],
                "quick_ratio": row["quick_ratio"],
                "gross_margin": row["gross_margin"],
                "operating_margin": row["operating_margin"],
                "net_margin": row["net_margin"],
                "debt_equity": row["debt_equity"],
                "interest_coverage": row["interest_coverage"],
                "asset_turnover": row["asset_turnover"],
                "roa": row["roa"],
                "roe": row["roe"]
            },
            "flags": {
                **flags,
                "severity": severity
            },
            "explanation": explanation
        })

    return results
