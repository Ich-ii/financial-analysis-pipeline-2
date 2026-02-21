from datetime import datetime


def build_afap_prompt(structured_record: dict) -> list[dict]:
    """
    Builds OpenAI-compatible messages for AFAP interpretation.
    Adds strict temporal discipline, structured analytical modes,
    and controlled contextual integration.
    """

    ratios = structured_record["ratios"]
    composite = structured_record.get("composite_risk", {})
    profile = structured_record.get("analysis_profile", "full_diagnostic")
    context = structured_record.get("context", {})

    analysis_year = structured_record["Year"]
    current_year = datetime.now().year
    years_gap = current_year - analysis_year

    temporal_mode = structured_record.get("temporal_mode")

    # ------------------------------
    # AUTO-DETECT TEMPORAL MODE
    # ------------------------------
    if not temporal_mode:
        temporal_mode = "real_time" if years_gap == 0 else "retrospective"

    # ------------------------------
    # TEMPORAL INSTRUCTIONS
    # ------------------------------
    if temporal_mode == "real_time":
        temporal_instruction = (
            "This analysis is based on current-year financial data. "
            "All findings must be written in present tense. "
            "Interpret metrics as current conditions. "
            "Provide forward-looking, risk-aware recommendations. "
            "Recommendations may be action-oriented."
        )

    elif temporal_mode == "retrospective":
        temporal_instruction = (
            f"This analysis is being conducted in {current_year} "
            f"on financial data from {analysis_year}. "
            "All findings must be written in past tense. "
            "Interpret metrics strictly as conditions that existed in that reporting year. "
            "Do not write as if advising current management. "
            "Do not use imperative language. "
            "Period-specific actions must be framed as actions that were appropriate at the time. "
            "Structural implications may discuss how risks could have evolved after the reporting year, "
            "but must remain analytical and non-speculative."
        )

    elif temporal_mode == "multi_year_evolution":
        temporal_instruction = (
            "This analysis forms part of a structured multi-year comparative review. "
            "Write in analytical tone. "
            "Focus on trajectory, persistence, and structural directionality. "
            "Do not speculate beyond the provided data. "
            "Do not invent trends not explicitly inferable from the record."
        )

    else:
        raise ValueError("Invalid temporal_mode provided.")

    # ------------------------------
    # CONTEXT INSTRUCTIONS
    # ------------------------------
    if context:
        context_block = "\n".join([f"- {k}: {v}" for k, v in context.items()])
        context_instruction = (
            "EXTERNAL CONTEXT (STRUCTURED AND EXPLICITLY PROVIDED):\n"
            f"{context_block}\n\n"
            "Context may be used only as explanatory backdrop. "
            "Do not assume additional macroeconomic, industry, or geopolitical factors "
            "beyond what is explicitly listed. "
            "Do not invent causal relationships. "
            "Financial metrics remain primary evidence. "
            "Context may explain signals but must not override metric-based analysis."
        )
    else:
        context_instruction = (
            "No external context has been provided. "
            "Do not introduce macroeconomic, industry, or geopolitical assumptions."
        )

    # ------------------------------
    # SYSTEM MESSAGE
    # ------------------------------
    system_message = {
        "role": "system",
        "content": (
            "You are a conservative financial analyst producing professional, "
            "client-facing, audit-grade reports. "
            "Use precise, cautious language. "
            "Do not speculate. "
            "Do not invent metrics, trends, assumptions, or external conditions. "
            "Do not imply access to data not provided. "
            "Financial metrics are primary evidence. "
            "Maintain strict temporal discipline. "
            "If contextual information is provided, treat it as structured backdrop only."
        )
    }

    # ------------------------------
    # OUTPUT SCHEMA
    # ------------------------------
    output_schema = (
        "- summary:\n"
        "    Concise diagnostic overview written in correct temporal tense.\n"
        "    Must clearly identify:\n"
        "    • overall financial condition\n"
        "    • dominant financial pressure (liquidity, solvency, profitability, structural, etc.)\n"
        "    • whether risk appears concentrated or multi-dimensional\n\n"

        "- key_risks:\n"
        "    Top 3–5 material risks ordered by severity.\n"
        "    Each risk must:\n"
        "    • explicitly reference supporting metrics\n"
        "    • explain the financial mechanism (how the metric creates risk)\n"
        "    • avoid external assumptions unless explicitly provided in structured context\n\n"

        "- period_specific_actions:\n"
        "    Actions that were appropriate in the reporting year only.\n"
        "    Each action must directly address a stated risk.\n"
        "    No generic improvement language.\n"
        "    No present-tense advisory language in retrospective mode.\n\n"

        "- structural_long_term_implications:\n"
        "    Analytical discussion of potential structural evolution strictly inferable from metric patterns.\n"
        "    May reference persistence, deterioration, stabilization, or structural shifts.\n"
        "    No speculative macroeconomic narratives.\n"
        "    No invented external conditions.\n\n"

        "- contextual_interpretation:\n"
        "    If structured external context was provided:\n"
        "    • explicitly state whether and how the provided context informs interpretation\n"
        "    • clarify whether risks are primarily metric-driven or context-amplified\n"
        "    • do not introduce new context beyond what was supplied\n"
        "    If no context was provided:\n"
        "    • explicitly state that interpretation is based solely on financial metrics\n\n"

        "- confidence_notes:\n"
        "    Explicitly state interpretive limitations, including:\n"
        "    • missing financial data\n"
        "    • metric scope limitations\n"
        "    • contextual constraints\n"
        "    • uncertainty in structural inference\n"
    )

    # ------------------------------
    # USER MESSAGE
    # ------------------------------
    user_message = {
        "role": "user",
        "content": (
            f"ANALYSIS PROFILE:\n{profile}\n\n"
            f"COMPANY:\n{structured_record['Company']}\n"
            f"ANALYSIS YEAR:\n{analysis_year}\n"
            f"CURRENT YEAR:\n{current_year}\n"
            f"TEMPORAL MODE:\n{temporal_mode}\n\n"
            f"TEMPORAL CONTEXT:\n{temporal_instruction}\n\n"
            f"{context_instruction}\n\n"
            "RATIOS:\n" +
            "\n".join([f"- {k}: {v}" for k, v in ratios.items()]) + "\n\n"
            "COMPOSITE RISK:\n" +
            "\n".join([f"- {k}: {v}" for k, v in composite.items()]) + "\n\n"
            "RULES:\n"
            "- Follow the output schema exactly\n"
            "- Tie every risk to explicit metric evidence\n"
            "- Do not restate ratios without interpretation\n"
            "- Financial metrics are primary evidence\n"
            "- Context may explain but must not replace metric-based reasoning\n"
            "- If context is provided, explicitly evaluate its influence\n"
            "- If context is not provided, confirm metric-only interpretation\n"
            "- Maintain strict temporal framing\n"
            "- Separate period-specific actions from structural implications\n\n"
            "OUTPUT SCHEMA:\n"
            f"{output_schema}"
        )
    }

    return [system_message, user_message]