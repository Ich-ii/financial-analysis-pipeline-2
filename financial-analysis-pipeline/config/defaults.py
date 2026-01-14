# ------------------------------------------------------------------
# AFAP Default Client Configuration
# ------------------------------------------------------------------

DEFAULT_CLIENT_CONFIG = {
    "client_name": "DEFAULT",

    # Engine-level defaults
    "engines": {
        "composite_risk": {
            "trend_weight": 0.25,
            "cash_flow_weight": 0.25,
            "anomaly_weight": 0.25,
            "solvency_weight": 0.25
        }
    },

    # Analysis-level engine settings (used by composite_risk_engine)
    "analysis": {
        "risk_weights": {
            "trend": 0.25,
            "cash_flow": 0.25,
            "anomaly": 0.25,
            "solvency": 0.25
        },
        "risk_bands": {
            "low": 0.25,
            "medium": 0.5,
            "high": 0.75
        }
    },

    # Input placeholders (client-specific)
    "inputs": {},

    # Output placeholders (client-specific)
    "outputs": {},

    # Feature flags (optional future expansion)
    "features_enabled": []
}
