output "lambda_name" {
  value = aws_lambda_function.lambda_handler.function_name
}
output "role_exec_name" {
  value = aws_iam_role.lambda_exec_role.name
}
output "invoke_arn" {
  value = aws_lambda_function.lambda_handler.invoke_arn
}

output "lambda_arn" {
  value = aws_lambda_function.lambda_handler.arn
}

output "lambda_id" {
  value = aws_lambda_function.lambda_handler.id
}