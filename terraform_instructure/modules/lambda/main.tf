## example https://github.com/atheiman/terraform-aws-lambda-python/blob/main/main.tf
##https://github.com/cjh-cloud/lambda-chain-tf/blob/main/project/lambda_layer.tf
## The source_code_hash attribute will change whenever you update the code contained in the archive,
##which lets Lambda know that there is a new version of your code available.

resource "aws_cloudwatch_log_group" "log_group" {
  name = "/aws/lambda/${var.function_name}"
  retention_in_days = 30
}

# Attach the specified policies to the role
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  count = length(var.policy_arns)

  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = element(var.policy_arns, count.index)
}
data "archive_file" "lambda_archiving" {
  type = "zip"

  source_dir  = "./../dragons_api"
  output_path = "./lambda_outputs/${var.function_name}_${var.env}.zip"
}


resource "aws_lambda_function" "lambda_handler" {
  function_name = var.function_name
  filename = "./lambda_outputs/${var.function_name}_${var.env}.zip"

  runtime = "python3.11"
  handler = var.handler

  source_code_hash = filebase64sha256(var.source_code_filename)
  layers = [var.layer_arn]

  role = aws_iam_role.lambda_exec_role.arn
  environment {
    variables = merge(
      {
        ENVIRONMENT = var.env
      },
      var.lambda_env_vars
    )
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "role-${var.function_name}-${var.env}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}
