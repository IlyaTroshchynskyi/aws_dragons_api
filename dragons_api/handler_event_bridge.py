import logging
import os
import time
import uuid
from enum import Enum

from utils import json_response, get_dynamodb_table

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

table_name = os.environ["STATISTICS_TABLE_NAME"]
table = get_dynamodb_table(table_name)


def lambda_handler(event: dict, context) -> dict:
    """
    Take event from EventBridge. Parse that event and save statistic information to dynamodb table
    based on the dynamodb action. Dynamo db has ttl 24 hours. Take note that
    ttl does not work straightaway. This feature can delete records through some time.
    """
    logger.debug(event)
    dragon_ttl = int(float(os.environ.get("TIME_TO_LIVE")) * 60 * 60) + int(time.time())
    records = event.get("detail").get("Records")
    for record in records:
        event_name = record.get("eventName")
        if event_name == DbAction.INSERT.value:
            put_dragon_statistics(dragon_ttl, DbAction.INSERT.value)
        elif event_name == DbAction.MODIFY.value:
            put_dragon_statistics(dragon_ttl, DbAction.MODIFY.value)
        elif event_name == DbAction.REMOVE.value:
            put_dragon_statistics(dragon_ttl, DbAction.REMOVE.value)

    return json_response({"response": records}, 200)


def put_dragon_statistics(dragon_ttl: int, dragon_action):
    """
    Insert new record to dynamodb
    """
    data = {
        "record_id": str(uuid.uuid4()),
        "dragon_ttl": dragon_ttl,
        "dragon_action": dragon_action,
    }
    logger.debug(data)
    table.put_item(Item=data)


class DbAction(Enum):
    INSERT = "INSERT"
    MODIFY = "MODIFY"
    REMOVE = "REMOVE"
