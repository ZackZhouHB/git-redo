# Lab 08 — Azure Monitor & Log Analytics

AWS Equivalent: CloudWatch (Logs, Metrics, Alarms, Dashboards)
Cost: ~$5

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
CloudWatch Metrics      →  Azure Monitor Metrics
CloudWatch Logs         →  Log Analytics Workspace
CloudWatch Alarms       →  Azure Monitor Alerts
CloudWatch Dashboards   →  Azure Dashboards / Workbooks
X-Ray                   →  Application Insights
CloudTrail              →  Activity Log
```

## Hands-On

### 1. Create Log Analytics Workspace
```bash
az group create --name rg-lab08 --location australiaeast

# Create workspace (like CloudWatch Log Group — but centralized)
az monitor log-analytics workspace create \
  --resource-group rg-lab08 \
  --workspace-name law-lab08

export WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group rg-lab08 --workspace-name law-lab08 --query id -o tsv)
```

### 2. Activity Log (like CloudTrail)
```bash
# View recent activity (like: aws cloudtrail lookup-events)
az monitor activity-log list --max-events 10 -o table
```

### 3. Alerts (like CloudWatch Alarms)
```bash
# Create a VM to monitor
az vm create \
  --resource-group rg-lab08 \
  --name vm-lab08 \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

VM_ID=$(az vm show --resource-group rg-lab08 --name vm-lab08 --query id -o tsv)

# Create metric alert (like CloudWatch Alarm)
az monitor metrics alert create \
  --resource-group rg-lab08 \
  --name "high-cpu" \
  --scopes $VM_ID \
  --condition "avg Percentage CPU > 80" \
  --description "CPU over 80%"

# List alerts
az monitor metrics alert list --resource-group rg-lab08 -o table
```

### 4. Query Logs (KQL — Kusto Query Language)
```bash
# Query logs using KQL (like CloudWatch Insights)
az monitor log-analytics query \
  --workspace $WORKSPACE_ID \
  --analytics-query "AzureActivity | take 10" \
  --timespan P1D -o table
```

## Cleanup
```bash
az group delete --name rg-lab08 --yes --no-wait
```

## Key Takeaways
- Log Analytics Workspace = centralized log store (CloudWatch Logs on steroids)
- KQL (Kusto Query Language) = CloudWatch Insights query language — learn it!
- Application Insights = X-Ray + CloudWatch combined for app monitoring
- Activity Log = CloudTrail (auto-enabled, 90 days retention)
- Azure Monitor is the umbrella — metrics, logs, alerts all under one roof
