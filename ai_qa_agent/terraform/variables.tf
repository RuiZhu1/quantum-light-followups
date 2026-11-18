variable "aws_region" {
  description = "AWS region for deployment"
  type        = string
  default     = "us-east-1"
}

variable "container_image" {
  description = "Container image URI for the AI QA Agent"
  type        = string
}

variable "ai_qa_client" {
  description = "LLM client to use (placeholder, openai, anthropic)"
  type        = string
  default     = "placeholder"
}

variable "openai_model" {
  description = "OpenAI model name"
  type        = string
  default     = "gpt-4o-mini"
}

variable "openai_api_key_secret_arn" {
  description = "ARN of the AWS Secrets Manager secret containing the OpenAI API key"
  type        = string
}

variable "ecs_execution_role_arn" {
  description = "ARN of the ECS task execution role"
  type        = string
}

variable "subnets" {
  description = "List of subnet IDs for the ECS service"
  type        = list(string)
}

variable "security_groups" {
  description = "List of security group IDs for the ECS service"
  type        = list(string)
}
