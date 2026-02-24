# Lab 07 — End-to-End Data Pipeline

AWS Equivalent: Full data platform (S3 + Glue + EMR + Redshift + QuickSight)
Cost: ~$5 (reuse existing resources)

## Architecture

```
Source Data → Event Hubs → ADLS Bronze → Databricks (Silver/Gold) → Synapse SQL → Power BI
                              ↑
                    Data Factory (orchestration)
```

AWS equivalent:
```
Source → Kinesis → S3 Raw → Glue/EMR (Transform) → Redshift → QuickSight
                              ↑
                    Step Functions (orchestration)
```

## The Azure Data Platform Stack

| Layer | Service | AWS Equivalent |
|-------|---------|---------------|
| Ingestion | Event Hubs, Data Factory | Kinesis, Glue |
| Storage | ADLS Gen2 | S3 |
| Processing | Databricks | EMR / Glue Spark |
| Warehouse | Synapse Serverless | Athena |
| Governance | Unity Catalog | Lake Formation |
| Orchestration | Data Factory / Databricks Workflows | Step Functions / MWAA |
| BI | Power BI | QuickSight |

## Pipeline Design (Databricks Notebook)

### Step 1: Ingest to Bronze
```python
# Simulate ingestion — in production this comes from Event Hubs or ADF
raw_orders = [
    (1, "Alice", "Laptop", 999.99, "2024-01-01", "au"),
    (2, "Bob", "Phone", 599.99, "2024-01-01", "us"),
    (3, "Alice", "Tablet", 399.99, "2024-01-02", "au"),
    (4, "Dave", "Laptop", 999.99, "2024-01-02", "uk"),
    (5, "Eve", "Phone", 599.99, "2024-01-03", "au"),
]
df = spark.createDataFrame(raw_orders, ["id", "customer", "product", "amount", "date", "region"])
df.write.format("delta").mode("overwrite").saveAsTable("bronze.orders")
```

### Step 2: Clean to Silver
```python
from pyspark.sql.functions import col, to_date, upper

df_silver = (spark.table("bronze.orders")
    .withColumn("date", to_date(col("date")))
    .withColumn("region", upper(col("region")))
    .dropDuplicates(["id"])
    .filter(col("amount") > 0)
)
df_silver.write.format("delta").mode("overwrite").saveAsTable("silver.orders")
```

### Step 3: Aggregate to Gold
```python
from pyspark.sql.functions import sum, count, avg

# Revenue by region
(spark.table("silver.orders")
    .groupBy("region")
    .agg(sum("amount").alias("revenue"), count("id").alias("orders"), avg("amount").alias("avg_order"))
    .write.format("delta").mode("overwrite").saveAsTable("gold.revenue_by_region"))

# Revenue by product
(spark.table("silver.orders")
    .groupBy("product")
    .agg(sum("amount").alias("revenue"), count("id").alias("orders"))
    .write.format("delta").mode("overwrite").saveAsTable("gold.revenue_by_product"))
```

### Step 4: Query from Synapse Serverless
```sql
-- In Synapse Studio, query the Gold tables via external tables or OPENROWSET
SELECT * FROM gold.revenue_by_region ORDER BY revenue DESC;
```

## Key Takeaways
- ADLS + Databricks + Data Factory = the standard Azure data stack
- Medallion (Bronze → Silver → Gold) is the universal pattern
- Data Factory orchestrates, Databricks transforms, Synapse queries
- This architecture handles 90% of enterprise data engineering needs
- Power BI connects directly to Gold layer for dashboards
