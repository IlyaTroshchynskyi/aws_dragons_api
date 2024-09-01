# https://github.com/atheiman/terraform-aws-lambda-python/blob/main/main.tf
locals {
  lambda_runtime                = "python3.11"
  poetry_lock                   = "../poetry.lock"
  lambda_root                   = "./../"
  lambda_layer_root             = "${local.lambda_root}/lambda_layer"
  lambda_layer_requirements_txt = "${local.lambda_layer_root}/requirements.txt"
  # Python deps should be zipped into a `/python/` directory
  # https://docs.aws.amazon.com/lambda/latest/dg/packaging-layers.html#packaging-layers-paths
  lambda_layer_lib_root = "${local.lambda_layer_root}/python"
  lambda_function_root  = "${local.lambda_root}/dragons_api"
}

# create zip file from requirements.txt. Triggers only when the file is updated
resource "null_resource" "create_lambda_layer" {
  triggers = {
    requirements = filesha1(local.poetry_lock)
  }
  # the command to install python and dependencies to the machine and zips
  provisioner "local-exec" {
    command = <<EOT
	poetry export -f requirements.txt --output ${local.lambda_layer_requirements_txt} --without-hashes
    pip install -r ${local.lambda_layer_requirements_txt} -t ${local.lambda_layer_lib_root}
     EOT
  }
}


data "archive_file" "lambda_layer" {
  depends_on  = [null_resource.create_lambda_layer]
  type        = "zip"
  source_dir  = local.lambda_layer_root
  output_path = "${local.lambda_layer_root}/lambda_layer.zip"

}

resource "aws_lambda_layer_version" "layer" {
  layer_name          = "dragons-app-pip-requirements"
  filename            = data.archive_file.lambda_layer.output_path
  source_code_hash    = data.archive_file.lambda_layer.output_base64sha256
  compatible_runtimes = [local.lambda_runtime]
  depends_on          = [data.archive_file.lambda_layer]

  # Ensure the new layer version is created before the old layer version is deleted (avoids /
  # reduces function downtime). An alternative option is to set `skip_destroy = true`, but that
  # will result in unused layers which incur a cost.
  lifecycle {
    create_before_destroy = true
  }
}
