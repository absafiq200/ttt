/* pinpoint campaign table */
variable "pinpoint_campaign_table_name" {
  description = "pinpoint campaign table name"
  type        = string
}
variable "pinpoint_campaign_table_billing_mode" {
  description = "pinpoint campaign table billing mode"
  type        = string
}
variable "pinpoint_campaign_table_hash_key" {
  description = "pinpoint campaign table hash key"
  type        = string
}
variable "pinpoint_campaign_table_hash_key_column_type" {
  description = "pinpoint campaign table hash key type"
  type        = string
}

/* Pinpoint campaign metadata table */
variable "pinpoint_campaign_meta_table_name" {
  description = "pinpoint campaign metadata table name"
  type        = string
}
variable "pinpoint_campaign_meta_billing_mode" {
  description = "pinpoint campaign metadata table billing mode"
  type        = string
}
variable "pinpoint_campaign_meta_hash_key" {
  description = "pinpoint campaign metadata table hash key"
  type        = string
}
variable "pinpoint_campaign_meta_hash_key_column_type" {
  description = "pinpoint campaign metadata table hash key type"
  type        = string
}

variable "pinpoint_campaign_template_table_name" {
  description = "Pinpoint campaign template table"
  type =  string
}
variable "pinpoint_campaign_template_billing_mode" {
  description = "pinpoint campaign metadata table billing mode"
  type        = string
}
variable "pinpoint_campaign_template_hash_key" {
  description = "pinpoint campaign metadata table hash key"
  type        = string
}
variable "pinpoint_campaign_template_hash_key_column_type" {
  description = "pinpoint campaign metadata table hash key type"
  type        = string
}


