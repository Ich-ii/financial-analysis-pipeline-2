import pandas as pd
from .schema_validator import validate_engine_output
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


def evaluate_ratios(input_df: pd.DataFrame, config: dict | None = None) -> list[dict]:
    """
    AFAP Phase 3 — Locked Ratio Evaluation Engine
    """

    required_cols = [
        "Company", "Year",
        "current_ratio", "quick_ratio",
        "gross_margin", "operating_margin", "net_margin",
        "debt_equity", "interest_coverage",
        "asset_turnover", "roa", "roe"
    ]
    missing = [c for c in required_cols if c not in input_df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    cfg = DEFAULT_CONFIG.copy()
    if config:
        cfg.update(config)

    results = []

    for company, grp in input_df.groupby("Company"):
        grp = grp.sort_values("Year")

        for _, row in grp.iterrows():

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

            risk_count = sum(flags.values())
            severity = "action" if risk_count >= 3 else "watch" if risk_count >= 1 else "stable"

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
    "Company": company,
    "Year": int(row["Year"]),

    # 🔹 expose ratios as real columns
    "current_ratio": row["current_ratio"],
    "quick_ratio": row["quick_ratio"],
    "gross_margin": row["gross_margin"],
    "operating_margin": row["operating_margin"],
    "net_margin": row["net_margin"],
    "debt_equity": row["debt_equity"],
    "interest_coverage": row["interest_coverage"],
    "asset_turnover": row["asset_turnover"],
    "roa": row["roa"],
    "roe": row["roe"],

    # 🔹 keep metrics dict for schema validation
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

    "flags": {**flags, "severity": severity},
    "explanation": explanation
})



    validate_engine_output(results, "ratio_engine_eval")
    return results

