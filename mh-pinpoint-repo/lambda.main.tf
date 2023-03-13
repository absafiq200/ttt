
module "segment_iam_role" {
  source = "./modules/module/iamrole"
  assume_type            = var.sts_assume_service
  trust_role             = var.sts_assume_role
  iam_role_path          = var.iam_role_path
  iam_role_name          = "pinpoint-segment-lambda-execute-${var.env}"  
  iam_role_description   = "pinpoint segment lambda execution role -${var.env}"  
  iam_policy_name        = "pinpoint-segment-lambda-policy-${var.env}"
  iam_policy_description = "pinpoint segment lambda execution policy -${var.env}"  
  policy = templatefile("${path.module}/lambda/segment/policy/lambda.json", {  
    region = "${var.aws_region}",
    function_name = "EHS-pinpoint-segment-api-${var.env}",
    account_id = var.account_id 
  })
  
}

module "segment_lambda" {
  source = "./modules/module/lambda"
  zip_type = var.lambda_zip_file
  source_dir="${path.module}/lambda/segment/src"
  output_path_filename = "${path.module}/lambda/segment/template.zip"
  function_name = "EHS-pinpoint-segment-api-${var.env}"
  description = "Pinpoint Segment Api"
  memory_size = var.memory_256
  runtime = var.python_runtime_38
  role_arn = module.segment_iam_role.iam_role_arn
  handler = "lambda_handler.lambda_handler"  
  timeout = var.campaign_segment_lambda_timeout
  depends_on = [
    module.segment_iam_role
  ]
  lambda_env_var = {
    LOG_LEVEL    = "INFO"
  }
  layers = [local.powertoollayer]
  tags = local.lambda_api_tags
}

module "template_iam_role" {
  source = "./modules/module/iamrole"
  assume_type            = var.sts_assume_service
  trust_role             = var.sts_assume_role
  iam_role_path          = var.iam_role_path
  iam_role_name          = "pinpoint-template-lambda-execute-${var.env}"  
  iam_role_description   = "pinpoint message template lambda execution role -${var.env}"  
  iam_policy_name        = "pinpoint-template-lambda-policy-${var.env}"
  iam_policy_description = "pinpoint message template lambda execution policy -${var.env}"  
  policy = templatefile("${path.module}/lambda/template/policy/lambda.json", {  
    region = "${var.aws_region}",
    function_name = "EHS-pinpoint-template-api-${var.env}",
    account_id = var.account_id 
  })
  
}

module "template_lambda" {
  source = "./modules/module/lambda"
  zip_type = var.lambda_zip_file
  source_dir="${path.module}/lambda/template/src"
  output_path_filename = "${path.module}/lambda/template/template.zip"
  function_name = "EHS-pinpoint-template-api-${var.env}"
  description = "Pinpoint Template CRUD Api"
  memory_size = var.memory_256
  runtime = var.python_runtime_38
  role_arn = module.template_iam_role.iam_role_arn
  handler = "lambda_handler.lambda_handler"  
  timeout = var.template_lambda_timeout
  depends_on = [
    module.template_iam_role
  ]
  lambda_env_var = {
    LOG_LEVEL    = "INFO"
    CAMPAIGN_TEMPLATE = local.pinpoint_campaign_template_table_name
  }
  layers = [local.powertoollayer]
  tags = local.lambda_api_tags
}

module "campaign_crud_iam_role" {
  source = "./modules/module/iamrole"
  assume_type            = var.sts_assume_service
  trust_role             = var.sts_assume_role
  iam_role_path          = var.iam_role_path
  iam_role_name          = "pinpoint-campaign-crud-lambda-execute-${var.env}"  
  iam_role_description   = "pinpoint campaign crud lambda execution role -${var.env}"  
  iam_policy_name        = "pinpoint-campaign-crud-lambda-policy-${var.env}"
  iam_policy_description = "pinpoint campaign crud lambda execution policy -${var.env}"  
  policy = templatefile("${path.module}/lambda/campaign_crud/policy/lambda.json", {  
    region = "${var.aws_region}",
    function_name = "EHS-pinpoint-campaign-crud-api-${var.env}",
    account_id = var.account_id 
  })
  
}

module "campaign_crud_lambda" {
  source = "./modules/module/lambda"
  zip_type = var.lambda_zip_file
  source_dir="${path.module}/lambda/campaign_crud/src"
  output_path_filename = "${path.module}/lambda/campaign_crud/campaign_crud.zip"
  function_name = "EHS-pinpoint-campaign-crud-api-${var.env}"
  description = "Pinpoint campaign crud Api"
  memory_size = var.memory_256
  runtime = var.python_runtime_38
  role_arn = module.campaign_crud_iam_role.iam_role_arn
  handler = "lambda_handler.lambda_handler"  
  timeout = var.campaign_crud_lambda_timeout
  
  depends_on = [
    module.campaign_crud_iam_role
  ]
  lambda_env_var = {
    LOG_LEVEL    = "DEBUG",
    CAMPAIGN_TABLE = local.pinpoint_campaign_table_name,
    CAMPAIGN_META_TABLE = local.pinpoint_campaign_meta_table_name
    PINPOINT_PROJECT_ID = var.pinpoint_project_id
  }
  layers = [local.powertoollayer]
  tags = local.lambda_api_tags
}

