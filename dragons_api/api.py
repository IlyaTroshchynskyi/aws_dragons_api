import logging
import uuid
from datetime import datetime

from botocore.exceptions import ClientError
from utils import json_response


logger = logging.getLogger("dragons")
logger.setLevel("DEBUG")


class DragonApi:
    def __init__(self, table):
        self.table = table

    def get_dragons(self) -> dict:
        """
        Get all dragons from db
        """
        dragons = self.table.scan()["Items"]
        return json_response(dragons)

    def create_dragon(self, data, username):
        """
        Create dragon if dragon not exists in table
        """
        data.update(
            {
                "dragon_id": str(uuid.uuid4()),
                "created_at": str(datetime.now()),
                "username": username,
            }
        )
        try:
            self.table.put_item(
                Item=data, ConditionExpression="attribute_not_exists(dragon_id)"
            )
            message = (data, 201)
        except ClientError as error:
            message = ("Item already exists", 400)
            logger.error(error)
        return json_response(*message)
