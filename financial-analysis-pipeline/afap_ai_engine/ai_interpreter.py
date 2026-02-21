from openai import OpenAI
from afap_ai_engine.prompt_builder import build_afap_prompt
import unicodedata

client = OpenAI()


def afap_llm_interpretation(
    structured_records,
    model="gpt-5-mini",
):
    """
    Wraps OpenAI API call for AFAP interpretation.

    Expected structure per record:
    {
        "Company": str,
        "Year": int,
        "financials": {...},
        "analysis_profile": str | None,
        "temporal_mode": str | None,
        "context": {
            "macro": {...},
            "industry": {...},
            "event_flags": {...}
        }
    }

    Returns:
        List[dict] — one interpretation per record
    """

    interpretations = []

    for record in structured_records:

        # Ensure structured context exists (avoid KeyError downstream)
        record.setdefault("context", {})
        record.setdefault("analysis_profile", None)
        record.setdefault("temporal_mode", None)

        # 🔑 Unified prompt builder handles ALL interpretation logic
        messages = build_afap_prompt(record)

        response = client.responses.create(
            model=model,
            input=messages
        )

        # -------------------------------
        # CLEAN AND NORMALIZE OUTPUT
        # -------------------------------
        raw_text = response.output_text
        clean_text = unicodedata.normalize("NFKD", raw_text)
        clean_text = clean_text.encode("utf-8", "ignore").decode("utf-8")

        # -------------------------------
        # APPEND INTERPRETATION
        # -------------------------------
        interpretations.append({
            "Company": record.get("Company"),
            "Year": record.get("Year"),
            "analysis_profile": record.get("analysis_profile"),
            "temporal_mode": record.get("temporal_mode"),
            "context_used": record.get("context"),
            "interpretation": clean_text
        })

    return interpretations