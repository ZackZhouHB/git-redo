# Lab 02 — Azure AI Services (Cognitive Services)

AWS Equivalent: Rekognition, Comprehend, Translate, Polly, Textract
Cost: ~$5 (free tier available for most services)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
Rekognition             →  Azure AI Vision (Computer Vision)
Comprehend              →  Azure AI Language (Text Analytics)
Translate               →  Azure AI Translator
Polly                   →  Azure AI Speech (Text-to-Speech)
Transcribe              →  Azure AI Speech (Speech-to-Text)
Textract                →  Azure AI Document Intelligence (Form Recognizer)
```

## Hands-On

### 1. Create AI Services (multi-service resource)
```bash
az group create --name rg-ai-lab02 --location australiaeast

# Multi-service resource (one key for Vision, Language, Speech, etc.)
az cognitiveservices account create \
  --resource-group rg-ai-lab02 \
  --name ai-lab02-$(date +%s | tail -c 8) \
  --kind CognitiveServices \
  --sku S0 \
  --location australiaeast

export AI_NAME=$(az cognitiveservices account list --resource-group rg-ai-lab02 --query [0].name -o tsv)
export AI_ENDPOINT=$(az cognitiveservices account show \
  --resource-group rg-ai-lab02 --name $AI_NAME --query properties.endpoint -o tsv)
export AI_KEY=$(az cognitiveservices account keys list \
  --resource-group rg-ai-lab02 --name $AI_NAME --query key1 -o tsv)
```

### 2. Text Analytics (like Comprehend)
```bash
curl "$AI_ENDPOINT/text/analytics/v3.1/sentiment" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: $AI_KEY" \
  -d '{
    "documents": [
      {"id": "1", "language": "en", "text": "Azure is amazing for cloud computing!"},
      {"id": "2", "language": "en", "text": "The deployment failed and I lost all my data."}
    ]
  }'
```

### 3. Computer Vision (like Rekognition)
```bash
# Analyze an image
curl "$AI_ENDPOINT/vision/v3.2/analyze?visualFeatures=Categories,Description,Tags" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: $AI_KEY" \
  -d '{"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Sydney_Opera_House_Sails.jpg/800px-Sydney_Opera_House_Sails.jpg"}'
```

### 4. Translator (like AWS Translate)
```bash
curl "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0&to=ja&to=fr" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: $AI_KEY" \
  -H "Ocp-Apim-Subscription-Region: australiaeast" \
  -d '[{"text": "Hello, I am learning Azure AI services."}]'
```

### 5. Python SDK
```bash
pip install azure-ai-textanalytics
```

```python
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os

client = TextAnalyticsClient(
    endpoint=os.environ["AI_ENDPOINT"],
    credential=AzureKeyCredential(os.environ["AI_KEY"]),
)

docs = ["Azure is great!", "This is terrible."]
results = client.analyze_sentiment(docs)
for doc in results:
    print(f"{doc.sentiment}: pos={doc.confidence_scores.positive:.2f}, neg={doc.confidence_scores.negative:.2f}")
```

## Cleanup
```bash
az group delete --name rg-ai-lab02 --yes --no-wait
```

## Key Takeaways
- Azure AI Services = umbrella for Vision, Language, Speech, Decision
- Multi-service resource = one key for everything (convenient)
- Free tier: 5000 transactions/month for most services
- Same pattern everywhere: create resource → get key + endpoint → call API
- No ML knowledge needed — these are pre-built AI APIs
