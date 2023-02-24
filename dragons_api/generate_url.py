import logging
import os

from utils import json_response, get_s3_client


logger = logging.getLogger(__name__)
logger.setLevel("DEBUG")


s3_client = get_s3_client()


def lambda_handler(event, context) -> dict:
    """
    Generate a presigned Amazon S3 PUT request to upload a file.
    A presigned PUT can be used for a limited time to let someone without an AWS
    account upload a file to a bucket.
    Url should looks like http:domain/generate_url?file_name=<your file name>
    """
    file = event.get("queryStringParameters")
    if file:
        file_name = file.get("file_name")
    else:
        return json_response(
            {"message": "User should set up query parameter for filename"}, 400
        )

    url = s3_client.generate_presigned_url(
        "put_object",
        Params={"Bucket": os.environ.get("AWS_S3_BUCKET_NAME", ""), "Key": file_name},
        ExpiresIn=3600,
    )
    logger.debug(f"Got presigned URL: {url}")

    return json_response({"url": url}, 200)
