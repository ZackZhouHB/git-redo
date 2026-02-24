# Lab 09 — Bicep & ARM Templates (Infrastructure as Code)

AWS Equivalent: CloudFormation, CDK
Cost: Free (just deploying templates)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
CloudFormation (JSON/YAML) → ARM Templates (JSON) — verbose, legacy
CDK                     →  Bicep (DSL that compiles to ARM) — recommended
cfn-lint                →  bicep build (validation)
aws cloudformation deploy → az deployment group create
Stacks                  →  Deployments
Nested Stacks           →  Modules
```

Bicep is the way to go. ARM JSON is like writing raw CloudFormation JSON — painful.

## Hands-On

### 1. Your First Bicep Template
```bash
mkdir -p /tmp/bicep-lab09 && cd /tmp/bicep-lab09

cat > main.bicep << 'EOF'
param location string = resourceGroup().location
param storageName string = 'stbicep${uniqueString(resourceGroup().id)}'

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageName
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

output storageId string = storageAccount.id
output storageName string = storageAccount.name
EOF
```

### 2. Deploy
```bash
az group create --name rg-lab09 --location australiaeast

# Deploy Bicep (like: aws cloudformation deploy)
az deployment group create \
  --resource-group rg-lab09 \
  --template-file main.bicep

# Show outputs (like: aws cloudformation describe-stacks)
az deployment group show \
  --resource-group rg-lab09 \
  --name main \
  --query properties.outputs -o json
```

### 3. Bicep with Parameters (like CFN Parameters)
```bash
cat > vnet.bicep << 'EOF'
param vnetName string
param addressPrefix string = '10.0.0.0/16'
param location string = resourceGroup().location

resource vnet 'Microsoft.Network/virtualNetworks@2023-05-01' = {
  name: vnetName
  location: location
  properties: {
    addressSpace: { addressPrefixes: [addressPrefix] }
    subnets: [
      { name: 'web', properties: { addressPrefix: '10.0.1.0/24' } }
      { name: 'app', properties: { addressPrefix: '10.0.2.0/24' } }
    ]
  }
}

output vnetId string = vnet.id
EOF

az deployment group create \
  --resource-group rg-lab09 \
  --template-file vnet.bicep \
  --parameters vnetName=vnet-lab09
```

### 4. Bicep Modules (like Nested Stacks)
```bash
mkdir modules

cat > modules/storage.bicep << 'EOF'
param name string
param location string

resource sa 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: name
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

output id string = sa.id
EOF

cat > main-with-module.bicep << 'EOF'
param location string = resourceGroup().location

module storage 'modules/storage.bicep' = {
  name: 'storageDeployment'
  params: {
    name: 'stmod${uniqueString(resourceGroup().id)}'
    location: location
  }
}
EOF

az deployment group create \
  --resource-group rg-lab09 \
  --template-file main-with-module.bicep
```

### 5. Terraform with Azure (since you already know TF)
```bash
cat > main.tf << 'EOF'
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "rg-terraform-lab09"
  location = "australiaeast"
}

resource "azurerm_storage_account" "example" {
  name                     = "sttflab09${substr(md5(azurerm_resource_group.example.id), 0, 8)}"
  resource_group_name      = azurerm_resource_group.example.name
  location                 = azurerm_resource_group.example.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}
EOF

# terraform init && terraform plan && terraform apply
```

## Cleanup
```bash
az group delete --name rg-lab09 --yes --no-wait
```

## Key Takeaways
- Bicep = Azure-native IaC (like CDK but simpler, compiles to ARM JSON)
- ARM Templates = raw JSON (like raw CloudFormation — avoid if possible)
- Terraform works great with Azure — just use `azurerm` provider
- `az deployment group create` = `aws cloudformation deploy`
- Bicep modules = nested stacks / CDK constructs
