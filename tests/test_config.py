from app.config import load_settings


def test_config():

    settings = load_settings()

    print(
        "Generator model:",
        settings.generator_model
    )

    print(
        "Judge model:",
        settings.judge_model
    )

    assert settings.generator_model
    assert settings.judge_model
