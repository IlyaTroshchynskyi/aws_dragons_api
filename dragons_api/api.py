import logging
import uuid
from datetime import datetime
from typing import Union

from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from utils import json_response, get_update_params


logger = logging.getLogger("dragons")
logger.setLevel("DEBUG")


class DragonApi:
    def __init__(self, table, validators):
        self.table = table
        self.validators = validators

    def get_dragons(self, query_params:  Union[dict, None]) -> dict:
        """
        Get all dragons from db. User can paginate query using LastEvaluatedKey which
        equal the last dragon_id in query. Filter dragons using field "breed".
        Show 3 items per one query
        """
        scan_kwargs = {}
        if "LastEvaluatedKey" in query_params:
            scan_kwargs.update(
                {"ExclusiveStartKey": {"dragon_id": query_params["LastEvaluatedKey"]}}
            )
        if "breed" in query_params:
            scan_kwargs.update(
                {"FilterExpression": Attr("breed").eq(query_params.get("breed"))}
            )
        dragons = self.table.scan(Limit=3, **scan_kwargs)["Items"]
        return json_response(dragons)

    def get_dragon(self, key: dict) -> dict:
        """
        Get dragon using dragon id
        """
        dragon = self.table.get_item(Key=key).get("Item")
        if dragon:
            return json_response(dragon)
        return json_response({"message": "dragon fon found"}, 404)

    def create_dragon(self, data: dict, username: str) -> dict:
        """
        Create dragon if dragon not exists in table
        """
        valid = self.validators.validate_dragon(data)
        if valid is not True:
            return json_response({"message": valid}, 400)

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

    def delete_dragon(self, key: dict, username: str) -> dict:
        """
        Delete dragon if user is authorized and owner of dragon
        """
        try:
            self.table.delete_item(
                Key=key,
                ConditionExpression="username = :username",
                ExpressionAttributeValues={":username": username},
            )
            return json_response({"message": "Dragon is deleted"}, 204)
        except ClientError as error:
            logger.error(error)
        return json_response(
            {"message": "dragon is not found or user is not owner of dragon"}, 404
        )

    def update_dragon(self, key: dict, data: dict, username: str) -> dict:
        """
        Update dragon if user is authorized and owner of dragon
        """
        valid = self.validators.validate_dragon(data)
        if valid is not True:
            return json_response({"message": valid}, 400)

        update_expression, attribute_values, attribute_names = get_update_params(data)
        attribute_values.update({":username": username})
        try:
            self.table.update_item(
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=attribute_values,
                ExpressionAttributeNames=attribute_names,
                ConditionExpression="username = :username",
            )
            return json_response({"message": "Dragon is updated"}, 200)
        except ClientError as error:
            logger.error(error)
        return json_response(
            {"message": "dragon is not found or user is not owner of dragon"}, 404
        )

    @staticmethod
    def method_not_allowed():
        """
        Return response to users if user send wrong path or method
        """
        return json_response({"message": "Method or path not allowed"})

    @staticmethod
    def get_username(event: dict) -> str:
        """
        Get username from event object
        """
        return event.get("requestContext").get("authorizer").get("claims").get("sub")
