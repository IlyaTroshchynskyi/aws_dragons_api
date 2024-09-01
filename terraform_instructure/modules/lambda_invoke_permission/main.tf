resource "aws_lambda_permission" "lambda_invoke_permission" {
  action        = "lambda:InvokeFunction"
  function_name =  var.function_name
  principal     = var.principal
  source_arn    = var.source_arn
}
