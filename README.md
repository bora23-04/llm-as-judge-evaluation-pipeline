# LLM-as-Judge Evaluation Pipeline

An evaluation pipeline for structured model-output evaluation with A/B
comparison, position-bias testing, verbosity probes, and automated tests.

> **Note:** The submitted version uses a deterministic mock judge for offline
> validation because external LLM API credits were unavailable. The judge
> layer is separated so a real LLM judge can be connected later.

## Features

- JSON test-suite input
- Structured evaluation verdicts
- Explicit evaluation rubric
- JSON parsing with malformed-response handling
- A/B comparison
- Position-bias testing
- Verbosity/length probe
- Automated pytest tests
- JSON evaluation reports

## Architecture

```text
Test Suite (JSON)
       |
       v
Prompt Construction
       |
       v
Judge Layer
(Mock Judge)
       |
       v
JSON Parser
+ Fallback
       |
       v
Structured Verdict
       |
   +---+---+
   |       |
   v       v
A/B      Bias
Test     Tests
   |       |
   +---+---+
       |
       v
Suite Report

## Tech Stack
- Python 3.12
- pytest
- JSON
- python-dotenv

## Setup
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd llm-as-judge-evaluation-pipeline
pip install -r requirements.txt

## Run Tests
python -m pytest -v

## Run Evaluation
python run_local.py

## Bias Experiments
- Position-bias test:
python run_bias_test.py

- Verbosity test:
python run_verbosity_test.py

The position-bias test evaluates the same A/B pair in both orders and
calculates the resulting flip rate.

## Results

The current offline evaluation successfully processes 3 test cases and the
core automated tests pass.

The current results validate the evaluation pipeline and bias-testing
infrastructure.

They should not be interpreted as real-LLM bias measurements because the
submitted version uses a deterministic mock judge.

## Limitations

A live LLM judge was not connected because external API credits were
unavailable.

Therefore, real LLM measurements such as:

Human/LLM agreement
Cohen's kappa
Test-retest consistency
Real LLM position bias
Self-enhancement bias
Real LLM A/B comparison

are not claimed in this submission.

## Future Work
Connect a real LLM judge
Run human/gold validation
Measure judge consistency
Evaluate real position and verbosity bias
Compare different judge/model 
