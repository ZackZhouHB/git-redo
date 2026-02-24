# Lab 10 — Azure DevOps & CI/CD

AWS Equivalent: CodeCommit, CodeBuild, CodePipeline, CodeDeploy
Cost: Free tier (5 users, 1 parallel job)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
CodeCommit              →  Azure Repos (or just use GitHub)
CodeBuild               →  Azure Pipelines (build stage)
CodePipeline            →  Azure Pipelines (full pipeline)
CodeDeploy              →  Azure Pipelines (deploy stage)
CodeArtifact            →  Azure Artifacts
GitHub Actions          →  Azure Pipelines (YAML-based, very similar)
```

## Hands-On

### 1. Azure DevOps vs GitHub Actions
Both work great with Azure. GitHub Actions is more common now.

**GitHub Actions for Azure** (recommended if you use GitHub):
```yaml
# .github/workflows/deploy.yml
name: Deploy to Azure
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - run: |
          az group create --name rg-cicd --location australiaeast
          az deployment group create \
            --resource-group rg-cicd \
            --template-file main.bicep
```

### 2. Create Service Principal for CI/CD
```bash
# Create SP with Contributor role (for pipelines)
az ad sp create-for-rbac --name sp-cicd \
  --role Contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv) \
  --sdk-auth

# Output goes into GitHub Secrets as AZURE_CREDENTIALS
```

### 3. Azure CLI in Pipelines
```bash
# Common pipeline commands
az deployment group create --resource-group rg-app --template-file main.bicep  # Deploy infra
az acr build --registry myacr --image myapp:$BUILD_ID .                        # Build container
az aks get-credentials --resource-group rg-app --name my-aks                   # Get k8s creds
kubectl apply -f k8s/                                                           # Deploy to AKS
```

## Cleanup
```bash
az ad sp delete --id $(az ad sp list --display-name sp-cicd --query [0].id -o tsv) 2>/dev/null
```

## Key Takeaways
- Azure Pipelines ≈ GitHub Actions (YAML-based CI/CD)
- GitHub Actions + Azure is the most popular combo now
- Service Principal with `--sdk-auth` output = ready for CI/CD secrets
- Azure DevOps is a full platform (repos, boards, pipelines, artifacts, test plans)
- Free tier: 5 users, 1 Microsoft-hosted parallel job
