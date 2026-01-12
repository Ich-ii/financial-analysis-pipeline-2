# ai_engine/llm_local.py
from typing import List, Dict

def call_local_llm(records: List[Dict], profile: str = "full_diagnostic") -> List[Dict]:
    """
    Local deterministic LLM stub.
    Produces modular, profile-aware, audit-ready outputs.
    """

    outputs = []

    for rec in records:
        company = rec["Company"]
        year = rec["Year"]
        metrics = rec.get("ratios", {})
        trend = rec.get("trend", {})
        cash_flow = rec.get("cash_flow", {})
        anomaly = rec.get("anomaly", {})
        solvency = rec.get("solvency", {})
        composite = rec.get("composite_risk", {})

        # Identify threshold triggers (simple example, can extend with config thresholds)
        threshold_flags = {k: v for k, v in metrics.items() if v > 0.8}

        # Executive Summary
        executive_summary = (
            f"[{profile}] {company} ({year}) overview: "
            f"Composite risk score {composite.get('score',0)}, band {composite.get('band','low')}."
        )

        # Key Risks (only include if profile allows)
        key_risks = {}
        if profile in ["full_diagnostic", "solvency_focus", "risk_scan", "going_concern_screen"]:
            key_risks = {k: f"Value={v}, exceeds threshold" for k,v in threshold_flags.items()}

        # Opportunities
        opportunities = {}
        if profile in ["full_diagnostic", "liquidity_focus", "performance_focus"]:
            opportunities = {k: "Potential improvement opportunity based on trend." for k in trend.keys()}

        # Forward-Looking Scenarios
        forward_scenarios = {}
        if profile in ["full_diagnostic", "solvency_focus", "liquidity_focus"]:
            forward_scenarios = {
                "Best": "Positive trend growth continues.",
                "Likely": "Current trend persists.",
                "Worst": "Metrics deteriorate to trigger risk thresholds."
            }

        # Recommendations
        recommendations = {}
        if profile in ["full_diagnostic", "solvency_focus", "liquidity_focus", "going_concern_screen"]:
            for metric in threshold_flags.keys():
                recommendations[metric] = f"Monitor {metric}; take action if value > threshold."

        # Confidence Notes
        confidence_notes = {
            "composite": "High confidence",
            "trend": "Medium confidence",
            "anomaly": "Lower confidence due to irregular patterns"
        }

        # Assemble structured output
        explanation = {
            "Executive_Summary": executive_summary,
            "Key_Risks": key_risks,
            "Opportunities": opportunities,
            "Forward_Scenarios": forward_scenarios,
            "Recommendations": recommendations,
            "Confidence_Notes": confidence_notes
        }

        outputs.append({
            "Company": company,
            "Year": year,
            "analysis_profile": profile,
            "llm_explanation": explanation
        })

    return outputs
