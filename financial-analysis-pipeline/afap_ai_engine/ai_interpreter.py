from openai import OpenAI
from afap_ai_engine.prompt_builder import build_afap_prompt  # optional, can inline if you want

# Use environment variable for API key
client = OpenAI()

def afap_llm_interpretation(structured_records, model="gpt-5-mini", temperature=0.2, analysis_profile=None):
    """
    Wraps OpenAI API call for AFAP interpretation.
    Returns a list of dicts: one per record
    """
    interpretations = []

    for record in structured_records:
        # Build prompt (you can inline your notebook prompt logic here)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a conservative financial analyst producing professional, "
                    "client-facing audit-grade reports. "
                    "Use cautious language. Do not speculate. "
                    "Do not invent metrics, trends, or assumptions."
                )
            },
            {
                "role": "user",
                "content": (
                    f"ANALYSIS PROFILE:\n{analysis_profile}\n\n"
                    f"COMPANY: {record['Company']}\nYEAR: {record['Year']}\n\n"
                    f"RATIOS:\n" +
                    "\n".join([f"- {k}: {v}" for k, v in record["ratios"].items()]) + "\n\n"
                    f"COMPOSITE RISK:\n" +
                    "\n".join([f"- {k}: {v}" for k, v in record.get("composite_risk", {}).items()]) + "\n\n"
                    "RULES:\n"
                    "- Follow the output schema exactly\n"
                    "- Explicitly highlight metrics exceeding conservative thresholds\n"
                    "- Use audit-appropriate language\n"
                    "- Do not invent metrics, ratios, or trends\n\n"
                    "OUTPUT SCHEMA:\n"
                    "- summary\n"
                    "- key_risks\n"
                    "- recommendations\n"
                    "- confidence_notes"
                )
            }
        ]

        response = client.responses.create(
            model=model,
            reasoning={"effort": "low"},
            input=messages
        )

        interpretations.append({
            "Company": record["Company"],
            "Year": record["Year"],
            "analysis_profile": record.get("analysis_profile"),
            "interpretation": response.output_text
        })

    return interpretations
