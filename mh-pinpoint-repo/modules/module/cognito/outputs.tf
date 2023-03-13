output "cognito_user_pool_client_id" {
  value = aws_cognito_user_pool_client.cognito.id
  description = "cognito user pool client id"
}
output "cognito_user_pool_endpoint" {
  value = aws_cognito_user_pool.cognito.endpoint
  description = "cognito user pool endpoint"
}