import json
import os
import time

from .utils import create_invoke_command


def test_dynamodb_stream_event_creator(create_event_bus, base_dir):
    command = create_invoke_command(base_dir, "DynamoDbStreamEventCreator", "dynamo_db_stream_event")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 200
    assert body.get("response") == "Events were send"


def test_handler_event_bridge(dynamo_db_statistics_table, base_dir, env_vars):
    command = create_invoke_command(base_dir, "EventBridgeHandler", "event_bridge_event")
    response = os.popen(command)
    data = json.loads(response.read())

    assert dynamo_db_statistics_table.scan()["Count"] == 3
    time.sleep(7)
    assert dynamo_db_statistics_table.scan()["Count"] == 0
