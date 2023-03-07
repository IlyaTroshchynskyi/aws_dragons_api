import json
import os

from .utils import create_invoke_command


def test_sns_lambda_notification(create_sns_topic, base_dir):
    command = create_invoke_command(base_dir, "NotifyAboutDangerousDragon", "sns_data_event")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    assert data.get("statusCode") == 200
    assert body.get("response").get("ResponseMetadata").get("HTTPStatusCode") == 200
