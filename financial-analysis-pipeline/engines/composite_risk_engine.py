def composite_risk_engine(
    ratio_results,
    trend_results,
    cashflow_results,
    anomaly_results,
    solvency_results,
    weights=None
):
    """
    Produces a composite risk score per Company-Year
    """

    if weights is None:
        weights = {
            "ratios": 0.20,
            "trends": 0.15,
            "cashflow": 0.25,
            "anomalies": 0.20,
            "solvency": 0.20
        }

    results = []

    # Index results by Company-Year
    def index_results(data):
        return {
            (r["Company"], r["Year"]): r
            for r in data
        }

    ratio_idx = index_results(ratio_results)
    trend_idx = index_results(trend_results)
    cashflow_idx = index_results(cashflow_results)
    anomaly_idx = index_results(anomaly_results)
    solvency_idx = index_results(solvency_results)

    keys = set(
        ratio_idx.keys()
        & trend_idx.keys()
        & cashflow_idx.keys()
        & anomaly_idx.keys()
        & solvency_idx.keys()
    )

    for company, year in keys:
        score = 0
        components = {}

        # --- Ratios ---
        ratio_status = ratio_idx[(company, year)].get("status", "normal")
        ratio_score = 1 if ratio_status == "weak" else 0
        components["ratios"] = ratio_score
        score += ratio_score * weights["ratios"]

        # --- Trends ---
        trend_flags = trend_idx[(company, year)].get("trend_flags", {})
        trend_score = sum(trend_flags.values()) / max(len(trend_flags), 1)
        components["trends"] = trend_score
        score += trend_score * weights["trends"]

        # --- Cash Flow ---
        cf_status = cashflow_idx[(company, year)].get("cashflow_health", "healthy")
        cf_score = 1 if cf_status == "weak" else 0
        components["cashflow"] = cf_score
        score += cf_score * weights["cashflow"]

        # --- Anomalies ---
        anomaly_sev = anomaly_idx[(company, year)].get("severity", "normal")
        anomaly_score = 1 if anomaly_sev == "high" else 0.5 if anomaly_sev == "watch" else 0
        components["anomalies"] = anomaly_score
        score += anomaly_score * weights["anomalies"]

        # --- Solvency ---
        solvency_risk = solvency_idx[(company, year)].get("risk_level", "low")
        solvency_score = 1 if solvency_risk == "high" else 0.5 if solvency_risk == "medium" else 0
        components["solvency"] = solvency_score
        score += solvency_score * weights["solvency"]

        # Normalize to 0–100
        final_score = round(score * 100, 1)

        if final_score >= 70:
            tier = "High Risk"
        elif final_score >= 40:
            tier = "Moderate Risk"
        else:
            tier = "Low Risk"

        results.append({
            "engine": "composite_risk_engine",
            "Company": company,
            "Year": year,
            "risk_score": final_score,
            "risk_tier": tier,
            "components": components
        })

    return results
