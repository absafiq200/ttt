provider "aws" {
  region = var.aws_region
  assume_role {
    role_arn = var.app_deploy_env_role_arn
  }
}