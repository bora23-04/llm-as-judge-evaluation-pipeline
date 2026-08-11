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


configurations
Add cost and token tracking
