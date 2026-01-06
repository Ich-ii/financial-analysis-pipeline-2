def composite_risk_engine(
    ratio_results,
    trend_results,
    cashflow_results,
    anomaly_results,
    solvency_results,
    client_config=None
):
    DEFAULT_WEIGHTS = {
        "ratio_engine": 0.25,
        "trend_engine": 0.20,
        "cash_flow_engine": 0.20,
        "anomaly_efficiency_engine": 0.20,
        "solvency_engine": 0.15
    }

    SEVERITY_MAP = {
        "stable": 0,
        "normal": 0,
        "low": 10,
        "watch": 30,
        "medium": 50,
        "high": 70,
        "action": 90
    }

    weights = DEFAULT_WEIGHTS.copy()
    if client_config and "risk_weights" in client_config:
        weights.update(client_config["risk_weights"])

    # --- Index all engine outputs ---
    all_engines = (
        ratio_results
        + trend_results
        + cashflow_results
        + anomaly_results
        + solvency_results
    )

    index = {}
    for r in all_engines:
        key = (r["Company"], r["Year"])
        index.setdefault(key, []).append(r)

    results = []

    for (company, year), records in index.items():
        total_score = 0
        total_weight = 0
        drivers = []

        breakdown = {}

        for r in records:
            engine = r["engine"]
            severity = r.get("severity") or r.get("flags", {}).get("severity", "normal")

            score = SEVERITY_MAP.get(severity, 0)
            weight = weights.get(engine, 0)

            weighted_score = score * weight

            breakdown[engine] = weighted_score
            total_score += weighted_score
            total_weight += weight

            if score >= 50:
                drivers.append(r["explanation"])

        normalized_score = round(total_score / total_weight, 1) if total_weight else 0

        if normalized_score >= 70:
            overall_risk = "high"
        elif normalized_score >= 40:
            overall_risk = "medium"
        else:
            overall_risk = "low"

        results.append({
            "engine": "composite_risk_engine",
            "Company": company,
            "Year": year,
            "overall_risk": overall_risk,
            "risk_score": normalized_score,
            "risk_breakdown": breakdown,
            "key_drivers": drivers
        })

    return results
