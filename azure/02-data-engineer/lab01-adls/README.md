# Lab 01 — ADLS Gen2 (Azure Data Lake Storage)

AWS Equivalent: S3 + Lake Formation + Glue Catalog
Cost: ~$2

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
S3 (data lake)          →  ADLS Gen2 (Storage Account with HNS)
Lake Formation          →  ADLS Gen2 ACLs + Unity Catalog
Glue Data Catalog       →  Unity Catalog / Hive Metastore
s3://bucket/path        →  abfss://container@account.dfs.core.windows.net/path
```

ADLS Gen2 = Storage Account with Hierarchical Namespace (HNS) enabled.
This gives you real directory operations (rename, delete folder) — S3 doesn't have this.

## Hands-On

### 1. Create ADLS Gen2
```bash
az group create --name rg-data-lab01 --location australiaeast

# Create storage account with HNS (hierarchical namespace = data lake)
az storage account create \
  --resource-group rg-data-lab01 \
  --name adlslab01$(date +%s | tail -c 8) \
  --sku Standard_LRS \
  --kind StorageV2 \
  --hns true

export ADLS_NAME=$(az storage account list --resource-group rg-data-lab01 --query [0].name -o tsv)
```

### 2. Create Containers (Bronze/Silver/Gold — Medallion Architecture)
```bash
export ADLS_KEY=$(az storage account keys list --account-name $ADLS_NAME --query [0].value -o tsv)

# Create medallion layers
az storage fs create --name bronze --account-name $ADLS_NAME --account-key $ADLS_KEY
az storage fs create --name silver --account-name $ADLS_NAME --account-key $ADLS_KEY
az storage fs create --name gold --account-name $ADLS_NAME --account-key $ADLS_KEY

# Create directories
az storage fs directory create --name raw/2024/01 -f bronze --account-name $ADLS_NAME --account-key $ADLS_KEY

# Upload sample data
echo 'id,name,amount,date
1,Alice,100,2024-01-01
2,Bob,200,2024-01-02
3,Charlie,150,2024-01-03' > /tmp/sales.csv

az storage fs file upload \
  --source /tmp/sales.csv \
  --path raw/2024/01/sales.csv \
  --file-system bronze \
  --account-name $ADLS_NAME \
  --account-key $ADLS_KEY

# List files
az storage fs file list --file-system bronze --account-name $ADLS_NAME --account-key $ADLS_KEY -o table
```

### 3. Access via ABFSS URL
```
# This is how Databricks/Spark accesses ADLS:
abfss://bronze@<account>.dfs.core.windows.net/raw/2024/01/sales.csv

# Equivalent to:
s3://my-data-lake/raw/2024/01/sales.csv
```

## Cleanup
```bash
az group delete --name rg-data-lab01 --yes --no-wait
```

## Key Takeaways
- ADLS Gen2 = Storage Account + HNS (hierarchical namespace)
- HNS gives real directory operations — better than S3 for data lakes
- Medallion architecture: Bronze (raw) → Silver (cleaned) → Gold (aggregated)
- ABFSS protocol = how Spark/Databricks reads from ADLS
- ADLS is the foundation of every Azure data platform
