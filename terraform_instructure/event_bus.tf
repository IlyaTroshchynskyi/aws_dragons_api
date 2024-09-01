resource "aws_cloudwatch_event_bus" "dragons_event_bus" {
  name = "dragons-${var.environment}"
}

resource "aws_cloudwatch_event_rule" "dangerous_dragon_rule" {
  event_bus_name = aws_cloudwatch_event_bus.dragons_event_bus.arn
  name           = "capture-dangerous-dragons-${var.environment}"
  description    = "capture-dangerous-dragons-${var.environment}"

  event_pattern = jsonencode({
    source = [module.dynamo_db_stream_event_creator_lambda.lambda_name]

  })
  depends_on = [aws_cloudwatch_event_bus.dragons_event_bus]
}

resource "aws_cloudwatch_event_target" "event_lambda_target" {
  event_bus_name = aws_cloudwatch_event_bus.dragons_event_bus.arn
  rule           = aws_cloudwatch_event_rule.dangerous_dragon_rule.name
  target_id      = "Lambda-Dangerous-${var.environment}"
  arn            = module.event_bridge_event_handler_lambda.lambda_arn
  depends_on     = [aws_cloudwatch_event_rule.dangerous_dragon_rule]
}

# Generate event report ==============================================================================
resource "aws_cloudwatch_event_rule" "daily_statistics_rule" {
  name                = "DragonsDailyStatistics-${var.environment}"
  description         = "DragonsDailyStatistics-${var.environment}"
  schedule_expression = "cron(0 0 * * ? *)"
}

resource "aws_cloudwatch_event_target" "daily_statistics_rule_target" {
  rule       = aws_cloudwatch_event_rule.daily_statistics_rule.name
  arn        = module.generate_report_lambda.lambda_arn
  depends_on = [aws_cloudwatch_event_rule.daily_statistics_rule]
}


# Dangerous dragon ==========================================================

resource "aws_cloudwatch_event_rule" "super_dangerous_dragon_rule" {

  event_bus_name = aws_cloudwatch_event_bus.dragons_event_bus.arn
  name           = "DangerousDragon-${var.environment}"
  description    = "DangerousDragon-${var.environment}"

  event_pattern = jsonencode({
    "source" = [
      "event_bridge_event_handle-${var.environment}"
    ],
    "detail" = {
      "danger_rating" = [{
        "numeric" = [">", 6]
      }]
    }
  })

}

resource "aws_cloudwatch_event_target" "super_dangerous_dragon_target" {
  event_bus_name = aws_cloudwatch_event_bus.dragons_event_bus.arn
  rule           = aws_cloudwatch_event_rule.super_dangerous_dragon_rule.name
  arn            = module.dangerous_dragon_lambda.lambda_arn
  depends_on = [
    aws_cloudwatch_event_rule.super_dangerous_dragon_rule,
    aws_cloudwatch_event_bus.dragons_event_bus
  ]
}
