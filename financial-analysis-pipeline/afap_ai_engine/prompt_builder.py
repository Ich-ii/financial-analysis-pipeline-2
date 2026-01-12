def build_afap_prompt(structured_record: dict) -> list[dict]:
    """
    Builds OpenAI-compatible messages for AFAP interpretation.
    No API calls here. Pure prompt logic.
    """

    ratios = structured_record["ratios"]
    composite = structured_record.get("composite_risk", {})
    profile = structured_record.get("analysis_profile", "full_diagnostic")

    system_message = {
        "role": "system",
        "content": (
            "You are a conservative financial analyst producing professional, "
            "client-facing, audit-grade reports. "
            "Use cautious language. Do not speculate. "
            "Do not invent metrics, trends, or assumptions."
        )
    }

    user_message = {
        "role": "user",
        "content": (
            f"ANALYSIS PROFILE:\n{profile}\n\n"

            f"COMPANY:\n{structured_record['Company']}\n"
            f"YEAR:\n{structured_record['Year']}\n\n"

            "RATIOS:\n" +
            "\n".join([f"- {k}: {v}" for k, v in ratios.items()]) + "\n\n"

            "COMPOSITE RISK:\n" +
            "\n".join([f"- {k}: {v}" for k, v in composite.items()]) + "\n\n"

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

    return [system_message, user_message]
