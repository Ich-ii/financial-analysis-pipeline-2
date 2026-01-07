def afap_run(financials_df, client_config=None):
    from engines.ratio_engine_core import ratio_engine
    from engines.trend_engine import trend_engine
    from engines.cash_flow_engine import cash_flow_engine
    from engines.anomaly_efficiency_engine import anomaly_efficiency_engine
    from engines.solvency_engine import solvency_engine
    from engines.composite_risk_engine import composite_risk_engine
    import pandas as pd

    # 1. Core ratios (list output)
    ratios_list = ratio_engine(financials_df)

    # 🔁 Normalize ONCE
    ratios_df = pd.DataFrame(ratios_list)

    # 2. Deterministic engines
    trend = trend_engine(ratios_df)
    cash = cash_flow_engine(financials_df)
    anomaly = anomaly_efficiency_engine(ratios_df)
    solvency = solvency_engine(ratios_df)

    # 3. Composite risk
    composite = composite_risk_engine(
        trend, cash, anomaly, solvency
    )

    return {
        "ratios": ratios_list,     # keep canonical output
        "trend": trend,
        "cash_flow": cash,
        "anomaly": anomaly,
        "solvency": solvency,
        "composite_risk": composite
    }
