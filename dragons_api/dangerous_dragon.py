import json
import logging
import os

from utils import json_response, get_sns_client

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

sns_client = get_sns_client()


def lambda_handler(event, context) -> dict:
    """
    Push email notification to user who is subscribed on topic if dragon was added pr modified
    with danger_rating > 6
    """
    logger.debug(event)
    response = sns_client.publish(
        TopicArn=os.environ["SNS_TOPIC_ARN"],
        Message=json.dumps(event.get("detail")),
        Subject="Dangerous Dragon",
    )
    logger.debug(response)
    return json_response({"response": response}, 200)
