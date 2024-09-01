variable "function_name" {
  type = string
}

variable "source_code_filename" {
  type = string
}

variable "env" {
  type = string

}

variable "lambda_env_vars" {
  description = "A map of environment-specific variables for Lambda functions"
  type        = map(string)
  default     = {}
}

variable "policy_arns" {
  description = "A list of IAM policy ARNs to attach to the Lambda function's role"
  type        = list(string)
  default     = []
}
variable "handler" {
  type = string
}
variable "layer_arn" {
  type = string
}