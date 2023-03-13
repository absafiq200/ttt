
module "cognito" {
  source                               = "./modules/module/cognito"
  cog_user_pool_name                   = "ehs-user-pool-${var.env}"
  tags                                 = local.cognito_tags
  cog_identifier                       = var.amplify_domain_name
  scope_name                           = "all"
  scope_description                    = "Get access to all API Gateway endpoints."
  allowed_oauth_flows                  = ["implicit"]
  supported_identity_providers         = ["COGNITO"]
  allowed_oauth_flows_user_pool_client = true
  explicit_auth_flows                  = ["ALLOW_CUSTOM_AUTH", "ALLOW_REFRESH_TOKEN_AUTH", "ALLOW_USER_SRP_AUTH"]
  generate_secret                      = false
  cognito_domain_name                  = var.cognito_domain_name 
  depends_on = [
    module.template_iam_role,module.template_lambda,module.campaign_crud_iam_role,module.campaign_crud_lambda,
    module.campaign_report_iam_role,module.campaign_report_lambda,#module.campaign_start_iam_role,module.campaign_start_lambda,
    module.campaign_stop_iam_role,module.campaign_stop_lambda
  ]
  allowed_oauth_scopes =  var.allowed_oauth_scopes
}

module "apigatewy" {
  source             = "./modules/module/apigateway"
  description        = "Api Gateway for Pinpoint"
  api_name           = "${var.api_name}-${var.env}"
  protocol_type      = var.protocol_type
  cors_configuration = var.cors_configuration
  endpoint_type      = var.endpoint_type
  stage_name         = var.env
  auto_deploy        = true
  cognitio_auth_name = "ehs-api-auth-${var.env}"
  auth_audience      = module.cognito.cognito_user_pool_client_id
  cog_endpoint       = module.cognito.cognito_user_pool_endpoint
  auth_type          = "JWT"
  depends_on = [
    module.cognito
  ]
  apiroutes = {
    "POST /create_campaign" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "POST /create_campaign/run" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "PUT /update_campaign" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "PUT /update_campaign/run" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "POST /start_campaign" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "POST /stop_campaign" = {
      lambda_arn = module.campaign_stop_lambda.lambda_function_arn
    }
    "POST /get_campaign" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "POST /get_campaign/run" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "DELETE /delete_campaign" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "DELETE /delete_campaign/run" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }
    "GET /list_campaign" = {
      lambda_arn = module.campaign_crud_lambda.lambda_function_arn
    }

    "POST /template/{type}/create" = {
      lambda_arn = module.template_lambda.lambda_function_arn
    }
    "PUT /template/{type}/update" = {
      lambda_arn = module.template_lambda.lambda_function_arn
    }
    "DELETE /template/{type}/delete" = {
      lambda_arn = module.template_lambda.lambda_function_arn
    }
    "POST /template/{type}/get" = {
      lambda_arn = module.template_lambda.lambda_function_arn
    }
    "GET /template/list_templates" = {
      lambda_arn = module.template_lambda.lambda_function_arn
    }
    "POST /reports/{type}/create" = {
      lambda_arn = module.campaign_report_lambda.lambda_function_arn
    }
    "PUT /reports/{type}/update" = {
      lambda_arn = module.campaign_report_lambda.lambda_function_arn
    }
    "DELETE /reports/{type}/delete/{reportid}" = {
      lambda_arn = module.campaign_report_lambda.lambda_function_arn
    }
    "GET /reports/{type}/get/{reportid}" = {
      lambda_arn = module.campaign_report_lambda.lambda_function_arn
    }
    "GET /reports/list_reports" = {
      lambda_arn = module.campaign_report_lambda.lambda_function_arn
    }
    "POST /upload/{folder}/{object}" = {
      lambda_arn = module.campaign_report_lambda.lambda_function_arn
    }
    "POST /segment/create/status" = {
      lambda_arn = module.segment_lambda.lambda_function_arn
    }
    "DELETE /segment/delete" = {
      lambda_arn = module.segment_lambda.lambda_function_arn
    }
    "POST /segment/{type}/get" = {
      lambda_arn = module.segment_lambda.lambda_function_arn
    }


  }

  tags = local.apigateway_tags
}

module "apigw_lambda_invoke_perm" {
  source                    = "./modules/module/apigw_lambda_perm"
  lambda_function_name      = "arn:aws:lambda:us-east-1:054247801503:function:testpp"
  api_gateway_execution_arn = module.apigatewy.api_gateway_execution_arn
}

module "apigw_lambda_invoke_perm_template" {
  source                    = "./modules/module/apigw_lambda_perm"
  lambda_function_name = module.template_lambda.lambda_function_arn
  api_gateway_execution_arn = module.apigatewy.api_gateway_execution_arn
}

module "apigw_lambda_invoke_perm_segment" {
  source                    = "./modules/module/apigw_lambda_perm"
  lambda_function_name = module.segment_lambda.lambda_function_arn
  api_gateway_execution_arn = module.apigatewy.api_gateway_execution_arn
}

module "apigw_lambda_invoke_perm_campaign_crud" {
  source                    = "./modules/module/apigw_lambda_perm"
  lambda_function_name = module.campaign_crud_lambda.lambda_function_arn
  api_gateway_execution_arn = module.apigatewy.api_gateway_execution_arn
}

module "apigw_lambda_invoke_perm_campaign_report" {
  source                    = "./modules/module/apigw_lambda_perm"
  lambda_function_name = module.campaign_report_lambda.lambda_function_arn
  api_gateway_execution_arn = module.apigatewy.api_gateway_execution_arn
}

#module "apigw_lambda_invoke_perm_campaign_start" {
#  source                    = "./modules/module/apigw_lambda_perm"
#  lambda_function_name = module.campaign_start_lambda.lambda_function_arn
#  api_gateway_execution_arn = module.apigatewy.api_gateway_execution_arn
#}

module "apigw_lambda_invoke_perm_campaign_stop" {
  source                    = "./modules/module/apigw_lambda_perm"
  lambda_function_name = module.campaign_stop_lambda.lambda_function_arn
  api_gateway_execution_arn = module.apigatewy.api_gateway_execution_arn
}

