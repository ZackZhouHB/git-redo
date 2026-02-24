# Track 2: Senior Azure Data Engineer (Databricks)

Target Certs: DP-203 (Azure Data Engineer), Databricks Certified Data Engineer
Estimated Cost: ~$70

## Lab Order

| # | Lab | AWS Equivalent | Est. Cost |
|---|-----|---------------|-----------|
| 1 | [ADLS Gen2 (Data Lake)](lab01-adls/) | S3 + Lake Formation | ~$2 |
| 2 | [Azure Data Factory](lab02-data-factory/) | Glue ETL, Step Functions | ~$5 |
| 3 | [Databricks Workspace](lab03-databricks/) | EMR / Glue | ~$25 |
| 4 | [Delta Lake & Medallion](lab04-delta-lake/) | Iceberg/Hudi on S3 | ~$15 |
| 5 | [Synapse Analytics](lab05-synapse/) | Redshift + Athena | ~$10 |
| 6 | [Event Hubs & Stream Analytics](lab06-streaming/) | Kinesis + KDA | ~$8 |
| 7 | [End-to-End Pipeline](lab07-e2e-pipeline/) | Full data platform | ~$5 |

⚠️ ALWAYS terminate Databricks clusters and `az group delete` after each lab!
Databricks clusters burn money fast.
