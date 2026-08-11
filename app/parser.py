import json
import re


def extract_json(text):
    """
    Extract a JSON object from an LLM response.

    Handles:
    1. Pure JSON
    2. JSON inside ```json ... ```
    3. JSON surrounded by normal text
    """

    if not text or not isinstance(text, str):
        raise ValueError("Judge response is empty or invalid.")

    text = text.strip()

    # 1. Try parsing the complete response first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # 2. Look for JSON inside a Markdown code block
    code_block_pattern = r"```(?:json)?\s*(.*?)\s*```"

    matches = re.findall(
        code_block_pattern,
        text,
        flags=re.DOTALL | re.IGNORECASE
    )

    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue

    # 3. Look for a JSON object inside surrounding text
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and start < end:
        candidate = text[start:end + 1]

        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            pass

    raise ValueError(
        "Could not extract valid JSON from judge response."
    )