import pandas as pd

DEFAULT_CONFIG = {
    "debt_equity_max": 1.5,
    "interest_coverage_min": 1.5,
    "roa_min": 0.05,
    "roe_min": 0.10
}

def solvency_engine(ratios_df: pd.DataFrame, config: dict | None = None) -> list:
    cfg = DEFAULT_CONFIG.copy()
    if config:
        cfg.update(config)
    
    results = []
    
    for _, row in ratios_df.iterrows():
        flags = {
            "leverage_risk": row["debt_equity"] > cfg["debt_equity_max"],
            "coverage_risk": row["interest_coverage"] < cfg["interest_coverage_min"],
            "return_risk": (row["roa"] < cfg["roa_min"]) or (row["roe"] < cfg["roe_min"])
        }
        
        risk_count = sum(flags.values())
        severity = "stable" if risk_count == 0 else "watch" if risk_count == 1 else "action"
        
        explanation_parts = []
        if flags["leverage_risk"]: explanation_parts.append("Debt levels are high.")
        if flags["coverage_risk"]: explanation_parts.append("Interest coverage is weak.")
        if flags["return_risk"]: explanation_parts.append("Returns on assets or equity are below expectations.")
        explanation = " ".join(explanation_parts) if explanation_parts else "Solvency indicators are healthy."
        
        results.append({
            "engine": "solvency_engine",
            "Company": row["Company"],
            "Year": row["Year"],
            "metrics": {
                "debt_equity": row["debt_equity"],
                "interest_coverage": row["interest_coverage"],
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
