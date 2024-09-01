resource "aws_apigatewayv2_api" "aws_apigateway" {
  name          = "${var.environment}-${var.api_gateway_name}"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "aws_apigt_stage" {
  api_id = aws_apigatewayv2_api.aws_apigateway.id

  name        = "${var.environment}-${var.api_gateway_name}-stage"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gtw_log_group.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
  tags = {
    Environment = "${var.environment}"
  }
}
resource "aws_cloudwatch_log_group" "api_gtw_log_group" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.aws_apigateway.name}"

  retention_in_days = 30
}

resource "aws_apigatewayv2_authorizer" "cognito_authorizer" {
  api_id           = aws_apigatewayv2_api.aws_apigateway.id
  authorizer_type  = "JWT"
  authorizer_uri   = module.lambda_get_resigned_url.invoke_arn
  identity_sources = ["$request.header.Authorization"]
  name             = "cognito-authorizer-${var.environment}"
  jwt_configuration {
    audience = [aws_cognito_user_pool_client.user_pool_client.id]
    issuer   = "https://${aws_cognito_user_pool.dragons-user-pool.endpoint}"
  }
}

module "presigne_url_route_integration" {
  source                    = "./modules/api_gtw_integration_permission/"
  api_id                    = aws_apigatewayv2_api.aws_apigateway.id
  aws_apigateway_source_arn = "${aws_apigatewayv2_api.aws_apigateway.execution_arn}/*/*"
  lambda_name               = module.lambda_get_resigned_url.lambda_name
  integration_uri           = module.lambda_get_resigned_url.invoke_arn
  route_key                 = "GET /generate_url"
  integration_method        = "POST"
  authorizer_id             = aws_apigatewayv2_authorizer.cognito_authorizer.id
}


# Crud routes

variable "routes" {
  type = map(string)
  default = {
    "GET /dragons"    = "GET"
    "POST /dragons"   = "POST"
    "PUT /dragons"    = "PUT"
    "DELETE /dragons" = "DELETE"
  }
}

module "crud_integration_routes_get" {
  source                    = "./modules/api_gtw_integration_permission/"
  api_id                    = aws_apigatewayv2_api.aws_apigateway.id
  aws_apigateway_source_arn = "${aws_apigatewayv2_api.aws_apigateway.execution_arn}/*/*"
  lambda_name               = module.crud_dragons_lambda.lambda_name
  integration_uri           = module.crud_dragons_lambda.invoke_arn
  route_key                 = "GET /dragons"
  authorizer_id             = aws_apigatewayv2_authorizer.cognito_authorizer.id
}

module "crud_integration_routes_get_by_id" {
  source                    = "./modules/api_gtw_integration_permission/"
  is_create                 = 0
  api_id                    = aws_apigatewayv2_api.aws_apigateway.id
  aws_apigateway_source_arn = "${aws_apigatewayv2_api.aws_apigateway.execution_arn}/*/*"
  lambda_name               = module.crud_dragons_lambda.lambda_name
  integration_uri           = module.crud_dragons_lambda.invoke_arn
  route_key                 = "GET /dragons/{proxy}"
  authorizer_id             = aws_apigatewayv2_authorizer.cognito_authorizer.id
}

module "crud_integration_routes_post" {
  source                    = "./modules/api_gtw_integration_permission/"
  is_create                 = 0
  api_id                    = aws_apigatewayv2_api.aws_apigateway.id
  aws_apigateway_source_arn = "${aws_apigatewayv2_api.aws_apigateway.execution_arn}/*/*"
  lambda_name               = module.crud_dragons_lambda.lambda_name
  integration_uri           = module.crud_dragons_lambda.invoke_arn
  route_key                 = "POST /dragons"
  authorizer_id             = aws_apigatewayv2_authorizer.cognito_authorizer.id
}


module "crud_integration_routes_patch" {
  source                    = "./modules/api_gtw_integration_permission/"
  is_create                 = 0
  api_id                    = aws_apigatewayv2_api.aws_apigateway.id
  aws_apigateway_source_arn = "${aws_apigatewayv2_api.aws_apigateway.execution_arn}/*/*"
  lambda_name               = module.crud_dragons_lambda.lambda_name
  integration_uri           = module.crud_dragons_lambda.invoke_arn
  route_key                 = "PATCH /dragons"
  authorizer_id             = aws_apigatewayv2_authorizer.cognito_authorizer.id
}

module "crud_integration_routes_delete" {
  source                    = "./modules/api_gtw_integration_permission/"
  is_create                 = 0
  api_id                    = aws_apigatewayv2_api.aws_apigateway.id
  aws_apigateway_source_arn = "${aws_apigatewayv2_api.aws_apigateway.execution_arn}/*/*"
  lambda_name               = module.crud_dragons_lambda.lambda_name
  integration_uri           = module.crud_dragons_lambda.invoke_arn
  route_key                 = "DELETE /dragons/{proxy}"
  authorizer_id             = aws_apigatewayv2_authorizer.cognito_authorizer.id
}

