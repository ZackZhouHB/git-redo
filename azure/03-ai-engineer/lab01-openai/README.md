# Lab 01 — Azure OpenAI Service

AWS Equivalent: Amazon Bedrock
Cost: ~$10 (pay per token)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
Bedrock                 →  Azure OpenAI Service
Bedrock invoke-model    →  Azure OpenAI chat/completions API
Bedrock model access    →  Azure OpenAI deployment
Titan Embeddings        →  text-embedding-ada-002 / text-embedding-3-small
Claude/Llama on Bedrock →  GPT-4o, GPT-4, GPT-3.5 on Azure OpenAI
```

## Hands-On

### 1. Create Azure OpenAI Resource
```bash
az group create --name rg-ai-lab01 --location australiaeast

# Create OpenAI resource (requires prior approval)
az cognitiveservices account create \
  --resource-group rg-ai-lab01 \
  --name oai-lab01-$(date +%s | tail -c 8) \
  --kind OpenAI \
  --sku S0 \
  --location australiaeast

export OAI_NAME=$(az cognitiveservices account list --resource-group rg-ai-lab01 --query [0].name -o tsv)

# Get endpoint and key
export OAI_ENDPOINT=$(az cognitiveservices account show \
  --resource-group rg-ai-lab01 --name $OAI_NAME --query properties.endpoint -o tsv)
export OAI_KEY=$(az cognitiveservices account keys list \
  --resource-group rg-ai-lab01 --name $OAI_NAME --query key1 -o tsv)
```

### 2. Deploy a Model
```bash
# Deploy GPT-4o-mini (cheapest, good for learning)
az cognitiveservices account deployment create \
  --resource-group rg-ai-lab01 \
  --name $OAI_NAME \
  --deployment-name gpt-4o-mini \
  --model-name gpt-4o-mini \
  --model-version "2024-07-18" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard
```

### 3. Call the API (curl)
```bash
curl "$OAI_ENDPOINT/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-06-01" \
  -H "Content-Type: application/json" \
  -H "api-key: $OAI_KEY" \
  -d '{
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain Azure to an AWS engineer in 3 sentences."}
    ],
    "max_tokens": 200
  }'
```

### 4. Call the API (Python)
```bash
pip install openai
```

```python
from openai import AzureOpenAI
import os

client = AzureOpenAI(
    api_key=os.environ["OAI_KEY"],
    api_version="2024-06-01",
    azure_endpoint=os.environ["OAI_ENDPOINT"],
)

response = client.chat.completions.create(
    model="gpt-4o-mini",  # deployment name, not model name
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Compare Azure AKS vs AWS EKS in a table."},
    ],
    max_tokens=500,
)
print(response.choices[0].message.content)
```

### 5. Deploy Embeddings Model (for RAG later)
```bash
az cognitiveservices account deployment create \
  --resource-group rg-ai-lab01 \
  --name $OAI_NAME \
  --deployment-name text-embedding \
  --model-name text-embedding-3-small \
  --model-version "1" \
  --model-format OpenAI \
  --sku-capacity 10 \
  --sku-name Standard
```

## Cleanup
```bash
az group delete --name rg-ai-lab01 --yes --no-wait
```

## Key Takeaways
- Azure OpenAI = Bedrock but exclusively OpenAI models (GPT-4o, GPT-4, etc.)
- You deploy models to get an endpoint — like Bedrock model access
- Uses the same OpenAI Python SDK, just with `AzureOpenAI` client
- gpt-4o-mini is cheapest for learning
- Requires approval — apply at https://aka.ms/oai/access
