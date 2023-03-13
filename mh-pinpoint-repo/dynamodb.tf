
module "dynamodb-campaign" {
  source     = "./modules/module/dynamodb"
  table_name = local.pinpoint_campaign_table_name

  billing_mode         = var.pinpoint_campaign_table_billing_mode
  hash_key_column      = var.pinpoint_campaign_table_hash_key
  hash_key_column_type = var.pinpoint_campaign_table_hash_key_column_type
  tags                 = local.dynamodb_tags
}

module "dynamodb-camp-metadata" {
  source               = "./modules/module/dynamodb"
  table_name           = local.pinpoint_campaign_meta_table_name 
  billing_mode         = var.pinpoint_campaign_meta_billing_mode
  hash_key_column      = var.pinpoint_campaign_meta_hash_key
  hash_key_column_type = var.pinpoint_campaign_meta_hash_key_column_type
  tags                 = local.dynamodb_tags
}

module "dynamodb-camp-template" {
  source               = "./modules/module/dynamodb"
  table_name           = local.pinpoint_campaign_template_table_name 
  billing_mode         = var.pinpoint_campaign_template_billing_mode
  hash_key_column      = var.pinpoint_campaign_template_hash_key
  hash_key_column_type = var.pinpoint_campaign_template_hash_key_column_type
  tags                 = local.dynamodb_tags
}

resource "aws_dynamodb_table" "dynamodb_hash_index" {
  name         = "pinpoint_campaign_optout-${var.env}"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "record_id"
  point_in_time_recovery {
    enabled = true
  }
  attribute {
    name = "record_id"
    type = "S"
  }
  attribute {
    name = "campaign_id"
    type = "S"
  }

  attribute {
    name = "campaign_name"
    type = "S"
  }

  attribute {
    name = "phonenum"
    type = "S"
  }

  global_secondary_index {
    name            = "campaign_id-PhoneNum-index"
    hash_key        = "campaign_id"
    range_key       = "phonenum"
    projection_type = "ALL"
  }

  global_secondary_index {
    name            = "campaign_name-PhoneNum-index"
    hash_key        = "campaign_name"
    range_key       = "phonenum"
    projection_type = "ALL"
  }
  tags = local.dynamodb_tags
}