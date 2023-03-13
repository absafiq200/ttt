
resource "aws_apigatewayv2_api" "api_gw" {
    name = var.api_name    
    protocol_type = var.protocol_type
    description = var.description
    api_key_selection_expression = "$request.header.x-api-key"
    route_selection_expression   = "$request.method $request.path"
    dynamic "cors_configuration" {

        for_each = length(keys(var.cors_configuration)) == 0 ? [] : [var.cors_configuration]
        content {
        allow_credentials = try(cors_configuration.value.allow_credentials, null)
        allow_headers     = try(cors_configuration.value.allow_headers, null)
        allow_methods     = try(cors_configuration.value.allow_methods, null)
        allow_origins     = try(cors_configuration.value.allow_origins, null)
        expose_headers    = try(cors_configuration.value.expose_headers, null)
        max_age           = try(cors_configuration.value.max_age, null)
        }    
    }
  
    tags = var.tags
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.api_gw.name}"
  retention_in_days = 180
}


resource "aws_apigatewayv2_stage" "api_gw" {
  api_id = aws_apigatewayv2_api.api_gw.id
  name   = var.stage_name
  auto_deploy = var.auto_deploy  
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn
    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_authorizer" "api_gw" {
  api_id = aws_apigatewayv2_api.api_gw.id
  authorizer_type = var.auth_type
  identity_sources = [ "$request.header.Authorization" ]
  name = var.cognitio_auth_name
  jwt_configuration {
    audience = [ var.auth_audience ]
    issuer = "https://${var.cog_endpoint}"
  }
}

resource "aws_apigatewayv2_integration" "api_gw" {
  api_id = aws_apigatewayv2_api.api_gw.id
  for_each = var.apiroutes
  integration_type = "AWS_PROXY"
  integration_method = "POST"
  payload_format_version = "2.0"
  timeout_milliseconds = 600
  connection_type = "INTERNET"
  integration_uri= each.value.lambda_arn     
}

resource "aws_apigatewayv2_route" "api_gw" {
  api_id    = aws_apigatewayv2_api.api_gw.id
  for_each = var.apiroutes
  route_key = each.key
  target                              = "integrations/${aws_apigatewayv2_integration.api_gw[each.key].id}"
  authorization_type = var.auth_type
  authorizer_id = aws_apigatewayv2_authorizer.api_gw.id
}


