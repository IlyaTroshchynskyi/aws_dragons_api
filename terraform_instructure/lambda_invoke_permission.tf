# Allow S3 to invoke Lambda
module "allow_s3_invoke" {
  source        = "./modules/lambda_invoke_permission/"
  function_name = module.upload_dragons_to_db.lambda_name
  principal     = "s3.amazonaws.com"
  source_arn    = "arn:aws:s3:::${module.csv-dragons.bucket_name}"
}
#

module "event_bridge_event_handler_lambda_permission" {
  source        = "./modules/lambda_invoke_permission/"
  function_name = module.event_bridge_event_handler_lambda.lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.dangerous_dragon_rule.arn
}

#
module "generate_report_lambda_permission" {
  source        = "./modules/lambda_invoke_permission/"
  function_name = module.generate_report_lambda.lambda_name
  principal     = "events.amazonaws.com"
}

#
module "super_dangerous_dragon_permission" {
  source        = "./modules/lambda_invoke_permission/"
  function_name = module.dangerous_dragon_lambda.lambda_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.super_dangerous_dragon_rule.arn
}