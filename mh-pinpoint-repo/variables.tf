variable "aws_region" {
  description = "Aws region"
  type        = string
  default     = "us-east-1"
}

variable "app_deploy_env_role_arn" {
  description = "Mgmt Deployment role"
  type        = string
}

variable "env" {
  description = "Environment"
  type        = string
}

variable "amplify_domain_name" {
  description = "amplify front end domain name"
  type        = list(string)
}
variable "account_id" {
  description = "Aws Account ID"
  type = string
  
}
variable "pinpoint_project_id" {
  description = "EHS pinpoint project id"
  type = string
  default = "6961dcd9bff04b21970d9380310d4c57"
}

variable "cognito_domain_name" {
  description = "cognito domain name"
  type = string
  default = "masshealthoutreachtest"

}
variable "allowed_oauth_scopes" {
  description = "Allowed oAuth Scope"
  type = list(string)
  default = ["email","openid","phone","profile"]
  
}