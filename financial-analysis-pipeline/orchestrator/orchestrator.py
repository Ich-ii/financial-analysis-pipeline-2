from config.defaults import DEFAULT_CLIENT_CONFIG
from config.utils import merge_config

def afap_run(financials_df, client_config=None):
    config = merge_config(
        DEFAULT_CLIENT_CONFIG,
        client_config or {}
    )

    from engines.ratio_engine_core import ratio_engine
    from engines.trend_engine import trend_engine
    from engines.cash_flow_engine import cash_flow_engine
    from engines.anomaly_efficiency_engine import anomaly_efficiency_engine
    from engines.solvency_engine import solvency_engine
    from engines.composite_risk_engine import composite_risk_engine

    ratios_df = ratio_engine(financials_df)

    trend = trend_engine(ratios_df)
    cash = cash_flow_engine(financials_df)
    anomaly = anomaly_efficiency_engine(ratios_df)
    solvency = solvency_engine(ratios_df)

    composite = composite_risk_engine(
        trend, cash, anomaly, solvency, config
    )

    return {
        "ratios": ratios_df,
        "trend": trend,
        "cash_flow": cash,
        "anomaly": anomaly,
        "solvency": solvency,
        "composite_risk": composite
    }
