resource "aws_ssm_parameter" "parameter_email" {
  name  = "/${var.environment}/sender/email"
  type  = "SecureString"
  value = "email"
  lifecycle {
    ignore_changes = [value]
  }

}