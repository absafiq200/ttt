terraform {
  required_version = ">=1.0"

  required_providers {
    aws = {
      version = "3.48.0"
    }
  }


  backend "s3" {
    bucket         = "hix-terraform-state"
    key            = "mh-pinpoint-repo/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "hix-terraform-state-lock-dynamo"
  }

}