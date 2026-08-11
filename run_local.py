from app.runner import run_suite


if __name__ == "__main__":

    results = run_suite(
        "data/test_suite.json",
        "results/local_report.json"
    )

    print(f"Evaluated {len(results)} cases.")

    for result in results:
        print(
            result["case_id"],
            "→",
            result["parsed_verdict"]["overall_score"]
        )