import json
import os
from datetime import date

import pytest
from .utils import create_invoke_command


@pytest.mark.parametrize(
    "create_delete_bucket", ["dragonsapireporttest"], indirect=True
)
def test_generate_report(
    fill_statistics_table, create_delete_bucket, base_dir, env_vars
):
    command = create_invoke_command(base_dir, "GenerateReport", "cron_report_event")
    response = os.popen(command)
    data = json.loads(response.read())
    body = json.loads(data.get("body"))
    file_name = create_delete_bucket.list_objects(
        Bucket=env_vars["REPORT_BUCKET_NAME"]
    )["Contents"][0]["Key"]
    content = create_delete_bucket.get_object(
        Bucket=env_vars["REPORT_BUCKET_NAME"], Key=file_name
    )
    contents = content["Body"].read().decode("utf-8")
    current_data = date.today()
    assert (
        contents == f"action,count,current_date\r\n"
        f"INSERT,2,{current_data}\r\n"
        f"MODIFY,2,{current_data}\r\n"
        f"REMOVE,2,{current_data}\r\n"
    )
    assert data.get("statusCode") == 200
    assert body.get("response") == {"INSERT": 2, "MODIFY": 2, "REMOVE": 2}
