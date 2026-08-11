import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()

@dataclass
class Settings:
    generator_api_key: str
    judge_api_key: str

    generator_model: str
    judge_model: str

    generator_temperature: float
    judge_temperature: float

    max_retries: int


def load_settings() -> Settings:
    generator_api_key = os.getenv("GENERATOR_API_KEY")
    judge_api_key = os.getenv("JUDGE_API_KEY")

    if not generator_api_key:
        raise ValueError("GENERATOR_API_KEY is missing from .env")

    if not judge_api_key:
        raise ValueError("JUDGE_API_KEY is missing from .env")

    return Settings(
        generator_api_key=generator_api_key,
        judge_api_key=judge_api_key,
        generator_model=os.getenv(
            "GENERATOR_MODEL",
            "gpt-5.6-luna"
        ),
        judge_model=os.getenv(
            "JUDGE_MODEL",
            "gpt-5.6-luna"
        ),
        generator_temperature=float(
            os.getenv("GENERATOR_TEMPERATURE", "0")
        ),
        judge_temperature=float(
            os.getenv("JUDGE_TEMPERATURE", "0")
        ),
        max_retries=int(
            os.getenv("MAX_RETRIES", "2")
        ),
    )