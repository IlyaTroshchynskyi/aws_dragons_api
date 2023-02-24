import json
import logging
import os
from datetime import datetime

from utils import json_response, get_event_client

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

event_client = get_event_client()


def lambda_handler(event, context) -> dict:
    """
    Take events from dynamodb stream and send event to Event Bridge service.
    EventBusName bust be created.
    Source is like condition in event rule. If source equal to source in the EventPattern
    then event bridge will trigger next lambda function.
    """

    logger.debug(event)
    entry = {
        "Time": datetime.now(),
        "Source": os.environ.get("SOURCE"),
        "DetailType": "Dynamodb stream data",
        "Detail": json.dumps(event),
        "EventBusName": os.environ.get("EVENT_BUS_NAME"),
    }
    response = event_client.put_events(
        Entries=[
            entry,
        ]
    )
    logger.debug(response)

    return json_response({"response": response}, 200)
