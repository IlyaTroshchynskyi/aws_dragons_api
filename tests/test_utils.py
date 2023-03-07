from decimal import Decimal

from dragons_api.utils import json_response, is_danger_rating_changed


def test_json_response():
    data = {"name": "Carl Junior1", "danger_rating": Decimal("5")}
    result = json_response(data)
    assert result.get("statusCode") == 200
    assert result.get("body") == '{"name": "Carl Junior1", "danger_rating": 5}'


def test_is_danger_rating_changed():
    data = {
        "eventName": "MODIFY",
        "dynamodb": {
            "Keys": {"dragon_id": {"S": "102"}},
            "NewImage": {"danger_rating": {"N": "8"}},
            "OldImage": {"danger_rating": {"N": "7"}},
        },
    }
    assert is_danger_rating_changed(data) is True
