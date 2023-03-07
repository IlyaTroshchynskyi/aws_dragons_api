import json
import logging
import os
from datetime import datetime

from utils import json_response, get_event_client, is_danger_rating_changed

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

event_client = get_event_client()


def lambda_handler(event, context) -> dict:
    """
    Take events from dynamodb stream and send event to Event Bridge service.
    EventBusName must be created.
    Source is like condition in event rule. If source equal to source in the EventPattern
    then event bridge will trigger next lambda function.
    The first event will be sent to lambda which create statistics

    The second Event bridge rule has condition based on value of danger_rating. If danger_rating > 6 then
    event bridge send event to lambda function which send notification to SNS topic
    """
    logger.debug(event)
    entry = {
        "Time": datetime.now(),
        "Source": os.environ.get("SOURCE_STREAM_HANDLER"),
        "DetailType": "Dynamodb stream data",
        "Detail": json.dumps(event),
        "EventBusName": os.environ.get("EVENT_BUS_NAME"),
    }
    try:
        response = event_client.put_events(
            Entries=[
                entry,
            ]
        )
        logger.debug(response)

        entry["Source"] = os.environ.get("SOURCE_DANGER_DRAGON")
        for event in event.get("Records"):
            if event.get("eventName") in (
                "MODIFY",
                "INSERT",
            ) and is_danger_rating_changed(event):
                record = event.get("dynamodb")
                entry["Detail"] = json.dumps(
                    {
                        "dragon_id": record.get("Keys").get("dragon_id").get("S"),
                        "danger_rating": int(
                            record.get("NewImage").get("danger_rating").get("N")
                        ),
                    }
                )
                response = event_client.put_events(
                    Entries=[
                        entry,
                    ]
                )
                logger.debug(response)
    except Exception as error:
        logger.error(error)
    return json_response({"response": "Events were send"}, 200)
