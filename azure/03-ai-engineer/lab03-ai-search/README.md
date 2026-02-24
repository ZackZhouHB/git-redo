# Lab 03 — Azure AI Search

AWS Equivalent: Amazon Kendra / OpenSearch
Cost: ~$15 (Free tier: 1 index, 50MB)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
Kendra                  →  Azure AI Search
OpenSearch              →  Azure AI Search (also supports full-text)
Kendra + Bedrock KB     →  AI Search + Azure OpenAI (RAG pattern)
```

AI Search is the vector/full-text search engine that powers RAG in Azure.

## Hands-On

### 1. Create AI Search
```bash
az group create --name rg-ai-lab03 --location australiaeast

az search service create \
  --resource-group rg-ai-lab03 \
  --name search-lab03-$(date +%s | tail -c 8) \
  --sku free \
  --location australiaeast

export SEARCH_NAME=$(az search service list --resource-group rg-ai-lab03 --query [0].name -o tsv)
export SEARCH_KEY=$(az search admin-key show \
  --resource-group rg-ai-lab03 --service-name $SEARCH_NAME --query primaryKey -o tsv)
export SEARCH_ENDPOINT="https://$SEARCH_NAME.search.windows.net"
```

### 2. Create an Index
```bash
curl -X PUT "$SEARCH_ENDPOINT/indexes/products?api-version=2024-07-01" \
  -H "Content-Type: application/json" \
  -H "api-key: $SEARCH_KEY" \
  -d '{
    "fields": [
      {"name": "id", "type": "Edm.String", "key": true, "filterable": true},
      {"name": "name", "type": "Edm.String", "searchable": true},
      {"name": "description", "type": "Edm.String", "searchable": true},
      {"name": "category", "type": "Edm.String", "filterable": true, "facetable": true},
      {"name": "price", "type": "Edm.Double", "filterable": true, "sortable": true}
    ]
  }'
```

### 3. Upload Documents
```bash
curl -X POST "$SEARCH_ENDPOINT/indexes/products/docs/index?api-version=2024-07-01" \
  -H "Content-Type: application/json" \
  -H "api-key: $SEARCH_KEY" \
  -d '{
    "value": [
      {"@search.action": "upload", "id": "1", "name": "Surface Laptop", "description": "Lightweight laptop for professionals", "category": "Laptops", "price": 999.99},
      {"@search.action": "upload", "id": "2", "name": "Xbox Controller", "description": "Wireless gaming controller", "category": "Gaming", "price": 59.99},
      {"@search.action": "upload", "id": "3", "name": "Azure Dev Board", "description": "IoT development board for cloud projects", "category": "IoT", "price": 149.99}
    ]
  }'
```

### 4. Search
```bash
# Full-text search
curl "$SEARCH_ENDPOINT/indexes/products/docs/search?api-version=2024-07-01" \
  -H "Content-Type: application/json" \
  -H "api-key: $SEARCH_KEY" \
  -d '{"search": "laptop", "top": 5}'

# Filtered search
curl "$SEARCH_ENDPOINT/indexes/products/docs/search?api-version=2024-07-01" \
  -H "Content-Type: application/json" \
  -H "api-key: $SEARCH_KEY" \
  -d '{"search": "*", "filter": "price lt 200", "orderby": "price desc"}'
```

## Cleanup
```bash
az group delete --name rg-ai-lab03 --yes --no-wait
```

## Key Takeaways
- AI Search = full-text + vector search engine
- Free tier: 1 service, 3 indexes, 50MB — enough for learning
- Supports vector search for embeddings (key for RAG)
- AI Search + Azure OpenAI = the standard RAG pattern in Azure
- Indexers can auto-pull from Blob Storage, SQL, Cosmos DB
