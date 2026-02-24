# Lab 03 — Databricks Workspace

AWS Equivalent: EMR + Glue + Jupyter Notebooks
Cost: ~$25 (⚠️ terminate clusters immediately after use!)

## Concepts

```
AWS                     →  Azure Databricks
─────────────────────────────────────────
EMR Cluster             →  Databricks Cluster
Glue Spark Jobs         →  Databricks Notebooks / Jobs
Glue Data Catalog       →  Unity Catalog
EMR Notebooks           →  Databricks Notebooks
SageMaker Notebooks     →  Databricks Notebooks (ML too)
S3                      →  ADLS Gen2 (mounted or direct access)
```

## Hands-On

### 1. Create Databricks Workspace
```bash
az group create --name rg-data-lab03 --location australiaeast

# Create Databricks workspace
az databricks workspace create \
  --resource-group rg-data-lab03 \
  --name dbw-lab03 \
  --location australiaeast \
  --sku trial

# Get workspace URL
az databricks workspace show \
  --resource-group rg-data-lab03 \
  --name dbw-lab03 \
  --query workspaceUrl -o tsv

# Open in browser: https://<workspace-url>
```

### 2. Create a Cluster (⚠️ SMALLEST POSSIBLE)
In the Databricks UI:
- Compute → Create Cluster
- **Name**: lab-cluster
- **Policy**: Unrestricted
- **Node type**: Standard_DS3_v2 (or smallest available)
- **Workers**: 0 (single node mode) ← IMPORTANT for cost saving
- **Auto-termination**: 10 minutes ← CRITICAL
- **Databricks Runtime**: Latest LTS

### 3. First Notebook
Create a notebook in Databricks and run:
```python
# Read CSV from DBFS (Databricks File System)
# Upload sales.csv via UI first, or:

data = [
    (1, "Alice", 100, "2024-01-01"),
    (2, "Bob", 200, "2024-01-02"),
    (3, "Charlie", 150, "2024-01-03"),
]
df = spark.createDataFrame(data, ["id", "name", "amount", "date"])
df.show()

# Write as Delta table
df.write.format("delta").mode("overwrite").saveAsTable("sales")

# Query it
spark.sql("SELECT * FROM sales WHERE amount > 100").show()
```

### 4. Connect to ADLS Gen2
```python
# In Databricks notebook — direct access using account key
spark.conf.set(
    "fs.azure.account.key.<storage-account>.dfs.core.windows.net",
    "<access-key>"
)

# Read from ADLS
df = spark.read.csv("abfss://bronze@<account>.dfs.core.windows.net/raw/sales.csv",
                     header=True, inferSchema=True)
df.show()
```

## Cleanup
```bash
# FIRST: Terminate cluster in Databricks UI!
az group delete --name rg-data-lab03 --yes --no-wait
```

## Key Takeaways
- Databricks = Spark + Notebooks + ML + SQL — all in one platform
- ALWAYS use single-node clusters and 10-min auto-termination for learning
- Trial SKU gives you 14 days of Databricks premium features
- Unity Catalog = centralized governance (like Lake Formation + Glue Catalog)
- Databricks on Azure is the #1 data platform choice for enterprises
