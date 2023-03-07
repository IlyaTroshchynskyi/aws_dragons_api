import json
import os
from decimal import Decimal

import boto3
from botocore.config import Config


def is_develop() -> bool:
    """
    Define if we run lambda functions in dev or prod environment
    """
    return os.environ["AWS_SAM_LOCAL"] == "dev"


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        Serialize Decimal object
        """
        if isinstance(obj, Decimal):
            return int(obj)
        return super().default(obj)


def json_response(data, response_code=200) -> dict:
    """
    Build response for lambda functions
    """
    return {"statusCode": response_code, "body": json.dumps(data, cls=DecimalEncoder)}


def get_update_params(data: dict) -> tuple:
    """
    Given a dictionary of key-value pairs to update an item with in DynamoDB,
    generate three objects to be passed to UpdateExpression, ExpressionAttributeValues,
    and ExpressionAttributeNames respectively.
    """
    update_expression = []
    attribute_values = {}
    attribute_names = {}

    for key, value in data.items():
        update_expression.append(f" #{key.lower()} = :{key.lower()}")
        attribute_values[f":{key.lower()}"] = value
        attribute_names[f"#{key.lower()}"] = key.lower()

    return "set " + ", ".join(update_expression), attribute_values, attribute_names


def get_s3_client():
    """
    Initializes s3 client
    """
    if is_develop():
        s3_client = boto3.client(
            "s3",
            endpoint_url=os.environ.get("AWS_S3_ENDPOINT_URL", ""),
            config=Config(signature_version="s3v4"),
            aws_access_key_id=os.environ.get("ACCESS_KEY_ID", ""),
            aws_secret_access_key=os.environ.get("SECRET_ACCESS_KEY", ""),
        )
    else:
        s3_client = boto3.client("s3", config=Config(signature_version="s3v4"))
    return s3_client


def get_dynamodb_table(table_name: str):
    """
    Initializes dynamodb table
    """
    if is_develop():
        ddb = boto3.resource(
            "dynamodb",
            endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", "test"),
        )
    else:
        ddb = boto3.resource("dynamodb")

    table = ddb.Table(table_name)
    return table


def get_event_client():
    """
    Initializes data bridge event client
    """
    if is_develop():
        client = boto3.client(
            "events", endpoint_url=os.environ.get("EVENT_BRIDGE_ENDPOINT")
        )
    else:
        client = boto3.client("events")
    return client


def get_sns_client():
    """
    Initializes sns client
    """
    if is_develop():
        sns_client = boto3.client(
            "sns", endpoint_url=os.environ.get("SNS_TOPIC_ENDPOINT")
        )
    else:
        sns_client = boto3.client("sns")
    return sns_client


def is_danger_rating_changed(data: dict) -> bool:
    """
    Compare old and new danger rating
    """
    new_danger_rating = (
        data.get("dynamodb").get("NewImage").get("danger_rating").get("N")
    )
    old_danger_rating = (
        data.get("dynamodb").get("OldImage", {}).get("danger_rating", {}).get("N", "-")
    )
    return not new_danger_rating == old_danger_rating
