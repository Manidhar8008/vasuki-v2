def mentor_response(query: str) -> dict:
    return {
        "tool": "mentor",
        "query": query,
        "method": [
            "Define the target skill or outcome",
            "Identify current level and missing prerequisites",
            "Choose one focused exercise",
            "Review output and extract mistakes",
            "Repeat with a harder exercise"
        ],
        "next_question": "What exact outcome do you want to achieve first?"
    }
