resource "aws_lambda_function" "lambda" {   

    filename = var.output_path_filename
    function_name = var.function_name
    description = var.description
    memory_size = var.memory_size
    runtime = var.runtime
    role = var.role_arn
    handler = var.handler
    source_code_hash = data.archive_file.lambda.output_base64sha256
    timeout = var.timeout
    environment {
      variables = var.lambda_env_var
    }
    depends_on = [
      data.archive_file.lambda,aws_cloudwatch_log_group.lambda
    ]
    layers = var.layers 
    tags = var.tags
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = "/aws/lambda/${var.function_name}"
  retention_in_days = 365
}

data "archive_file" "lambda" {
  type        = var.zip_type
  source_dir  = var.source_dir
  output_path = var.output_path_filename
}