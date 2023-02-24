import json
import logging

from api import DragonApi
from utils import get_dynamodb_table
from validators import DragonValidator

table = get_dynamodb_table()

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


def lambda_handler(event, context):
    api = DragonApi(table, DragonValidator())
    method = event.get("httpMethod")
    resource = event.get("resource")
    logger.debug(event)

    if method == "GET" and resource == "/dragons":
        return api.get_dragons(event.get("queryStringParameters") or {})
    if method == "GET" and resource == "/dragons/{dragon_id}":
        return api.get_dragon(event.get("pathParameters"))
    if method == "POST" and resource == "/dragons":
        body = json.loads(event.get("body"))
        return api.create_dragon(body, api.get_username(event))

    if method == "DELETE" and resource == "/dragons/{dragon_id}":
        return api.delete_dragon(event.get("pathParameters"), api.get_username(event))

    if method == "PATCH" and resource == "/dragons/{dragon_id}":
        body = json.loads(event.get("body"))
        return api.update_dragon(
            event.get("pathParameters"), body, api.get_username(event)
        )
    return api.method_not_allowed()