module "campaign_report_iam_role" {
  source = "./modules/module/iamrole"
  assume_type            = var.sts_assume_service
  trust_role             = var.sts_assume_role
  iam_role_path          = var.iam_role_path
  iam_role_name          = "pinpoint-campaign-report-lambda-execute-${var.env}"  
  iam_role_description   = "pinpoint campaign report lambda execution role -${var.env}"  
  iam_policy_name        = "pinpoint-campaign-report-lambda-policy-${var.env}"
  iam_policy_description = "pinpoint campaign report lambda execution policy -${var.env}"  
  policy = templatefile("${path.module}/lambda/campaign_report/policy/lambda.json", {  
    region = "${var.aws_region}",
    function_name = "EHS-pinpoint-campaign-report-api-${var.env}",
    account_id = var.account_id 
  })
}

module "campaign_report_lambda" {
  source = "./modules/module/lambda"
  zip_type = var.lambda_zip_file
  source_dir="${path.module}/lambda/campaign_report/src"
  output_path_filename = "${path.module}/lambda/campaign_report/campaign_report.zip"
  function_name = "EHS-pinpoint-campaign-report-api-${var.env}"
  description = "Pinpoint campaign report Api"
  memory_size = var.memory_256
  runtime = var.python_runtime_38
  role_arn = module.campaign_report_iam_role.iam_role_arn
  handler = "lambda_handler.lambda_handler"  
  timeout = var.campaign_report_lambda_timeout
  depends_on = [
    module.campaign_report_iam_role
  ]
  lambda_env_var = {
    LOG_LEVEL    = "DEBUG"
  }
  layers = [local.powertoollayer]
  tags = local.lambda_api_tags
}

#module "campaign_start_iam_role" {
#  source = "./modules/module/iamrole"
#  assume_type            = var.sts_assume_service
#  trust_role             = var.sts_assume_role
#  iam_role_path          = var.iam_role_path
#  iam_role_name          = "pinpoint-campaign-start-lambda-execute-${var.env}"  
#  iam_role_description   = "pinpoint campaign start lambda execution role -${var.env}"  
#  iam_policy_name        = "pinpoint-campaign-start-lambda-policy-${var.env}"
#  iam_policy_description = "pinpoint campaign start lambda execution policy -${var.env}"  
#  policy = templatefile("${path.module}/lambda/campaign_start/policy/lambda.json", {  
#    region = "${var.aws_region}",
#    function_name = "EHS-pinpoint-campaign-start-api-${var.env}",
#    account_id = var.account_id 
#  })
#}

#module "campaign_start_lambda" {
#  source = "./modules/module/lambda"
#  zip_type = var.lambda_zip_file
#  source_dir="${path.module}/lambda/campaign_start/src"
#  output_path_filename = "${path.module}/lambda/campaign_start/campaign_start.zip"
#  function_name = "EHS-pinpoint-campaign-start-api-${var.env}"
#  description = "Pinpoint campaign start Api"
#  memory_size = var.memory_256
#  runtime = var.python_runtime_38
#  role_arn = module.campaign_start_iam_role.iam_role_arn
#  handler = "campaign_main.lambda_handler"  
#  timeout = var.campaign_start_lambda_timeout
#  depends_on = [
#    module.campaign_start_iam_role
#  ]
#  lambda_env_var = {
#    LOG_LEVEL    = "INFO"
#  }
#  layers = [local.powertoollayer]
#  tags = local.lambda_api_tags
#}

module "campaign_stop_iam_role" {
  source = "./modules/module/iamrole"
  assume_type            = var.sts_assume_service
  trust_role             = var.sts_assume_role
  iam_role_path          = var.iam_role_path
  iam_role_name          = "pinpoint-campaign-stop-lambda-execute-${var.env}"  
  iam_role_description   = "pinpoint campaign stop lambda execution role -${var.env}"  
  iam_policy_name        = "pinpoint-campaign-stop-lambda-policy-${var.env}"
  iam_policy_description = "pinpoint campaign stop lambda execution policy -${var.env}"  
  policy = templatefile("${path.module}/lambda/campaign_stop/policy/lambda.json", {  
    region = "${var.aws_region}",
    function_name = "EHS-pinpoint-campaign-stop-api-${var.env}",
    account_id = var.account_id 
  })
}

module "campaign_stop_lambda" {
  source = "./modules/module/lambda"
  zip_type = var.lambda_zip_file
  source_dir="${path.module}/lambda/campaign_stop/src"
  output_path_filename = "${path.module}/lambda/campaign_stop/campaign_stop.zip"
  function_name = "EHS-pinpoint-campaign-stop-api-${var.env}"
  description = "Pinpoint campaign stop Api"
  memory_size = var.memory_256
  runtime = var.python_runtime_38
  role_arn = module.campaign_stop_iam_role.iam_role_arn
  handler = "campaign_main.lambda_handler"  
  timeout = var.campaign_stop_lambda_timeout
  depends_on = [
    module.campaign_stop_iam_role
  ]
  lambda_env_var = {
    LOG_LEVEL    = "DEBUG"
  }
  layers = [local.powertoollayer]
  tags = local.lambda_api_tags
}