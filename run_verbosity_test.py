import json

from app.verbosity import mock_verbosity_judge


def load_probe(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":

    cases = load_probe("data/verbosity_probe.json")

    results = []

    for case in cases:

        verdict = mock_verbosity_judge(case)

        results.append({
            "case_id": case["id"],
            "winner": verdict["winner"],
            "short_length": len(case["short_answer"]),
            "verbose_length": len(case["verbose_answer"])
        })

    print("\nVerbosity Bias Probe")
    print("====================")

    for result in results:

        print(
            result["case_id"],
            "| winner:",
            result["winner"],
            "| short chars:",
            result["short_length"],
            "| verbose chars:",
            result["verbose_length"]
        )