# Lab 06 — Event Hubs & Stream Analytics

AWS Equivalent: Kinesis Data Streams + Kinesis Data Analytics
Cost: ~$8

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
Kinesis Data Streams    →  Event Hubs
Kinesis Firehose        →  Event Hubs Capture
Kinesis Data Analytics  →  Stream Analytics
MSK (Kafka)             →  Event Hubs (Kafka-compatible!)
```

Event Hubs is Kafka-compatible — if you know Kafka, you already know Event Hubs.

## Hands-On

### 1. Create Event Hub
```bash
az group create --name rg-data-lab06 --location australiaeast

# Create namespace (like Kinesis stream group)
az eventhubs namespace create \
  --resource-group rg-data-lab06 \
  --name ehns-lab06-$(date +%s | tail -c 8) \
  --sku Basic \
  --location australiaeast

export EHNS=$(az eventhubs namespace list --resource-group rg-data-lab06 --query [0].name -o tsv)

# Create event hub (like Kinesis stream)
az eventhubs eventhub create \
  --resource-group rg-data-lab06 \
  --namespace-name $EHNS \
  --name orders \
  --partition-count 2 \
  --message-retention 1
```

### 2. Send Events (Python)
```bash
pip install azure-eventhub
```

```python
# send_events.py
from azure.eventhub import EventHubProducerClient, EventData
import json, os

conn_str = os.environ["EH_CONN_STR"]  # get from portal or CLI
client = EventHubProducerClient.from_connection_string(conn_str, eventhub_name="orders")

with client:
    batch = client.create_batch()
    for i in range(10):
        event = {"order_id": i, "product": "Laptop", "amount": 999.99}
        batch.add(EventData(json.dumps(event)))
    client.send_batch(batch)
    print("Sent 10 events")
```

### 3. Get Connection String
```bash
# Create auth rule
az eventhubs namespace authorization-rule keys list \
  --resource-group rg-data-lab06 \
  --namespace-name $EHNS \
  --name RootManageSharedAccessKey \
  --query primaryConnectionString -o tsv
```

### 4. Stream Analytics (like Kinesis Data Analytics)
```bash
# Create Stream Analytics job
az stream-analytics job create \
  --resource-group rg-data-lab06 \
  --job-name sa-lab06 \
  --location australiaeast \
  --output-error-policy Stop \
  --events-outoforder-policy Adjust \
  --events-outoforder-max-delay 5 \
  --events-late-arrival-max-delay 16 \
  --compatibility-level "1.2"

# Configure input/output/query in Azure Portal:
# Input: Event Hub → orders
# Output: Blob Storage or ADLS
# Query:
#   SELECT product, SUM(amount) as total, COUNT(*) as cnt
#   INTO [output]
#   FROM [input]
#   GROUP BY product, TumblingWindow(minute, 1)
```

## Cleanup
```bash
az group delete --name rg-data-lab06 --yes --no-wait
```

## Key Takeaways
- Event Hubs = Kinesis (but also Kafka-compatible!)
- Event Hubs Capture = Firehose (auto-dump to ADLS/Blob)
- Stream Analytics = Kinesis Data Analytics (SQL over streams)
- Basic tier is cheapest for learning
- In production, most teams use Databricks Structured Streaming instead of Stream Analytics
