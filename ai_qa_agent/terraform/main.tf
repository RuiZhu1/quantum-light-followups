# Example Terraform configuration to deploy the AI QA Agent API on AWS ECS Fargate.
# This is intentionally minimal and educational; adapt VPC, subnets, and IAM to your environment.

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "ai_qa_agent" {
  name = "ai-qa-agent-cluster"
}

resource "aws_ecs_task_definition" "ai_qa_agent" {
  family                   = "ai-qa-agent"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = var.ecs_execution_role_arn

  container_definitions = jsonencode([
    {
      name  = "ai-qa-agent"
      image = var.container_image
      portMappings = [
        {
          containerPort = 8000
          hostPort      = 8000
        }
      ]
      environment = [
        { name = "AI_QA_CLIENT", value = var.ai_qa_client },
        { name = "AI_QA_OPENAI_MODEL", value = var.openai_model },
      ]
      secrets = [
        { name = "AI_QA_OPENAI_API_KEY", valueFrom = var.openai_api_key_secret_arn },
      ]
      healthCheck = {
        command     = ["CMD-SHELL", "python -c 'import urllib.request; urllib.request.urlopen(\"http://localhost:8000/health\")' || exit 1"]
        interval    = 30
        timeout     = 5
        retries     = 3
        startPeriod = 10
      }
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.ai_qa_agent.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ai-qa-agent"
        }
      }
    }
  ])
}

resource "aws_cloudwatch_log_group" "ai_qa_agent" {
  name              = "/ecs/ai-qa-agent"
  retention_in_days = 7
}

resource "aws_ecs_service" "ai_qa_agent" {
  name            = "ai-qa-agent-service"
  cluster         = aws_ecs_cluster.ai_qa_agent.id
  task_definition = aws_ecs_task_definition.ai_qa_agent.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = var.subnets
    security_groups  = var.security_groups
    assign_public_ip = true
  }
}
