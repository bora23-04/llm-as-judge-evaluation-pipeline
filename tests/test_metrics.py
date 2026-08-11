from app.metrics import calculate_position_flip_rate


def test_position_flip_rate():

    results = [
        {
            "case_id": "q01",
            "position_flip": False
        },
        {
            "case_id": "q02",
            "position_flip": True
        },
        {
            "case_id": "q03",
            "position_flip": False
        },
        {
            "case_id": "q04",
            "position_flip": True
        }
    ]

    result = calculate_position_flip_rate(results)

    assert result == 0.5