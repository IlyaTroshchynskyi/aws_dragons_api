import json
import os
from pathlib import Path

import requests

BASE_DIR = Path(__file__).resolve().parent.parent


def test_get_lambda_handler(create_test_table, create_dragon):
    response = requests.get("http://127.0.0.1:3000/dragons")
    assert response.status_code == 200
    assert response.json() == [create_dragon]


def test_create_dragon(create_test_table):
    response = os.popen(
        f'sam local invoke "DragonFunction" -e {BASE_DIR}/events/create_dragon_data.json  '
        f"--template-file {BASE_DIR}/template.yaml "
        f"--env-vars {BASE_DIR}/env.json  "
        f"--docker-network dragons"
    )
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 201
    assert body.get("dragon_id")
    assert body.get("created_at")
    assert body.get("name") == "Carl Junior1_test"
    assert body.get("breed") == "Standard Western Dragon"
    assert body.get("danger_rating") == "5"
    assert body.get("description") == "Cute dragon that eats babies"
    assert body.get("username") == "1"
