import json
import os
from urllib.parse import urlparse, parse_qs


import requests
from .utils import create_invoke_command


def test_generate_url_without_query_param():

    response = requests.get("http://127.0.0.1:3000/generate_url")
    assert response.status_code == 400
    assert response.json() == {
        "message": "User should set up query parameter for filename"
    }


def test_generate_url_with_query_param():

    response = requests.get("http://127.0.0.1:3000/generate_url?file_name=test.csv")
    url = response.json().get("url")
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    assert response.status_code == 200
    assert query_params["X-Amz-Algorithm"]
    assert query_params["X-Amz-Credential"]
    assert query_params["X-Amz-Date"]
    assert query_params["X-Amz-Expires"]
    assert query_params["X-Amz-SignedHeaders"]
    assert query_params["X-Amz-Signature"]
    assert str(url).startswith("http://localhost:9000/dragonsapidev/test.csv?")


def test_upload_to_db(dynamo_db_table, create_file_on_s3, base_dir):
    command = create_invoke_command(base_dir, "UploadDragonsToDynamoDb", "s3_put_event_data")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    result = dynamo_db_table.scan()
    assert result.get("Count") == 4
    assert data.get("statusCode") == 200
    assert body == {"message": "Numbers of rows are not valid: [3]"}
