# ------------------------------------------------------------------
# AFAP Orchestrator Output Contract (Frozen)
# ------------------------------------------------------------------

AFAP_OUTPUT_KEYS = [
    "profile_used",
    "ratios",
    "trend",
    "cash_flow",
    "anomaly",
    "solvency",
    "composite_risk",
    "ai_interpretation"
]

from datetime import datetime
import pandas as pd
from config.defaults import DEFAULT_CLIENT_CONFIG
from config.utils import merge_config

# ------------------------------------------------------------------
# Analysis Profiles (AIFs – AFAP Interpretation Frameworks)
# ------------------------------------------------------------------

ANALYSIS_PROFILES = {
    "full_diagnostic": {
        "engines": ["ratio", "trend", "cash_flow", "anomaly", "solvency", "composite_risk"],
        "metrics_scope": "all"
    },
    "solvency_focus": {
        "engines": ["ratio", "solvency", "composite_risk"],
        "metrics_scope": ["debt_to_equity", "interest_coverage", "equity_ratio"]
    },
    "liquidity_focus": {
        "engines": ["ratio", "trend", "cash_flow", "composite_risk"],
        "metrics_scope": ["current_ratio", "quick_ratio", "cash_ratio"]
    },
    "performance_focus": {
        "engines": ["ratio", "trend"],
        "metrics_scope": ["operating_margin", "net_margin", "asset_turnover"]
    },
    "risk_scan": {
        "engines": ["ratio", "solvency", "anomaly", "composite_risk"],
        "metrics_scope": "all"
    },
    "going_concern_screen": {
        "engines": ["ratio", "trend", "solvency", "composite_risk"],
        "metrics_scope": "critical_only"
    }
}

# ------------------------------------------------------------------
# Safe engine payload extractor (schema-agnostic)
# ------------------------------------------------------------------

def extract_engine_payload(engine_outputs, company, year):
    """
    Extracts the non-identifying payload from an engine output safely.
    """
    for record in engine_outputs:
        if record.get("Company") == company and record.get("Year") == year:
            return {k: v for k, v in record.items() if k not in ("Company", "Year", "engine")}
    return {}

# ------------------------------------------------------------------
# AFAP Orchestrator
# ------------------------------------------------------------------

def afap_run(
    financials_df,
    client_config=None,
    analysis_profile="full_diagnostic",
    external_context=None,
    use_mock_ai=False
):
    """
    Runs AFAP analysis for a given financials DataFrame and profile.
    """

    # ------------------------------------------------------------------
    # Merge client config with defaults
    # ------------------------------------------------------------------
    merged_config = merge_config(DEFAULT_CLIENT_CONFIG, client_config or {})
    analysis_config = merged_config.get("analysis", {})

    # ------------------------------------------------------------------
    # Validate profile
    # ------------------------------------------------------------------
    profile = ANALYSIS_PROFILES.get(analysis_profile)
    if not profile:
        raise ValueError(f"Unknown analysis profile: {analysis_profile}")

    engines_to_run = profile["engines"]

    # ------------------------------------------------------------------
    # Import Engines
    # ------------------------------------------------------------------
    from engines.ratio_engine_core import ratio_engine
    from engines.trend_engine import trend_engine
    from engines.cash_flow_engine import cash_flow_engine
    from engines.anomaly_efficiency_engine import anomaly_efficiency_engine
    from engines.solvency_engine import solvency_engine
    from engines.composite_risk_engine import composite_risk_engine

    # ------------------------------------------------------------------
    # Import AI Interpreter
    # ------------------------------------------------------------------
    from afap_ai_engine.ai_interpreter import afap_llm_interpretation

    # ------------------------------------------------------------------
    # Initialize Outputs
    # ------------------------------------------------------------------
    outputs = {k: [] for k in AFAP_OUTPUT_KEYS if k != "profile_used"}

    # ------------------------------------------------------------------
    # Ratio Engine (Canonical Base)
    # ------------------------------------------------------------------
    ratios_list = ratio_engine(financials_df) if "ratio" in engines_to_run else []
    outputs["ratios"] = ratios_list

    ratios_df = pd.DataFrame([{"Company": r["Company"], "Year": r["Year"], **r["metrics"]} for r in ratios_list]) if ratios_list else pd.DataFrame()
    ratios_flat = ratios_df.copy()

    # ------------------------------------------------------------------
    # Conditional Engines
    # ------------------------------------------------------------------
    if "trend" in engines_to_run:
        outputs["trend"] = trend_engine(ratios_flat)

    if "cash_flow" in engines_to_run:
        outputs["cash_flow"] = cash_flow_engine(financials_df)

    if "anomaly" in engines_to_run:
        outputs["anomaly"] = anomaly_efficiency_engine(ratios_flat)

    if "solvency" in engines_to_run:
        outputs["solvency"] = solvency_engine(ratios_flat)

    if "composite_risk" in engines_to_run:
        outputs["composite_risk"] = composite_risk_engine(
            outputs.get("trend", []),
            outputs.get("cash_flow", []),
            outputs.get("anomaly", []),
            outputs.get("solvency", []),
            {"analysis": analysis_config}
        )

    # ------------------------------------------------------------------
    # Structured Records for LLM (Profile + Temporal + Context Aware)
    # ------------------------------------------------------------------
    structured_records = []
    current_year = datetime.now().year

    # Wrap flat external_context under "global" for LLM
    external_context = {"global": external_context or {}}

    for _, row in ratios_df.iterrows():
        company = row["Company"]
        year = row["Year"]
        temporal_mode = "real_time" if year == current_year else "retrospective"

        # Resolve contextual layer (priority: Company+Year > Year > global)
        context_payload = {}
        if (company, year) in external_context:
            context_payload = external_context[(company, year)]
        elif year in external_context:
            context_payload = external_context[year]
        elif "global" in external_context:
            context_payload = external_context["global"]

        record = {
            "Company": company,
            "Year": year,
            "analysis_profile": analysis_profile,
            "temporal_mode": temporal_mode,
            "context": context_payload,  # LLM uses this
            "ratios": {k: row[k] for k in row.index if k not in ("Company", "Year")},
            "trend": extract_engine_payload(outputs.get("trend", []), company, year),
            "cash_flow": extract_engine_payload(outputs.get("cash_flow", []), company, year),
            "anomaly": extract_engine_payload(outputs.get("anomaly", []), company, year),
            "solvency": extract_engine_payload(outputs.get("solvency", []), company, year),
            "composite_risk": extract_engine_payload(outputs.get("composite_risk", []), company, year)
        }

        structured_records.append(record)

    # ------------------------------------------------------------------
    # LLM Interpretation
    # ------------------------------------------------------------------
    if use_mock_ai:
        outputs["ai_interpretation"] = [
            {
                "Company": r["Company"],
                "Year": r["Year"],
                "analysis_profile": r["analysis_profile"],
                "temporal_mode": r["temporal_mode"],
                "interpretation": "MOCK"
            }
            for r in structured_records
        ]
    else:
        outputs["ai_interpretation"] = afap_llm_interpretation(
            structured_records,
            model="gpt-5-mini"
        )

    # ------------------------------------------------------------------
    # Profile Used
    # ------------------------------------------------------------------
    outputs["profile_used"] = analysis_profile

    return outputs