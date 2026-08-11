import json

from app.bias import run_position_bias_test
from app.metrics import calculate_position_flip_rate


def load_suite(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


if __name__ == "__main__":

    cases = load_suite("data/test_suite.json")

    results = run_position_bias_test(cases)

    flip_rate = calculate_position_flip_rate(results)

    print("\nPosition Bias Results")
    print("=====================")

    for result in results:
        print(
            result["case_id"],
            "| A first:",
            result["ab_winner"],
            "| B first:",
            result["ba_winner"],
            "| flip:",
            result["position_flip"]
        )

    print(
        f"\nPosition flip rate: {flip_rate:.2%}"
    )