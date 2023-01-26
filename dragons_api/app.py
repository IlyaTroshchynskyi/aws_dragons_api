import json
import logging
import os

import boto3

from api import DragonApi


if int(os.environ.get("AWS_SAM_LOCAL", "")):
    ddb = boto3.resource(
        "dynamodb", endpoint_url=os.environ.get("DYNAMODB_ENDPOINT", "test")
    )
else:
    ddb = boto3.resource("dynamodb")
table = ddb.Table(os.environ["TABLE_NAME"])

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def lambda_handler(event, context):
    api = DragonApi(table)
    method = event.get("httpMethod")
    resource = event.get("resource")
    if method == "GET" and resource == "/dragons":
        logger.debug(event)
        return api.get_dragons()
    if method == "POST" and resource == "/dragons":
        body = json.loads(event.get("body"))
        return api.create_dragon(body)
