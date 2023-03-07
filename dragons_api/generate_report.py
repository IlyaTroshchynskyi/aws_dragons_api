import csv
import logging
import os
import time
from datetime import datetime, date

from boto3.dynamodb.conditions import Attr

from utils import json_response, get_dynamodb_table, get_s3_client

logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")

table_name = os.environ["STATISTICS_TABLE_NAME"]
table = get_dynamodb_table(table_name)
s3_client = get_s3_client()


def lambda_handler(event: dict, context) -> dict:
    """
    Cloud watch schedule event will trigger this lambda at the end of the day
    Generate a report in the form of a csv file, which will indicate how many dragons
    were created, updated and  deleted today.
    Upload the file to S3 bucket.
    Take note that ttl doesn't work right away.
    Therefore, we have a condition for filtering based on the current time.
    """
    statistics = {"INSERT": 0, "MODIFY": 0, "REMOVE": 0}
    filter_expr = Attr("dragon_ttl").gte(int(time.time()))
    response = table.scan(Limit=2, FilterExpression=filter_expr)
    data = response["Items"]
    while "LastEvaluatedKey" in response:
        response = table.scan(
            ExclusiveStartKey=response["LastEvaluatedKey"],
            Limit=2,
            FilterExpression=filter_expr,
        )
        data.extend(response["Items"])
    for item in data:
        statistics[item["dragon_action"]] += 1
    logger.debug(statistics)

    file_name = f"statistics_{datetime.now()}.csv"
    full_path = os.path.join("/tmp/", file_name)
    with open(full_path, "w") as file:
        writer = csv.writer(file)
        writer.writerow(["action", "count", "current_date"])
        for key, value in statistics.items():
            writer.writerow([key, value, date.today()])
    s3_client.upload_file(full_path, os.environ.get("REPORT_BUCKET_NAME"), file_name)

    return json_response({"response": statistics}, 200)
