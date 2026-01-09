from config.defaults import DEFAULT_CLIENT_CONFIG
from config.utils import merge_config
import pandas as pd

def afap_run(financials_df, client_config=None):
    # ---- Merge client config ----
    config = merge_config(
        DEFAULT_CLIENT_CONFIG,
        client_config or {}
    )

    # ---- Import engines ----
    from engines.ratio_engine_core import ratio_engine
    from engines.trend_engine import trend_engine
    from engines.cash_flow_engine import cash_flow_engine
    from engines.anomaly_efficiency_engine import anomaly_efficiency_engine
    from engines.solvency_engine import solvency_engine
    from engines.composite_risk_engine import composite_risk_engine

    # ---- Import AI Interpreter ----
    from ai_engine.llm_interpreter import afap_llm_interpretation

    # ---- Run deterministic engines ----
    ratios_list = ratio_engine(financials_df)  # keep canonical list output

    # ---- Convert list → DataFrame for convenience ----
    ratios_df = pd.DataFrame([
        {
            "Company": r["Company"],
            "Year": r["Year"],
            **r["metrics"]
        }
        for r in ratios_list
    ])

    # ---- Run other engines on the DataFrame ----
    trend = trend_engine(ratios_df)
    cash = cash_flow_engine(financials_df)
    anomaly = anomaly_efficiency_engine(ratios_df)
    solvency = solvency_engine(ratios_df)

    # ---- Compute composite risk ----
    composite = composite_risk_engine(
        trend, cash, anomaly, solvency, config
    )

    # ---- Prepare structured input for AI ----
    structured_records = []
    for i, row in ratios_df.iterrows():
        company = row["Company"]
        year = row["Year"]

        record = {
            "Company": company,
            "Year": year,
            "ratios": {k: row[k] for k in row.index if k not in ["Company", "Year"]},
            "trend": next((t["trends"] for t in trend if t["Company"] == company and t["Year"] == year), {}),
            "cash_flow": next((c["metrics"] for c in cash if c["Company"] == company and c["Year"] == year), {}),
            "anomaly": next((a["metrics"] for a in anomaly if a["Company"] == company and a["Year"] == year), {}),
            "solvency": next((s["metrics"] for s in solvency if s["Company"] == company and s["Year"] == year), {}),
            "composite_risk": next((c_r for c_r in composite if c_r["Company"] == company and c_r["Year"] == year), {})
        }

        structured_records.append(record)

    # ---- LLM Interpretation ----
    llm_results = afap_llm_interpretation(
        structured_records,
        model=config.get("ai_model", "local")
    )

    # ---- Return everything ----
    return {
        "ratios": ratios_list,        # keep canonical list output for validation
        "trend": trend,
        "cash_flow": cash,
        "anomaly": anomaly,
        "solvency": solvency,
        "composite_risk": composite,
        "ai_interpretation": llm_results
    }
