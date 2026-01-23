def composite_risk_engine(
    trend_results,
    cash_results,
    anomaly_results,
    solvency_results,
    config
):
    def index(results):
        return {(r["Company"], r["Year"]): r for r in results}

    t = index(trend_results)
    c = index(cash_results)
    a = index(anomaly_results)
    s = index(solvency_results)

    analysis_cfg = config["analysis"]
    weights = analysis_cfg["risk_weights"]
    bands = analysis_cfg["risk_bands"]

    rows = []

    for key in t.keys():
        score = 0

        if c.get(key, {}).get("severity") == "watch":
            score += weights["cash_flow"]

        if a.get(key, {}).get("severity") == "high":
            score += weights["anomaly"]

        if s.get(key, {}).get("severity") == "action":
            score += weights["solvency"]

        if t.get(key, {}).get("severity") == "watch":
            score += weights["trend"]

        if score >= bands["high"]:
            band = "high"
        elif score >= bands["medium"]:
            band = "medium"
        else:
            band = "low"

        rows.append({
            "Company": key[0],
            "Year": key[1],
            "composite_score": score,
            "risk_band": band
        })

    return rows
