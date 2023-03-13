variable "api_name" {
  description = "Api Gateway Name"
  type        = string
  default     = "Pinpoint-Campaign-Api"
}
variable "protocol_type" {
  description = "Api Gateway protocol type"
  type        = string
  default     = "HTTP"
}

variable "endpoint_type" {
  description = "domain name endpoint type"
  type        = string
  default     = "REGIONAL"
}
variable "cors_configuration" {
  type = any
  default = {
    allow_headers  = ["content-type", "x-amz-date", "authorization", "x-api-key", "x-amz-security-token", "x-amz-user-agent"]
    allow_methods  = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_origins  = ["*"]
    max_age        = 300
    expose_headers = ["Date", "x-api-id"]
  }
}