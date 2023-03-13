resource "aws_dynamodb_table" "dynamodb_hash" {    
    name = var.table_name   
    billing_mode = var.billing_mode
    hash_key = var.hash_key_column   
    point_in_time_recovery {
      enabled = true
    }
    attribute {
      name = var.hash_key_column
      type = var.hash_key_column_type
    }
    tags = var.tags
}

