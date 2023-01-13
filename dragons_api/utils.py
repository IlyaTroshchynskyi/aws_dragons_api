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


def json_response(data: dict, response_code=200) -> dict:
    """
    Build response for lambda functions
    """
    return {"statusCode": response_code, "body": json.dumps(data, cls=DecimalEncoder)}
