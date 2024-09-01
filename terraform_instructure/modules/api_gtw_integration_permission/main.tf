resource "aws_apigatewayv2_integration" "api_gtw_integration_dragons" {
  api_id = var.api_id

  integration_uri    = var.integration_uri
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "api_gtw_route_get" {
  api_id = var.api_id
  authorizer_id = var.authorizer_id
  authorization_type = var.authorization_type

  route_key = var.route_key
  target    = "integrations/${aws_apigatewayv2_integration.api_gtw_integration_dragons.id}"
}


#  gives API Gateway permission to invoke your Lambda function.
resource "aws_lambda_permission" "api_gtw_lambda_permission" {
  count = var.is_create
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_name
  principal     = "apigateway.amazonaws.com"


  source_arn = var.aws_apigateway_source_arn
}