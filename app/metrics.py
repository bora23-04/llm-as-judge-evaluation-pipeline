import json
from pathlib import Path
from sklearn.metrics import cohen_kappa_score

def load_jsonl(path):
    results = []

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:
            if line.strip():
                results.append(
                    json.loads(line)
                )

    return results


def calculate_ab_results(results):
    a_wins = 0
    b_wins = 0
    ties = 0

    for result in results:
        winner = result[
            "parsed_verdict"
        ]["winner"]

        if winner == "A":
            a_wins += 1

        elif winner == "B":
            b_wins += 1

        else:
            ties += 1

    total = len(results)

    return {
        "total_cases": total,
        "A_wins": a_wins,
        "B_wins": b_wins,
        "ties": ties,
        "A_win_rate": (
            a_wins / total
            if total else 0
        ),
        "B_win_rate": (
            b_wins / total
            if total else 0
        ),
        "tie_rate": (
            ties / total
            if total else 0
        )
    }

def calculate_human_agreement(
    judge_labels,
    human_labels
):
    matches = sum(
        j == h
        for j, h in zip(
            judge_labels,
            human_labels
        )
    )

    total = len(human_labels)

    agreement = (
        matches / total
        if total
        else 0
    )

    mapping = {
        "A": 0,
        "B": 1,
        "tie": 2
    }

    judge_numeric = [
        mapping[x]
        for x in judge_labels
    ]

    human_numeric = [
        mapping[x]
        for x in human_labels
    ]

    kappa = cohen_kappa_score(
        human_numeric,
        judge_numeric
    )

    return {
        "agreement": agreement,
        "cohen_kappa": kappa,
        "matches": matches,
        "total": total
    }

def calculate_position_flip_rate(results):
    if not results:
        return 0.0

    flips = sum(
        1
        for result in results
        if result["position_flip"]
    )

    return flips / len(results)