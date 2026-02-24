# Track 1: Senior Azure Cloud Engineer

Target Certs: AZ-104 (Admin), AZ-305 (Architect)
Estimated Cost: ~$80

## Lab Order

| # | Lab | AWS Equivalent | Est. Cost |
|---|-----|---------------|-----------|
| 1 | [Resource Groups & RBAC](lab01-resource-groups/) | IAM + Tagging | Free |
| 2 | [VNet & Networking](lab02-networking/) | VPC, Subnets, SG, NACLs | ~$5 |
| 3 | [Virtual Machines & Availability](lab03-virtual-machines/) | EC2, ASG, ALB | ~$10 |
| 4 | [Storage Accounts & Blob](lab04-storage/) | S3 | ~$2 |
| 5 | [Azure SQL & CosmosDB](lab05-databases/) | RDS, DynamoDB | ~$10 |
| 6 | [Azure Functions & Logic Apps](lab06-serverless/) | Lambda, Step Functions | ~$3 |
| 7 | [AKS (Kubernetes)](lab07-aks/) | EKS | ~$20 |
| 8 | [Azure Monitor & Log Analytics](lab08-monitoring/) | CloudWatch | ~$5 |
| 9 | [Bicep & ARM Templates](lab09-iac/) | CloudFormation | Free |
| 10 | [Azure DevOps & CI/CD](lab10-devops/) | CodePipeline, CodeBuild | Free tier |

⚠️ Run `az group delete --name <rg-name> --yes --no-wait` after each lab!
