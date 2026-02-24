# Lab 04 — RAG Pattern (AI Search + Azure OpenAI)

AWS Equivalent: Bedrock Knowledge Bases + Kendra
Cost: ~$10

## Concepts

```
AWS                          →  Azure
─────────────────────────────────────────
Bedrock Knowledge Bases      →  AI Search + OpenAI (RAG)
Kendra + Bedrock             →  AI Search + OpenAI (RAG)
Bedrock embeddings           →  OpenAI text-embedding-3-small
S3 (document store)          →  Blob Storage / ADLS
```

RAG = Retrieval-Augmented Generation
User question → Search relevant docs → Feed to LLM → Get grounded answer

## Architecture

```
User Query
    ↓
[Embedding Model] → vector
    ↓
[AI Search] → find relevant chunks
    ↓
[GPT-4o-mini] + context → grounded answer
```

## Hands-On (Python)

### 1. Setup
```bash
pip install openai azure-search-documents
```

### 2. Create Vector Index in AI Search
```python
import os, json
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SearchField, SearchFieldDataType,
    VectorSearch, HnswAlgorithmConfiguration, VectorSearchProfile,
)
from azure.core.credentials import AzureKeyCredential

search_endpoint = os.environ["SEARCH_ENDPOINT"]
search_key = os.environ["SEARCH_KEY"]

index_client = SearchIndexClient(search_endpoint, AzureKeyCredential(search_key))

# Define index with vector field
fields = [
    SearchField(name="id", type=SearchFieldDataType.String, key=True),
    SearchField(name="content", type=SearchFieldDataType.String, searchable=True),
    SearchField(name="embedding", type="Collection(Edm.Single)",
                searchable=True, vector_search_dimensions=1536,
                vector_search_profile_name="my-profile"),
]

vector_search = VectorSearch(
    algorithms=[HnswAlgorithmConfiguration(name="my-hnsw")],
    profiles=[VectorSearchProfile(name="my-profile", algorithm_configuration_name="my-hnsw")],
)

index = SearchIndex(name="rag-index", fields=fields, vector_search=vector_search)
index_client.create_or_update_index(index)
print("Index created")
```

### 3. Embed & Upload Documents
```python
from openai import AzureOpenAI
from azure.search.documents import SearchClient

oai = AzureOpenAI(
    api_key=os.environ["OAI_KEY"],
    api_version="2024-06-01",
    azure_endpoint=os.environ["OAI_ENDPOINT"],
)

# Sample knowledge base
docs = [
    {"id": "1", "content": "AKS is Azure Kubernetes Service. It provides managed Kubernetes with a free control plane."},
    {"id": "2", "content": "Azure Functions is a serverless compute service, similar to AWS Lambda. It supports HTTP triggers natively."},
    {"id": "3", "content": "Bicep is Azure's domain-specific language for infrastructure as code. It compiles to ARM templates."},
    {"id": "4", "content": "Azure Monitor collects metrics and logs. Log Analytics uses KQL (Kusto Query Language) for queries."},
]

# Generate embeddings
for doc in docs:
    resp = oai.embeddings.create(model="text-embedding", input=doc["content"])
    doc["embedding"] = resp.data[0].embedding

# Upload to search
search_client = SearchClient(search_endpoint, "rag-index", AzureKeyCredential(search_key))
search_client.upload_documents(docs)
print(f"Uploaded {len(docs)} documents")
```

### 4. RAG Query
```python
def rag_query(question: str) -> str:
    # Step 1: Embed the question
    q_emb = oai.embeddings.create(model="text-embedding", input=question).data[0].embedding

    # Step 2: Search for relevant docs
    from azure.search.documents.models import VectorizedQuery
    results = search_client.search(
        search_text=question,
        vector_queries=[VectorizedQuery(vector=q_emb, k_nearest_neighbors=3, fields="embedding")],
        top=3,
    )
    context = "\n".join([r["content"] for r in results])

    # Step 3: Ask GPT with context
    response = oai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n{context}"},
            {"role": "user", "content": question},
        ],
        max_tokens=300,
    )
    return response.choices[0].message.content

# Test it
print(rag_query("What is AKS and how does it compare to EKS?"))
print(rag_query("How do I do infrastructure as code in Azure?"))
```

## Cleanup
```bash
az group delete --name rg-ai-lab03 --yes --no-wait
az group delete --name rg-ai-lab01 --yes --no-wait
```

## Key Takeaways
- RAG = Search + LLM — the most important AI pattern right now
- AI Search handles vector + full-text hybrid search
- Embeddings convert text to vectors for semantic search
- This is how ChatGPT-like apps are built with enterprise data
- Azure equivalent of Bedrock Knowledge Bases, but more customizable
