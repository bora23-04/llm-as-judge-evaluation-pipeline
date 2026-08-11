from app.parser import extract_json


def test_extract_json():
    text = """
    {
        "winner": "A",
        "score": 5
    }
    """

    result = extract_json(text)

    assert result["winner"] == "A"
    assert result["score"] == 5