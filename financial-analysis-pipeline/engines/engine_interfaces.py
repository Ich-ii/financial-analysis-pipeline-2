# engines/engine_interfaces.py

ENGINE_SCHEMAS = {

    "ratio_engine": {
        "required_keys": {"engine", "Company", "Year", "metrics"},
        "metrics": {
            "current_ratio",
            "quick_ratio",
            "gross_margin",
            "operating_margin",
            "net_margin",
            "debt_equity",
            "interest_coverage",
            "asset_turnover",
            "roa",
            "roe"
        }
    },

    "trend_engine": {
        "required_keys": {
            "engine", "Company", "Year",
            "metrics", "flags", "severity", "explanation"
        }
    },

    "cash_flow_engine": {
        "required_keys": {
            "engine", "Company", "Year",
            "metrics", "flags", "severity", "explanation"
        }
    },

    "anomaly_efficiency_engine": {
        "required_keys": {
            "engine", "Company", "Year",
            "metrics", "flags", "severity", "explanation"
        }
    },

    "solvency_engine": {
        "required_keys": {
            "engine", "Company", "Year",
            "metrics", "flags", "severity", "explanation"
        }
    },

    "composite_risk_engine": {
        "required_keys": {
            "engine", "Company", "Year",
            "composite_score", "risk_band"
        }
    }
}
