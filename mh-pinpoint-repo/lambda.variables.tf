variable "trust_role" {
  description = "Trust relationship identifier or service name"
  type        = list(string)
  default     = ["lambda.amazonaws.com"]
}
variable "sts_assume_role" {
  type        = string
  description = "Trust relationships assume role"
  default     = "lambda.amazonaws.com"
}
variable "sts_assume_service" {
  type        = string
  description = "Trust relationships assume type"
  default     = "Service"
}
variable "iam_role_path" {
  description = "EC2 Backup Monitor IAM role path"
  type        = string
  default     = "/"
}

variable "python_runtime_38" {
  description = "python lambda runtime"
  type        = string
  default     = "python3.8"
}

variable "memory_256" {
  description = "python lambda runtime memory"
  type        = number
  default     = 256
}

variable "template_lambda_timeout" {
  description = "python lambda timeout in seconds"
  type        = number
  default     = 60
}

variable "lambda_zip_file" {
 description = "python lambda source file type"
  type        = string
  default     = "zip" 
}

variable "campaign_crud_lambda_timeout" {
  description = "python lambda timeout in seconds"
  type        = number
  default     = 60
}

variable "campaign_report_lambda_timeout" {
  description = "python lambda timeout in seconds"
  type        = number
  default     = 60
}

variable "campaign_segment_lambda_timeout" {
  description = "python lambda timeout in seconds"
  type        = number
  default     = 60
}

variable "campaign_start_lambda_timeout" {
  description = "python lambda timeout in seconds"
  type        = number
  default     = 60
}

variable "campaign_stop_lambda_timeout" {
  description = "python lambda timeout in seconds"
  type        = number
  default     = 60
}