import pandas as pd

def composite_risk_engine(
    trend_results,
    cash_results,
    anomaly_results,
    solvency_results
):
    def index(results):
        return {(r["Company"], r["Year"]): r for r in results}

    t = index(trend_results)
    c = index(cash_results)
    a = index(anomaly_results)
    s = index(solvency_results)

    rows = []

    keys = set(t) | set(c) | set(a) | set(s)

    for company, year in keys:
        score = 0

        if c.get((company, year), {}).get("flags", {}).get("severity") == "watch":
            score += 20

        if a.get((company, year), {}).get("severity") == "high":
            score += 20

        if s.get((company, year), {}).get("severity") == "action":
            score += 30

        band = "high" if score >= 50 else "medium" if score >= 25 else "low"

        rows.append({
            "Company": company,
            "Year": year,
            "composite_score": score,
            "risk_band": band
        })

    return rows
