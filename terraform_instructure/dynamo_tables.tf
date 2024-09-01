module "dynamodb_dragons" {
  source           = "./modules/dynamodb/"
  table_name       = "${var.dragons_name_table}-${var.environment}"
  hash_key         = "dragon_id"
  stream_enabled   = true
  stream_view_type = "NEW_AND_OLD_IMAGES"
}

module "dynamodb_statistics" {
  source             = "./modules/dynamodb/"
  table_name         = "${var.statistics_name_table}-${var.environment}"
  hash_key           = "record_id"
  ttl_enabled        = true
  ttl_attribute_name = "dragon_ttl"
}
