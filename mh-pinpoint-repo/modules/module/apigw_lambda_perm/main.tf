resource "aws_lambda_permission" "api_gw_lambda" {	
  action        = "lambda:InvokeFunction"
  function_name = var.lambda_function_name
  principal     = "apigateway.amazonaws.com"
  source_arn = format("%s/*/*",var.api_gateway_execution_arn)
}