# Lab 02 — Azure Data Factory (ADF)

AWS Equivalent: Glue ETL + Step Functions + EventBridge Scheduler
Cost: ~$5

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
Glue ETL Jobs           →  ADF Data Flows / Mapping Data Flows
Glue Crawlers           →  ADF Linked Services + Datasets
Step Functions          →  ADF Pipelines (orchestration)
EventBridge Scheduler   →  ADF Triggers
Glue Connections        →  ADF Linked Services
```

ADF is primarily an orchestration tool — it moves and transforms data between sources.

## Hands-On

### 1. Create Data Factory
```bash
az group create --name rg-data-lab02 --location australiaeast

az datafactory create \
  --resource-group rg-data-lab02 \
  --factory-name adf-lab02-$(date +%s | tail -c 8) \
  --location australiaeast

export ADF_NAME=$(az datafactory list --resource-group rg-data-lab02 --query [0].name -o tsv)
```

### 2. Create Linked Services (connections)
```bash
# Create a storage account as source/sink
az storage account create \
  --resource-group rg-data-lab02 \
  --name stadf$(date +%s | tail -c 8) \
  --sku Standard_LRS --kind StorageV2 --hns true

export SA_NAME=$(az storage account list --resource-group rg-data-lab02 \
  --query "[?starts_with(name,'stadf')].name" -o tsv)
export SA_KEY=$(az storage account keys list --account-name $SA_NAME --query [0].value -o tsv)

# Create linked service via ADF (best done in portal for visual experience)
echo "Open: https://adf.azure.com/en/home"
echo "Select factory: $ADF_NAME"
```

### 3. Key ADF Concepts
```
Pipeline     = Workflow (like Step Functions state machine)
Activity     = A step in the pipeline (Copy, Databricks, SQL, etc.)
Dataset      = Pointer to data (like Glue table reference)
Linked Svc   = Connection string (like Glue connection)
Trigger      = Schedule or event (like EventBridge rule)
Integration Runtime = Compute that runs activities (like Glue workers)
```

### 4. Create a Simple Pipeline via CLI
```bash
# Create a pipeline with a copy activity (JSON definition)
cat > /tmp/pipeline.json << EOF
{
  "activities": [
    {
      "name": "WaitActivity",
      "type": "Wait",
      "typeProperties": { "waitTimeInSeconds": 5 }
    }
  ]
}
EOF

az datafactory pipeline create \
  --resource-group rg-data-lab02 \
  --factory-name $ADF_NAME \
  --name pipeline-demo \
  --pipeline @/tmp/pipeline.json

# Trigger a run
az datafactory pipeline create-run \
  --resource-group rg-data-lab02 \
  --factory-name $ADF_NAME \
  --name pipeline-demo
```

## Cleanup
```bash
az group delete --name rg-data-lab02 --yes --no-wait
```

## Key Takeaways
- ADF = orchestration engine (Glue + Step Functions combined)
- Best experienced through the portal UI (visual pipeline designer)
- Linked Services = connections, Datasets = data pointers
- ADF + Databricks is the most common Azure data pattern
- Integration Runtime = where compute happens (Azure-hosted or self-hosted)
