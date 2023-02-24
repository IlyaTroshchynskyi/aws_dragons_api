import csv
import io
import os
import uuid
from datetime import datetime


from utils import json_response, get_s3_client, get_dynamodb_table
from validators import DragonValidator

s3_client = get_s3_client()
table = get_dynamodb_table()


def lambda_handler(event, context):
    """
    Read file from dynamodb parse dragons and write all dragons to db.
    If dragon_id is not unique batch operation will update dragon in table.
    Header of file should look like:
    event, name, breed, danger_rating, description.
    The second line of the file should have dragon data.
    """
    file_name = event["Records"][0]["s3"]["object"]["key"]

    response = s3_client.get_object(
        Bucket=os.environ.get("AWS_S3_BUCKET_NAME", ""), Key=file_name
    )
    data = response["Body"].read().decode("utf-8")
    reader = csv.reader(io.StringIO(data))

    header = next(reader)
    not_valid_items = []

    with table.batch_writer(overwrite_by_pkeys=["dragon_id"]) as batch:

        for line, row in enumerate(reader, start=1):
            dragon = dict(zip(header, row))
            dragon["danger_rating"] = (
                int(dragon["danger_rating"])
                if dragon["danger_rating"].isdigit()
                else dragon["danger_rating"]
            )
            valid = DragonValidator().validate_dragon(dragon)
            if valid is True:
                dragon.update(
                    {
                        "dragon_id": str(uuid.uuid4()),
                        "created_at": str(datetime.now()),
                        "username": "from file",
                    }
                )
                batch.put_item(Item=dragon)
            else:
                not_valid_items.append(line)
    return json_response(
        {
            "message": f"Numbers of rows are not valid: {not_valid_items}"
            if not_valid_items
            else "All unique items was uploaded"
        }
    )
