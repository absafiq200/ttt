output "dynamo_table_hash_arn" {
    description = "dynamodb table(primary key) arn"
    value = aws_dynamodb_table.dynamodb_hash.arn
}

output "dynamo_table_hash_name" {
    description = "dynamodb table(primary key) name"
    value = aws_dynamodb_table.dynamodb_hash.id  
}