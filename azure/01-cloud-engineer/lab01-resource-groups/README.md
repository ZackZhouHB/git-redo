# Lab 01 — Resource Groups, Subscriptions & RBAC

AWS Equivalent: IAM Users/Roles/Policies + Account structure
Cost: Free

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
AWS Account             →  Subscription
AWS Organizations       →  Management Groups
IAM Policies            →  Azure RBAC (Role-Based Access Control)
IAM Roles               →  Azure Roles (built-in or custom)
IAM Users               →  Entra ID Users
IAM Groups              →  Entra ID Groups
Resource Tags           →  Resource Groups (logical container) + Tags
```

Key difference: In Azure, EVERY resource must belong to a Resource Group.
Think of it as a mandatory folder for your resources.

## Hands-On

### 1. Create a Resource Group
```bash
# Like creating a "project folder" — no AWS equivalent
az group create --name rg-lab01 --location australiaeast

# List all resource groups
az group list -o table
```

### 2. Understand Scopes (Management Group → Subscription → RG → Resource)
```bash
# Show your subscription
az account show -o table

# List all subscriptions
az account list -o table
```

### 3. RBAC — Assign Roles
```bash
# List built-in roles (like AWS managed policies)
az role definition list --output table --query "[?contains(roleName,'Contributor')]"

# Key built-in roles:
# Owner         = AdministratorAccess
# Contributor   = PowerUserAccess (no RBAC management)
# Reader        = ReadOnlyAccess

# List your role assignments
az role assignment list --assignee $(az ad signed-in-user show --query id -o tsv) -o table
```

### 4. Create a Service Principal (like IAM User with access keys)
```bash
# Create SP for automation (like creating an IAM user for CI/CD)
az ad sp create-for-rbac --name sp-lab01 --role Contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/rg-lab01

# This outputs appId (client_id), password (client_secret), tenant
# Used for Terraform, CI/CD pipelines, etc.
```

### 5. Resource Locks (no direct AWS equivalent)
```bash
# Prevent accidental deletion
az lock create --name no-delete --resource-group rg-lab01 --lock-type CanNotDelete

# List locks
az lock list --resource-group rg-lab01 -o table

# Remove lock before cleanup
az lock delete --name no-delete --resource-group rg-lab01
```

## Cleanup
```bash
az ad sp delete --id $(az ad sp list --display-name sp-lab01 --query [0].id -o tsv)
az group delete --name rg-lab01 --yes --no-wait
```

## Key Takeaways
- Resource Groups are mandatory — plan your naming convention early
- RBAC is scope-based (Management Group > Subscription > RG > Resource)
- Service Principals = service accounts for automation
- Entra ID (Azure AD) is the identity backbone — not a separate service like IAM
