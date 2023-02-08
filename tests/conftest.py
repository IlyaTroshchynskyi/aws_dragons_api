from datetime import datetime
import boto3
import pytest


@pytest.fixture(scope="function")
def create_test_table():
    client = boto3.client("dynamodb", endpoint_url="http://localhost:8000")
    client.create_table(
        AttributeDefinitions=[
            {"AttributeName": "dragon_id", "AttributeType": "S"},
        ],
        TableName="dragons_test_table",
        KeySchema=[
            {"AttributeName": "dragon_id", "KeyType": "HASH"},
        ],
        BillingMode="PAY_PER_REQUEST",
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    yield
    client.delete_table(TableName="dragons_test_table")


@pytest.fixture(scope="function")
def create_dragon(create_test_table):

    data = {
        "dragon_id": "1",
        "created_at": str(datetime.now()),
        "name": "Test name",
        "breed": "Standard Western Dragon",
        "danger_rating": 4,
        "description": "Cute dragon that eats babies",
        "username": "1",
    }
    ddb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
    table = ddb.Table("dragons_test_table")
    table.put_item(Item=data)
    yield data
