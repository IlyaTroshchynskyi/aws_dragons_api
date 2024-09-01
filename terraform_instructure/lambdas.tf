module "lambda_get_resigned_url" {
  source               = "./modules/lambda/"
  function_name        = "generate_presigned_url-${var.environment}"
  source_code_filename = "../dragons_api/generate_url.py"
  env                  = var.environment
  handler              = "generate_url.lambda_handler"
  layer_arn            = aws_lambda_layer_version.layer.arn
  lambda_env_vars = {
    AWS_S3_ENDPOINT_URL : "url",
    AWS_SAM_LOCAL : "no"
    AWS_S3_BUCKET_NAME : module.dragonsapi.bucket_name

  }

  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess",
    aws_iam_policy.s3_write_policy.arn,
  ]
}

data "aws_iam_policy_document" "s3_write_policy" {
  statement {
    actions = ["s3:PutObject", "s3:PutObjectAcl"]
    resources = [
      "arn:aws:s3:::${module.dragonsapi.bucket_name}/*"
    ]
  }
}


resource "aws_iam_policy" "s3_write_policy" {
  name   = "s3_write_policy"
  policy = data.aws_iam_policy_document.s3_write_policy.json
}

resource "aws_iam_role_policy_attachment" "attach_s3_write_policy" {
  role       = module.lambda_get_resigned_url.role_exec_name
  policy_arn = aws_iam_policy.s3_write_policy.arn
}

module "upload_dragons_to_db" {
  source               = "./modules/lambda/"
  function_name        = "upload_dragons_to_db-${var.environment}"
  source_code_filename = "../dragons_api/upload_to_db.py"
  env                  = var.environment
  handler              = "upload_to_db.lambda_handler"
  layer_arn            = aws_lambda_layer_version.layer.arn
  lambda_env_vars = {
    AWS_S3_ENDPOINT_URL : "url",
    AWS_SAM_LOCAL : "no"
    AWS_S3_BUCKET_NAME : module.dragonsapi.bucket_name
    DYNAMODB_ENDPOINT : "url"
    TABLE_NAME : module.dynamodb_dragons.table_name
  }

  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess",
    "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess",
    "arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess",
  ]
}


# S3 bucket event to trigger Lambda
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = module.csv-dragons.bucket_name

  lambda_function {
    lambda_function_arn = module.upload_dragons_to_db.lambda_arn
    events              = ["s3:ObjectCreated:Put"]
    filter_suffix       = ".csv"
  }
}


# ===========================================================================================
# Dragons crud function

module "crud_dragons_lambda" {
  source               = "./modules/lambda/"
  function_name        = "crud_dragons-${var.environment}"
  source_code_filename = "../dragons_api/app.py"
  env                  = var.environment
  handler              = "app.lambda_handler"
  layer_arn            = aws_lambda_layer_version.layer.arn
  lambda_env_vars = {
    AWS_SAM_LOCAL : "no"
    DYNAMODB_ENDPOINT : "url"
    TABLE_NAME : module.dynamodb_dragons.table_name
  }

  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/AWSLambdaInvocation-DynamoDB",
  ]
}



# =======================================task EventBridge

module "dynamo_db_stream_event_creator_lambda" {
  source               = "./modules/lambda/"
  function_name        = "dynamo_db_stream_event_creator-${var.environment}"
  source_code_filename = "../dragons_api/app.py"
  env                  = var.environment
  handler              = "dynamodb_stream_event.lambda_handler"
  layer_arn            = aws_lambda_layer_version.layer.arn
  lambda_env_vars = {
    AWS_SAM_LOCAL : "no"
    DYNAMODB_ENDPOINT : "url"
    TABLE_NAME : module.dynamodb_dragons.table_name
    EVENT_BRIDGE_ENDPOINT : "url"
    SOURCE_STREAM_HANDLER : "dynamo_db_stream_event_creator-${var.environment}"
    SOURCE_DANGER_DRAGON : "event_bridge_event_handle-${var.environment}"
    EVENT_BUS_NAME : aws_cloudwatch_event_bus.dragons_event_bus.name
  }

  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
    "arn:aws:iam::aws:policy/AmazonEventBridgeFullAccess",
  ]
}
# Add event for lambda DynamoDbStream

resource "aws_lambda_event_source_mapping" "dynamodb_stream_event_mapping" {
  event_source_arn  = module.dynamodb_dragons.stream_arn
  function_name     = module.dynamo_db_stream_event_creator_lambda.lambda_arn
  starting_position = "LATEST"
}


module "event_bridge_event_handler_lambda" {
  source               = "./modules/lambda/"
  function_name        = "event_bridge_event_handle-${var.environment}"
  source_code_filename = "../dragons_api/handler_event_bridge.py"
  env                  = var.environment
  handler              = "handler_event_bridge.lambda_handler"
  layer_arn            = aws_lambda_layer_version.layer.arn
  lambda_env_vars = {
    AWS_SAM_LOCAL : "no"
    DYNAMODB_ENDPOINT : "url"
    STATISTICS_TABLE_NAME : module.dynamodb_statistics.table_name
    TIME_TO_LIVE : 24
  }

  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess",
  ]
}

# Task generate report ==========================================================================

module "generate_report_lambda" {
  source               = "./modules/lambda/"
  function_name        = "generate_report-${var.environment}"
  source_code_filename = "../dragons_api/generate_report.py"
  env                  = var.environment
  handler              = "generate_report.lambda_handler"
  layer_arn            = aws_lambda_layer_version.layer.arn
  lambda_env_vars = {
    AWS_SAM_LOCAL : "no"
    DYNAMODB_ENDPOINT : "url"
    STATISTICS_TABLE_NAME : module.dynamodb_statistics.table_name
    REPORT_BUCKET_NAME : module.dragons_reports.bucket_name
    AWS_S3_ENDPOINT_URL : ""

  }

  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess",
    "arn:aws:iam::aws:policy/AmazonS3FullAccess",
  ]
}

# Dangerous dragon ==========================================================


module "dangerous_dragon_lambda" {
  source               = "./modules/lambda/"
  function_name        = "dangerous_dragon-${var.environment}"
  source_code_filename = "../dragons_api/dangerous_dragon.py"
  env                  = var.environment
  handler              = "dangerous_dragon.lambda_handler"
  layer_arn            = aws_lambda_layer_version.layer.arn
  lambda_env_vars = {
    AWS_SAM_LOCAL : "no"
    SNS_TOPIC_ARN : aws_sns_topic.sns_topic_dangerous_dragons.arn
    SNS_TOPIC_ENDPOINT : ""
  }

  policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    "arn:aws:iam::aws:policy/AmazonSNSFullAccess"
  ]
}


