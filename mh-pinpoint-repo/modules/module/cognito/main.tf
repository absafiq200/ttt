resource "aws_cognito_user_pool" "cognito" {
  name = var.cog_user_pool_name
  tags = var.tags
  auto_verified_attributes = ["email"]
  }
/*
resource "aws_cognito_resource_server" "cognito" {
  name = var.cog_user_pool_name
  user_pool_id = aws_cognito_user_pool.cognito.id
  identifier = var.cog_identifier
  scope {
    scope_name = var.scope_name
    scope_description = var.scope_description
  }
}
*/
resource "aws_cognito_user_pool_client" "cognito" {
  //name = var.cog_user_pool_name  
  name = "ehs-campaignui"
  user_pool_id = aws_cognito_user_pool.cognito.id
  allowed_oauth_flows = var.allowed_oauth_flows
  callback_urls = var.cog_identifier
  logout_urls = var.cog_identifier   
  supported_identity_providers = var.supported_identity_providers
  allowed_oauth_flows_user_pool_client = var.allowed_oauth_flows_user_pool_client
  explicit_auth_flows =  var.explicit_auth_flows
  generate_secret = var.generate_secret
  allowed_oauth_scopes                  = var.allowed_oauth_scopes     

        
  

              
}

resource "aws_cognito_user_pool_domain" "cognito" {
  domain = var.cognito_domain_name
  user_pool_id = aws_cognito_user_pool.cognito.id 
}
