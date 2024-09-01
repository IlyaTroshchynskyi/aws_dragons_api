variable "environment" {
  description = "Environment"
  type        = string
}

variable "dynamo_db_tag" {
  description = "db"
  type        = string
}

variable "region" {
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "api_gateway_name" {
  type    = string
  default = "dragons_api_gw_http"
}
variable "python_version" {
  type    = string
  default = "python3.10"
}

variable "dragons_name_table" {
  type    = string
  default = "dragons"
}

variable "statistics_name_table" {
  type    = string
  default = "statistics"
}

variable "user_pool_name" {
  type    = string
  default = "dragons-pool"
}

variable "notify_about_dangerous_dragon_param" {
  type        = string
  default     = "NotifyAboutDangerousDragon"
  description = "Name of Source. It is used in Event bridge rule"
}

variable "dynamo_db_stream_event_creator_param" {
  type        = string
  default     = "DynamoDbStreamEventCreator"
  description = "Name of Source. It is used in Event bridge rule"
}
