output "api_gateway_execution_arn" {
    value = aws_apigatewayv2_api.api_gw.execution_arn
    description = "Api Gateway execution arn"  
}
output "api_gateway_invoke_url" {
  value = aws_apigatewayv2_stage.api_gw.invoke_url
}