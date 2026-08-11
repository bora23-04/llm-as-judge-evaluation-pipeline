import json
import time
from pathlib import Path
from typing import Literal

from openai import OpenAI
from pydantic import BaseModel, Field

from app.config import load_settings
from app.parser import extract_json


# ============================================================
# 1. STRUCTURED JUDGE RESPONSE
# ============================================================

class ScorePair(BaseModel):
    A: int = Field(ge=1, le=5)
    B: int = Field(ge=1, le=5)


class JudgeVerdict(BaseModel):
    winner: Literal["A", "B", "tie"]

    correctness: ScorePair

    completeness: ScorePair

    instruction_following: ScorePair

    clarity: ScorePair

    overall_score: ScorePair

    rationale: str


# ============================================================
# 2. JUDGE SYSTEM PROMPT
# ============================================================

JUDGE_SYSTEM_PROMPT = """
You are an impartial LLM evaluator.

Your task is to compare Answer A and Answer B.

Evaluate both answers using the reference answer when one
is provided.

Evaluate these criteria:

1. Correctness
2. Completeness
3. Instruction following
4. Clarity

Scoring:

5 = excellent
4 = good
3 = acceptable with noticeable issues
2 = poor
1 = very poor

Important bias controls:

- Do not prefer an answer because it appears first.
- Do not reward verbosity by itself.
- Do not reward confidence by itself.
- Do not reward unnecessary detail.
- A concise answer can receive a 5 if it is correct and complete.
- Prioritize factual correctness over style.
- Do not assume a confident answer is correct.
- Evaluate each answer independently before selecting the winner.

Return ONLY a JSON object.

Required structure:

{
    "winner": "A",
    "correctness": {
        "A": 1,
        "B": 1
    },
    "completeness": {
        "A": 1,
        "B": 1
    },
    "instruction_following": {
        "A": 1,
        "B": 1
    },
    "clarity": {
        "A": 1,
        "B": 1
    },
    "overall_score": {
        "A": 1,
        "B": 1
    },
    "rationale": "Brief evidence-based explanation."
}

The winner must be exactly one of:

"A"
"B"
"tie"
"""


# ============================================================
# 3. BUILD THE JUDGE PROMPT
# ============================================================

def build_judge_prompt(
    question: str,
    reference: str,
    answer_a: str,
    answer_b: str
) -> str:

    return f"""
USER QUESTION:

{question}

REFERENCE ANSWER:

{reference}

ANSWER A:

{answer_a}

ANSWER B:

{answer_b}

Evaluate Answer A and Answer B using the rubric.

Important:

- Focus on factual correctness.
- Do not reward unnecessary length.
- Do not reward confidence.
- Follow the scoring criteria exactly.
"""


# ============================================================
# 4. CALL THE JUDGE MODEL
# ============================================================

def call_judge(
    client,
    model: str,
    question: str,
    reference: str,
    answer_a: str,
    answer_b: str
):

    prompt = build_judge_prompt(
        question,
        reference,
        answer_a,
        answer_b
    )

    start = time.perf_counter()

    response = client.responses.create(
        model=model,
        instructions=JUDGE_SYSTEM_PROMPT,
        input=prompt
    )

    latency = (
        time.perf_counter() - start
    ) * 1000

    usage = getattr(
        response,
        "usage",
        None
    )

    input_tokens = (
        getattr(
            usage,
            "input_tokens",
            0
        )
        if usage
        else 0
    )

    output_tokens = (
        getattr(
            usage,
            "output_tokens",
            0
        )
        if usage
        else 0
    )

    return {
        "prompt": prompt,

        "raw_response":
            response.output_text,

        "latency_ms":
            round(latency, 2),

        "input_tokens":
            input_tokens,

        "output_tokens":
            output_tokens,

        "total_tokens":
            input_tokens + output_tokens
    }


# ============================================================
# 5. RUN ONE JUDGMENT
# ============================================================

def run_single_judgment(
    client,
    model: str,
    question: str,
    reference: str,
    answer_a: str,
    answer_b: str
):

    raw_result = call_judge(
        client=client,
        model=model,
        question=question,
        reference=reference,
        answer_a=answer_a,
        answer_b=answer_b
    )

    parsed = extract_json(
        raw_result["raw_response"]
    )

    verdict = JudgeVerdict.model_validate(
        parsed
    )

    raw_result["parsed_verdict"] = (
        verdict.model_dump()
    )

    return raw_result


# ============================================================
# 6. MAIN JUDGE PIPELINE
# ============================================================

def main():

    settings = load_settings()

    client = OpenAI(
        api_key=settings.judge_api_key
    )

    input_file = Path(
        "results/generated_outputs.json"
    )

    output_file = Path(
        "results/raw_judgments.jsonl"
    )

    if not input_file.exists():

        print(
            f"ERROR: {input_file} "
            f"does not exist."
        )

        print(
            "Run the generator first."
        )

        return

    with open(
        input_file,
        "r",
        encoding="utf-8"
    ) as file:

        generated = json.load(file)

    results = []

    for item in generated:

        print(
            f"Judging {item['id']}..."
        )

        result = run_single_judgment(
            client=client,
            model=settings.judge_model,
            question=item["input"],
            reference=item["expected_output"],
            answer_a=item["A"]["text"],
            answer_b=item["B"]["text"]
        )

        result["id"] = item["id"]

        result["order"] = "AB"

        results.append(result)

    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        for result in results:

            file.write(
                json.dumps(
                    result,
                    ensure_ascii=False
                )
                + "\n"
            )

    print(
        f"\nSaved judgments to "
        f"{output_file}"
    )


# ============================================================
# 7. RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()

from app.parser import extract_json


def mock_judge_response(case):
    """
    Temporary mock judge.

    This is only for local testing.
    It does not use any API credits.
    """

    return """
    {
        "scores": {
            "correctness": 5,
            "completeness": 4,
            "instruction_following": 5
        },
        "overall_score": 4.67,
        "winner": "A",
        "rationale": "The answer is correct, relevant, and follows the instructions."
    }
    """


def judge_case(case):
    """
    Evaluate one test case using the mock judge.
    """

    raw_response = mock_judge_response(case)

    parsed_verdict = extract_json(raw_response)

    return {
        "case_id": case["id"],
        "raw_response": raw_response,
        "parsed_verdict": parsed_verdict
    }