# Lab 05 — Synapse Analytics

AWS Equivalent: Redshift + Athena + Glue
Cost: ~$10

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
Redshift                →  Synapse Dedicated SQL Pool
Athena                  →  Synapse Serverless SQL Pool
Glue Data Catalog       →  Synapse Workspace + Lake Database
Redshift Spectrum       →  Synapse external tables
```

Synapse = unified analytics platform (SQL + Spark + Pipelines in one workspace).

## Hands-On

### 1. Create Synapse Workspace
```bash
az group create --name rg-data-lab05 --location australiaeast

# Create ADLS for Synapse
az storage account create \
  --resource-group rg-data-lab05 \
  --name stsynapse$(date +%s | tail -c 8) \
  --sku Standard_LRS --kind StorageV2 --hns true

export SA_NAME=$(az storage account list --resource-group rg-data-lab05 --query [0].name -o tsv)

# Create filesystem for Synapse
az storage fs create --name synapse --account-name $SA_NAME \
  --auth-mode login

# Create Synapse workspace
az synapse workspace create \
  --resource-group rg-data-lab05 \
  --name syn-lab05-$(date +%s | tail -c 8) \
  --storage-account $SA_NAME \
  --file-system synapse \
  --sql-admin-login sqladmin \
  --sql-admin-login-password 'P@ssw0rd1234!' \
  --location australiaeast

export SYN_NAME=$(az synapse workspace list --resource-group rg-data-lab05 --query [0].name -o tsv)

# Open firewall
az synapse workspace firewall-rule create \
  --resource-group rg-data-lab05 \
  --workspace-name $SYN_NAME \
  --name AllowAll \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255
```

### 2. Serverless SQL Pool (like Athena — query files directly)
```bash
# Upload sample data
echo 'id,product,amount
1,Laptop,999
2,Phone,599
3,Tablet,399' > /tmp/products.csv

export SA_KEY=$(az storage account keys list --account-name $SA_NAME --query [0].value -o tsv)
az storage fs file upload --source /tmp/products.csv --path data/products.csv \
  --file-system synapse --account-name $SA_NAME --account-key $SA_KEY
```

In Synapse Studio (https://web.azuresynapse.net):
```sql
-- Query CSV directly (like Athena — no table needed)
SELECT * FROM OPENROWSET(
    BULK 'https://<account>.dfs.core.windows.net/synapse/data/products.csv',
    FORMAT = 'CSV', HEADER_ROW = TRUE
) AS rows;
```

### 3. Serverless vs Dedicated

| Feature | Serverless SQL Pool | Dedicated SQL Pool |
|---------|--------------------|--------------------|
| AWS equiv | Athena | Redshift |
| Pricing | Pay per TB scanned | Pay per DWU (always on) |
| Use case | Ad-hoc queries | Heavy warehouse workloads |
| For learning | ✅ Use this | ❌ Too expensive |

## Cleanup
```bash
az group delete --name rg-data-lab05 --yes --no-wait
```

## Key Takeaways
- Synapse Serverless SQL = Athena (query files in place, pay per scan)
- Synapse Dedicated SQL = Redshift (provisioned warehouse — expensive)
- Use Serverless for learning — it's nearly free for small data
- Synapse Studio = web IDE for SQL, Spark, and pipeline authoring
- In practice, most teams use Databricks for Spark + Synapse Serverless for SQL
