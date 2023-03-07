import pytest

from dragons_api.validators import DragonValidator

data_1 = {
    "name": "Jacob",
    "breed": "Standard Western Dragon",
    "danger_rating": 5,
    "description": "Cute dragon that eats babies",
}

data_2 = {
    "name1": "Jacob",
    "breed": "Standard Western Dragon",
    "danger_rating": 5,
    "description": "Cute dragon that eats babies",
}

data_3 = {"name": "Ja"}
data_4 = {"breed": "St"}
data_5 = {"danger_rating": "5"}
data_6 = {
    "name": "Jacob",
    "breed": "Standard Western Dragon",
    "danger_rating": "5",
    "description": "Cute dragon that eats babies",
}


@pytest.mark.parametrize(
    "data, expected_result",
    [
        (data_1, True),
        (data_2, {"message": "Extra name1 is present in request"}),
        (data_3, [{"message": "Name attribute must have length between 3 and 100"}]),
        (data_4, [{"message": "Breed attribute must have length between 5 and 150"}]),
        (data_5, [{"message": "Danger rating must be integer or between 0 and 10"}]),
        (data_6, [{"message": "Danger rating must be integer or between 0 and 10"}]),
    ],
)
def test_validate_dragon(data, expected_result):
    assert DragonValidator().validate_dragon(data) == expected_result
