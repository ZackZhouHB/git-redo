# Lab 05 — Azure SQL & Cosmos DB

AWS Equivalent: RDS, Aurora, DynamoDB
Cost: ~$10

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
RDS (SQL)               →  Azure SQL Database
Aurora                  →  Azure SQL Hyperscale
RDS Multi-AZ            →  Azure SQL Geo-Replication
DynamoDB                →  Cosmos DB
DynamoDB Streams        →  Cosmos DB Change Feed
ElastiCache (Redis)     →  Azure Cache for Redis
```

## Hands-On

### 1. Azure SQL Database (like RDS)
```bash
az group create --name rg-lab05 --location australiaeast

# Create SQL Server (logical server — like RDS instance endpoint)
az sql server create \
  --resource-group rg-lab05 \
  --name sql-lab05-$(date +%s | tail -c 8) \
  --admin-user sqladmin \
  --admin-password 'P@ssw0rd1234!' \
  --location australiaeast

export SQL_SERVER=$(az sql server list --resource-group rg-lab05 --query [0].name -o tsv)

# Create database (Basic tier — cheapest, ~$5/month)
az sql db create \
  --resource-group rg-lab05 \
  --server $SQL_SERVER \
  --name mydb \
  --edition Basic \
  --capacity 5

# Allow your IP through firewall (like RDS Security Group)
az sql server firewall-rule create \
  --resource-group rg-lab05 \
  --server $SQL_SERVER \
  --name AllowMyIP \
  --start-ip-address $(curl -s ifconfig.me) \
  --end-ip-address $(curl -s ifconfig.me)

# List databases
az sql db list --resource-group rg-lab05 --server $SQL_SERVER -o table
```

### 2. Cosmos DB (like DynamoDB)
```bash
# Create Cosmos DB account (NoSQL API — closest to DynamoDB)
az cosmosdb create \
  --resource-group rg-lab05 \
  --name cosmos-lab05-$(date +%s | tail -c 8) \
  --kind GlobalDocumentDB \
  --default-consistency-level Session \
  --enable-free-tier true

export COSMOS_NAME=$(az cosmosdb list --resource-group rg-lab05 --query [0].name -o tsv)

# Create database
az cosmosdb sql database create \
  --resource-group rg-lab05 \
  --account-name $COSMOS_NAME \
  --name mydb

# Create container (like DynamoDB table)
az cosmosdb sql container create \
  --resource-group rg-lab05 \
  --account-name $COSMOS_NAME \
  --database-name mydb \
  --name users \
  --partition-key-path "/userId" \
  --throughput 400
```

## Cleanup
```bash
az group delete --name rg-lab05 --yes --no-wait
```

## Key Takeaways
- Azure SQL = RDS for SQL Server (also supports PostgreSQL, MySQL as separate services)
- Cosmos DB = DynamoDB but multi-model (SQL, MongoDB, Cassandra, Gremlin, Table APIs)
- Cosmos DB free tier: 1000 RU/s + 25GB — use `--enable-free-tier true`
- Azure SQL Basic tier is cheapest for learning (~$5/month)
- Cosmos DB partition key = DynamoDB partition key (same concept)
