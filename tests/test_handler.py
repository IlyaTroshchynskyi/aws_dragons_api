import json
import os

import requests

from .utils import create_invoke_command


def test_get_dragons(create_test_table, create_dragon):
    response = requests.get("http://127.0.0.1:3000/dragons")
    assert response.status_code == 200
    assert response.json() == [create_dragon[0], create_dragon[3], create_dragon[2]]


def test_create_dragon(create_test_table, base_dir):
    command = create_invoke_command(base_dir, "DragonFunction", "create_dragon_data")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 201
    assert body.get("dragon_id")
    assert body.get("created_at")
    assert body.get("name") == "Carl Junior1_test"
    assert body.get("breed") == "Standard Western Dragon"
    assert body.get("danger_rating") == 5
    assert body.get("description") == "Cute dragon that eats babies"
    assert body.get("username") == "1"


def test_get_dragon(create_test_table, create_dragon):
    response = requests.get(
        f"http://127.0.0.1:3000/dragons/{create_dragon[0].get('dragon_id')}"
    )
    assert response.status_code == 200
    assert response.json() == create_dragon[0]


def test_delete_dragon(create_test_table, create_dragon, base_dir):
    command = create_invoke_command(base_dir, "DragonFunction", "delete_dragon_data")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 204
    assert body == {"message": "Dragon is deleted"}


def test_delete_dragon_not_owner(create_test_table, create_dragon, base_dir):
    command = create_invoke_command(base_dir, "DragonFunction", "delete_dragon_not_owner_data")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 404
    assert body == {"message": "dragon is not found or user is not owner of dragon"}


def test_update_dragon(create_test_table, create_dragon, base_dir):
    command = create_invoke_command(base_dir, "DragonFunction", "update_dragon_data")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 200
    assert body == {"message": "Dragon is updated"}
    response = requests.get(
        f"http://127.0.0.1:3000/dragons/{create_dragon[0].get('dragon_id')}"
    )
    body = response.json()
    assert body.get("name") == "Carl Updated"
    assert body.get("danger_rating") == 9
    assert body.get("breed") == "Updated"
    assert body.get("dragon_id") == "1"
    assert body.get("username") == "1"


def test_update_dragon_not_owner(create_test_table, create_dragon, base_dir):
    command = create_invoke_command(base_dir, "DragonFunction", "update_dragon_not_owner_data")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 404
    assert body == {"message": "dragon is not found or user is not owner of dragon"}


def test_create_not_valid_dragon(create_test_table, create_dragon, base_dir):
    command = create_invoke_command(base_dir, "DragonFunction", "create_not_valid_dragon")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 400
    assert body == {
        "message": [
            {"message": "Name attribute must have length between 3 and 100"},
            {"message": "Breed attribute must have length between 5 and 150"},
            {"message": "Danger rating must be integer or between 0 and 10"},
        ]
    }


def test_update_not_valid_dragon(create_test_table, create_dragon, base_dir):
    command = create_invoke_command(base_dir, "DragonFunction", "update_not_valid_dragon")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 400
    assert body == {
        "message": [
            {"message": "Name attribute must have length between 3 and 100"},
            {"message": "Breed attribute must have length between 5 and 150"},
            {"message": "Danger rating must be integer or between 0 and 10"},
        ]
    }


def test_get_dragons_with_pagination(create_test_table, create_dragon):
    response = requests.get("http://127.0.0.1:3000/dragons?LastEvaluatedKey=4")
    assert response.status_code == 200
    assert response.json() == [create_dragon[2], create_dragon[1]]


def test_get_dragons_with_breed_filter(create_test_table, create_dragon):
    response = requests.get("http://127.0.0.1:3000/dragons?breed=3")
    assert response.status_code == 200
    assert response.json() == [create_dragon[3], create_dragon[2]]


def test_get_dragons_with_breed_filter_and_pagination(create_test_table, create_dragon):
    response = requests.get("http://127.0.0.1:3000/dragons?LastEvaluatedKey=4&breed=3")
    assert response.status_code == 200
    assert response.json() == [create_dragon[2]]
