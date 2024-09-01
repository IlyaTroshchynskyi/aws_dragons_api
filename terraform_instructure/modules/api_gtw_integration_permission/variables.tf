variable "api_id" {
  type = string
}

variable "integration_uri" {
  type = string
}

variable "integration_method" {
  type = string
  default = "GET"
}

variable "route_key" {
  type = string
  default = "GET /dragons"
}

variable "lambda_name" {
  type = string
}
variable "aws_apigateway_source_arn" {
  type = string
}
variable "is_create" {
  type = number
  default = 1
}

variable "authorizer_id" {
  type = string

}
variable "authorization_type" {
  type = string
  default = "JWT"
}
