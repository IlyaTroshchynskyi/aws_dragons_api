import os
from datetime import datetime
from pathlib import Path

import boto3
import pytest
from botocore.config import Config


@pytest.fixture(scope="function")
def env_vars():
    yield {
        "AWS_S3_ENDPOINT_URL": "http://localhost:9000",
        "AWS_ACCESS_KEY_ID": "access_key",
        "AWS_SECRET_ACCESS_KEY": "secret_key",
        "DYNAMODB_ENDPOINT": "http://127.0.0.1:8000",
        "AWS_S3_BUCKET_NAME": "dragonsapidev",
        "TABLE_NAME": "dragons_test_table",
        "STATISTICS_TABLE_NAME": "dragon_statistics_test_table",
        "EVENT_BRIDGE_ENDPOINT": "http://localhost:5000",
        "EVENT_BUS_NAME": "test_event_bus",
    }


@pytest.fixture(scope="function")
def base_dir():
    base_dir = Path(__file__).resolve().parent.parent
    yield base_dir


@pytest.fixture(scope="function")
def create_test_table(env_vars):
    client = boto3.client("dynamodb", endpoint_url=env_vars["DYNAMODB_ENDPOINT"])
    client.create_table(
        AttributeDefinitions=[
            {"AttributeName": "dragon_id", "AttributeType": "S"},
        ],
        TableName=env_vars["TABLE_NAME"],
        KeySchema=[
            {"AttributeName": "dragon_id", "KeyType": "HASH"},
        ],
        BillingMode="PAY_PER_REQUEST",
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    yield
    client.delete_table(TableName=env_vars["TABLE_NAME"])


@pytest.fixture(scope="function")
def dynamo_db_table(create_test_table, env_vars):
    ddb = boto3.resource("dynamodb", endpoint_url=env_vars["DYNAMODB_ENDPOINT"])
    table = ddb.Table(env_vars["TABLE_NAME"])
    yield table


@pytest.fixture(scope="function")
def create_dragon(create_test_table, dynamo_db_table):

    dragon_1 = {
        "dragon_id": "1",
        "created_at": str(datetime.now()),
        "name": "Test name",
        "breed": "Standard Western Dragon",
        "danger_rating": 4,
        "description": "Cute dragon that eats babies",
        "username": "1",
    }
    dragon_2 = {
        "dragon_id": "2",
        "created_at": str(datetime.now()),
        "name": "Test name",
        "breed": "2",
        "danger_rating": 4,
        "description": "Cute dragon that eats babies",
        "username": "100",
    }
    dragon_3 = {
        "dragon_id": "3",
        "created_at": str(datetime.now()),
        "name": "Test name",
        "breed": "3",
        "danger_rating": 4,
        "description": "Cute dragon that eats babies",
        "username": "1",
    }
    dragon_4 = {
        "dragon_id": "4",
        "created_at": str(datetime.now()),
        "name": "Test name",
        "breed": "3",
        "danger_rating": 4,
        "description": "Cute dragon that eats babies",
        "username": "1",
    }
    dynamo_db_table.put_item(Item=dragon_1)
    dynamo_db_table.put_item(Item=dragon_2)
    dynamo_db_table.put_item(Item=dragon_3)
    dynamo_db_table.put_item(Item=dragon_4)

    yield dragon_1, dragon_2, dragon_3, dragon_4


@pytest.fixture(scope="function")
def create_file_on_s3(base_dir, env_vars):
    s3_client = boto3.client(
        "s3",
        endpoint_url=env_vars["AWS_S3_ENDPOINT_URL"],
        config=Config(signature_version="s3v4"),
        aws_access_key_id=env_vars["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=env_vars["AWS_SECRET_ACCESS_KEY"],
    )
    bucket_name = env_vars["AWS_S3_BUCKET_NAME"]
    s3_client.create_bucket(ACL="public-read", Bucket=bucket_name)
    s3_client.upload_file(
        os.path.join(base_dir, "events/dragons.csv"), bucket_name, "dragons.csv"
    )
    yield
    s3_client.delete_object(Bucket=bucket_name, Key="dragons.csv")
    s3_client.delete_bucket(Bucket=bucket_name)


@pytest.fixture(scope="function")
def create_test_table_statistics(env_vars):
    client = boto3.client("dynamodb", endpoint_url=env_vars["DYNAMODB_ENDPOINT"])
    client.create_table(
        AttributeDefinitions=[
            {"AttributeName": "record_id", "AttributeType": "S"},
        ],
        TableName=env_vars["STATISTICS_TABLE_NAME"],
        KeySchema=[
            {"AttributeName": "record_id", "KeyType": "HASH"},
        ],
        BillingMode="PAY_PER_REQUEST",
        ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
    )
    client.update_time_to_live(
        TableName=env_vars["STATISTICS_TABLE_NAME"],
        TimeToLiveSpecification={"Enabled": True, "AttributeName": "dragon_ttl"},
    )
    yield
    client.delete_table(TableName=env_vars["STATISTICS_TABLE_NAME"])


@pytest.fixture(scope="function")
def dynamo_db_statistics_table(create_test_table_statistics, env_vars):
    ddb = boto3.resource("dynamodb", endpoint_url=env_vars["DYNAMODB_ENDPOINT"])
    table = ddb.Table(env_vars["STATISTICS_TABLE_NAME"])
    yield table


@pytest.fixture(scope="function")
def create_event_bus(env_vars):
    client = boto3.client("events", endpoint_url=env_vars["EVENT_BRIDGE_ENDPOINT"])

    client.create_event_bus(Name=env_vars["EVENT_BUS_NAME"])
    yield
    client.delete_event_bus(Name=env_vars["EVENT_BUS_NAME"])
