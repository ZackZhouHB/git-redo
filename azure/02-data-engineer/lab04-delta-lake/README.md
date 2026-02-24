# Lab 04 — Delta Lake & Medallion Architecture

AWS Equivalent: Iceberg/Hudi tables on S3 with Glue Catalog
Cost: ~$15 (Databricks cluster time)

## Concepts

```
AWS                     →  Azure / Databricks
─────────────────────────────────────────
Iceberg / Hudi          →  Delta Lake (default in Databricks)
S3 + Glue Catalog       →  ADLS + Unity Catalog
Athena queries          →  Databricks SQL
Lake Formation          →  Unity Catalog permissions
```

Delta Lake = open-source storage layer that adds ACID transactions to data lakes.
Medallion = Bronze (raw) → Silver (cleaned) → Gold (business-ready).

## Hands-On (Databricks Notebook)

### 1. Bronze Layer — Ingest Raw Data
```python
# Simulate raw data ingestion
from pyspark.sql.types import *

schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("product", StringType()),
    StructField("amount", DoubleType()),
    StructField("order_date", StringType()),
])

raw_data = [
    (1, "Alice", "Laptop", 999.99, "2024-01-01"),
    (2, "Bob", "Phone", 599.99, "2024-01-01"),
    (3, "Alice", "Tablet", 399.99, "2024-01-02"),
    (4, None, "Laptop", 999.99, "2024-01-02"),       # null customer
    (5, "Charlie", "Phone", -50.0, "2024-01-03"),     # negative amount
    (2, "Bob", "Phone", 599.99, "2024-01-01"),        # duplicate
]

df_bronze = spark.createDataFrame(raw_data, schema)
df_bronze.write.format("delta").mode("overwrite").saveAsTable("bronze_orders")
df_bronze.show()
```

### 2. Silver Layer — Clean & Deduplicate
```python
from pyspark.sql.functions import col

df_silver = (spark.table("bronze_orders")
    .dropna(subset=["customer"])           # remove nulls
    .filter(col("amount") > 0)             # remove invalid amounts
    .dropDuplicates(["order_id"])          # deduplicate
)

df_silver.write.format("delta").mode("overwrite").saveAsTable("silver_orders")
df_silver.show()
```

### 3. Gold Layer — Business Aggregations
```python
from pyspark.sql.functions import sum, count

df_gold = (spark.table("silver_orders")
    .groupBy("product")
    .agg(
        sum("amount").alias("total_revenue"),
        count("order_id").alias("order_count")
    )
)

df_gold.write.format("delta").mode("overwrite").saveAsTable("gold_product_summary")
df_gold.show()
```

### 4. Delta Lake Features (Time Travel, MERGE)
```python
# Time travel — query previous versions (like S3 versioning but for tables)
spark.sql("DESCRIBE HISTORY bronze_orders").show(truncate=False)

# Read a previous version
# spark.read.format("delta").option("versionAsOf", 0).table("bronze_orders")

# MERGE (upsert) — no equivalent in plain S3/Parquet
spark.sql("""
    MERGE INTO silver_orders target
    USING (SELECT 3 as order_id, 'Alice' as customer, 'Tablet' as product,
                  449.99 as amount, '2024-01-02' as order_date) source
    ON target.order_id = source.order_id
    WHEN MATCHED THEN UPDATE SET target.amount = source.amount
    WHEN NOT MATCHED THEN INSERT *
""")

spark.table("silver_orders").show()
```

## Cleanup
- Terminate Databricks cluster
- `az group delete --name rg-data-lab03 --yes --no-wait`

## Key Takeaways
- Delta Lake = ACID transactions on data lakes (the standard in Databricks)
- Medallion: Bronze (raw) → Silver (clean) → Gold (aggregated)
- Time travel lets you query/rollback to any previous version
- MERGE (upsert) is a killer feature — impossible with plain Parquet
- This pattern is used in 90% of Azure data engineering projects
