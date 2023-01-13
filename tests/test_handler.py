import requests


def test_get_lambda_handler(create_test_table, create_dragon):
    response = requests.get("http://127.0.0.1:3000/dragons")
    assert response.status_code == 200
    assert response.json() == [create_dragon]


def test_create_dragon(create_test_table, monkeypatch):

    response = requests.post(
        "http://127.0.0.1:3000/dragons",
        json={
            "name": "Carl Junior_test",
            "breed": "Standard Western Dragon",
            "danger_rating": "4",
            "description": "Cute dragon that eats babies",
        },
    )
    assert response.status_code == 201
    assert response.json().get("dragon_id")
    assert response.json().get("created_at")
    assert response.json().get("name") == "Carl Junior_test"
    assert response.json().get("breed") == "Standard Western Dragon"
    assert response.json().get("danger_rating") == "4"
    assert response.json().get("description") == "Cute dragon that eats babies"

