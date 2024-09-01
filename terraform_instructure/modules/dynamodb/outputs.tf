output "table_arn" {
  description = "The ARN of the DynamoDB table"
  value       = aws_dynamodb_table.dynamodb.arn
}

output "table_name" {
  description = "The name of the DynamoDB table"
  value       = aws_dynamodb_table.dynamodb.name
}

output "stream_arn" {
  description = "Stream arn"
  value       = aws_dynamodb_table.dynamodb.stream_arn
}
