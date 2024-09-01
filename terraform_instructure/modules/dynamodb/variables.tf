variable "table_name" {
  description = "The name of the DynamoDB table"
  type        = string
}

variable "billing_mode" {
  description = "Controls how you are charged for read and write throughput and how you manage capacity."
  type        = string
  default     = "PROVISIONED"
}

variable "read_capacity" {
  description = "The number of read units for this table. Required if billing_mode is PROVISIONED."
  type        = number
  default     = 5
}

variable "write_capacity" {
  description = "The number of write units for this table. Required if billing_mode is PROVISIONED."
  type        = number
  default     = 5
}

variable "hash_key" {
  description = "The name of the hash key in the DynamoDB table"
  type        = string
}

variable "hash_key_type" {
  description = "The type of the hash key (e.g., S for string, N for number)"
  type        = string
  default     = "S"
}

variable "stream_enabled" {
  description = "Indicates whether Streams are to be enabled (true) or disabled (false)."
  type        = bool
  default     = false
}

variable "stream_view_type" {
  description = "When an item in the table is modified, StreamViewType determines what information is written to the stream for this table."
  type        = string
  default     = "NEW_AND_OLD_IMAGES"
}

variable "ttl_enabled" {
  description = "Indicates whether TTL is enabled for the table."
  type        = bool
  default     = false
}

variable "ttl_attribute_name" {
  description = "The name of the TTL attribute."
  type        = string
  default     = ""
}

variable "tags" {
  description = "A map of tags to assign to the resource."
  type        = map(string)
  default     = {}
}
