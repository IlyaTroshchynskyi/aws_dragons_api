module "csv-dragons" {
  source      = "./modules/s3/"
  bucket_name = "cvs-dragons-${var.environment}"
  environment = var.environment
}

module "dragons_reports" {
  source      = "./modules/s3/"
  bucket_name = "dragons-reports-statistics-${var.environment}"
  environment = var.environment
}

module "dragonsapi" {
  source      = "./modules/s3/"
  bucket_name = "dragonsapi-${var.environment}"
  environment = var.environment
}
