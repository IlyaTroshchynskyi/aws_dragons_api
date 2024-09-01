resource "aws_sns_topic" "sns_topic_dangerous_dragons" {
  display_name = "dangerous-dragon-${var.environment}"
  name         = "dangerous-dragon-${var.environment}"

}

resource "aws_sns_topic_subscription" "sns_subscription_dangerous_dragons" {
  endpoint  = aws_ssm_parameter.parameter_email.value
  protocol  = "email"
  topic_arn = aws_sns_topic.sns_topic_dangerous_dragons.arn
}