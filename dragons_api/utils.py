import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        Serialize Decimal object
        """
        if isinstance(obj, Decimal):
            return str(obj)
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
    attribute_values = dict()
    attribute_names = dict()

    for key, value in data.items():
        update_expression.append(f" #{key.lower()} = :{key.lower()}")
        attribute_values[f":{key.lower()}"] = value
        attribute_names[f"#{key.lower()}"] = key.lower()

    return "set " + ", ".join(update_expression), attribute_values, attribute_names
