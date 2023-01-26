from decimal import Decimal

from dragons_api.utils import json_response


def test_json_response():
    data = {"name": "Carl Junior1", "danger_rating": Decimal("5")}
    result = json_response(data)
    assert result.get("statusCode") == 200
    assert result.get("body") == '{"name": "Carl Junior1", "danger_rating": "5"}'
