# Lab 06 — Azure Functions & Logic Apps

AWS Equivalent: Lambda, Step Functions, EventBridge
Cost: ~$3 (consumption plan — pay per execution)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
Lambda                  →  Azure Functions
API Gateway + Lambda    →  Azure Functions (HTTP trigger built-in)
Step Functions          →  Logic Apps / Durable Functions
EventBridge             →  Event Grid
SQS                     →  Storage Queue / Service Bus Queue
SNS                     →  Event Grid / Service Bus Topics
```

Key difference: Azure Functions have built-in HTTP triggers — no API Gateway needed.

## Hands-On

### 1. Create a Function App
```bash
az group create --name rg-lab06 --location australiaeast

# Create storage account (required by Functions for state)
az storage account create \
  --resource-group rg-lab06 \
  --name stfunclab06$(date +%s | tail -c 8) \
  --sku Standard_LRS

export SA_NAME=$(az storage account list --resource-group rg-lab06 --query [0].name -o tsv)

# Create Function App (like creating a Lambda function)
az functionapp create \
  --resource-group rg-lab06 \
  --name func-lab06-$(date +%s | tail -c 8) \
  --storage-account $SA_NAME \
  --consumption-plan-location australiaeast \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --os-type Linux

export FUNC_NAME=$(az functionapp list --resource-group rg-lab06 --query [0].name -o tsv)
```

### 2. Deploy a Function (using Azure Functions Core Tools)
```bash
# Install func CLI (if not installed)
# brew install azure-functions-core-tools@4

# Create local project
mkdir -p /tmp/func-lab06 && cd /tmp/func-lab06
func init --python --model V2

# Create HTTP trigger function
cat > function_app.py << 'EOF'
import azure.functions as func
import json

app = func.FunctionApp()

@app.route(route="hello", methods=["GET"])
def hello(req: func.HttpRequest) -> func.HttpResponse:
    name = req.params.get("name", "Azure")
    return func.HttpResponse(json.dumps({"message": f"Hello {name} from Azure Functions!"}),
                             mimetype="application/json")
EOF

# Deploy
func azure functionapp publish $FUNC_NAME

# Test it
echo "https://$FUNC_NAME.azurewebsites.net/api/hello?name=AWSEngineer"
```

### 3. App Settings (like Lambda Environment Variables)
```bash
# Set env vars
az functionapp config appsettings set \
  --resource-group rg-lab06 \
  --name $FUNC_NAME \
  --settings MY_SETTING=hello

# List settings
az functionapp config appsettings list --resource-group rg-lab06 --name $FUNC_NAME -o table
```

## Cleanup
```bash
az group delete --name rg-lab06 --yes --no-wait
```

## Key Takeaways
- Azure Functions = Lambda but with built-in HTTP endpoint (no API Gateway needed)
- Consumption plan = pay-per-execution (like Lambda pricing)
- Functions need a Storage Account for internal state
- Logic Apps = low-code Step Functions (visual designer in portal)
- Event Grid = EventBridge equivalent for event routing
