# ai_engine/llm_interpreter.py
from typing import List, Dict
# Placeholder for real LLM client
# from ai_engine.llm_oracle import call_oracle_llm
# from ai_engine.llm_local import call_local_llm

def afap_llm_interpretation(engine_outputs: List[Dict], model="local") -> List[Dict]:
    results = []

    for record in engine_outputs:
        company = record["Company"]
        year = record["Year"]
        composite = record.get("composite_risk", {})

        # Simulated LLM output (replace with real LLM API call)
        explanation = f"{company} ({year}) has a risk score of {composite.get('score',0)}, band {composite.get('band','low')}."
        recommendations = "Monitor liquidity and ROA trends."

        results.append({
            "Company": company,
            "Year": year,
            "llm_explanation": explanation,
            "llm_recommendations": recommendations
        })

    return results
