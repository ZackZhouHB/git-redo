# Azure Learning Path — From AWS Expert to Azure Expert

Budget: $200 free trial credit (30 days)
Background: Senior AWS engineer (EC2 → EKS, CloudFormation, CDK, Terraform)

## 3 Career Tracks

| # | Track | Folder | Key Certifications |
|---|-------|--------|-------------------|
| 1 | Senior Cloud Engineer | `01-cloud-engineer/` | AZ-104, AZ-305 |
| 2 | Senior Data Engineer (Databricks) | `02-data-engineer/` | DP-203, Databricks Certified |
| 3 | Senior AI Engineer | `03-ai-engineer/` | AI-102, AI-900 |

## Budget Strategy (~$200)

| Track | Estimated Cost | Notes |
|-------|---------------|-------|
| Cloud Engineer | ~$80 | VMs, AKS, networking — shut down after each lab |
| Data Engineer | ~$70 | Databricks workspace + storage — use smallest clusters |
| AI Engineer | ~$50 | Azure OpenAI + Cognitive Services — pay-per-call |

**Golden Rule**: Always `az group delete` after each lab to avoid surprise charges.

## Quick Reference: AWS → Azure

```
AWS Account        → Azure Subscription
IAM                → Entra ID (Azure AD)
CloudFormation     → ARM/Bicep
VPC                → VNet
EC2                → Virtual Machines
EKS                → AKS
S3                 → Blob Storage
RDS                → Azure SQL
Lambda             → Azure Functions
CloudWatch         → Azure Monitor
Route53            → Azure DNS
SQS/SNS            → Service Bus / Event Grid
Glue               → Data Factory / Databricks
SageMaker          → Azure ML / Azure OpenAI
```
