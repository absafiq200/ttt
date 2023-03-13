locals {
  pinpoint_campaign_table_name = "${var.pinpoint_campaign_table_name}-${var.env}"
  pinpoint_campaign_meta_table_name = "${var.pinpoint_campaign_meta_table_name}-${var.env}"
  pinpoint_campaign_template_table_name = "${var.pinpoint_campaign_template_table_name}-${var.env}"
  powertoollayer = "arn:aws:lambda:${var.aws_region}:017000801446:layer:AWSLambdaPowertoolsPythonV2:21"
  dynamodb_tags = {
    "environment" = var.env
  }

  apigateway_tags = {
    "environment" = var.env
  }

  cognito_tags = {
    "environment" = var.env
  }
  lambda_api_tags = {
    "environment" = var.env
  }


}