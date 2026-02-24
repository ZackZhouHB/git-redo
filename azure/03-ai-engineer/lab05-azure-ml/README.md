# Lab 05 — Azure Machine Learning & Prompt Flow

AWS Equivalent: SageMaker
Cost: ~$10

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
SageMaker Studio        →  Azure ML Studio
SageMaker Notebooks     →  Azure ML Compute Instances
SageMaker Endpoints     →  Azure ML Managed Endpoints
SageMaker Pipelines     →  Azure ML Pipelines
SageMaker Model Registry→  Azure ML Model Registry
Bedrock Agents          →  Prompt Flow
```

## Hands-On

### 1. Create Azure ML Workspace
```bash
az group create --name rg-ai-lab05 --location australiaeast

az ml workspace create \
  --resource-group rg-ai-lab05 \
  --name mlw-lab05 \
  --location australiaeast

# Open Azure ML Studio
echo "https://ml.azure.com"
```

### 2. Key Azure ML Concepts
```
Workspace        = SageMaker Domain (top-level container)
Compute Instance = SageMaker Notebook Instance (dev machine)
Compute Cluster  = SageMaker Training Job compute
Managed Endpoint = SageMaker Real-time Endpoint
Environment      = Container image + dependencies
Component        = Reusable pipeline step
```

### 3. Create Compute (CLI)
```bash
# Create compute instance (like SageMaker notebook)
az ml compute create \
  --resource-group rg-ai-lab05 \
  --workspace-name mlw-lab05 \
  --name ci-lab05 \
  --type ComputeInstance \
  --size Standard_DS1_v2

# List compute
az ml compute list --resource-group rg-ai-lab05 --workspace-name mlw-lab05 -o table
```

### 4. Prompt Flow (like Bedrock Agents)
Prompt Flow is a visual tool for building LLM workflows.

In Azure ML Studio → Prompt Flow → Create:
```yaml
# flow.dag.yaml — defines the LLM chain
inputs:
  question:
    type: string
nodes:
  - name: classify
    type: llm
    inputs:
      prompt: "Classify this question as: technical, billing, general.\nQuestion: {{question}}"
  - name: answer
    type: llm
    inputs:
      prompt: "You are a {{classify.output}} expert. Answer: {{question}}"
outputs:
  answer:
    value: "{{answer.output}}"
```

### 5. Deploy a Model as Endpoint
```bash
# Register a model
az ml model create \
  --resource-group rg-ai-lab05 \
  --workspace-name mlw-lab05 \
  --name my-model \
  --path ./model/ \
  --type custom_model

# Create managed online endpoint (like SageMaker endpoint)
az ml online-endpoint create \
  --resource-group rg-ai-lab05 \
  --workspace-name mlw-lab05 \
  --name ep-lab05 \
  --auth-mode key
```

## Cleanup
```bash
# Stop compute first!
az ml compute stop --name ci-lab05 \
  --resource-group rg-ai-lab05 --workspace-name mlw-lab05
az group delete --name rg-ai-lab05 --yes --no-wait
```

## Key Takeaways
- Azure ML = SageMaker (full ML lifecycle platform)
- Prompt Flow = visual LLM chain builder (like LangChain but visual)
- Managed Endpoints = SageMaker real-time endpoints
- For most AI Engineer roles, Azure OpenAI + AI Search (RAG) matters more than Azure ML
- Azure ML is for custom model training; OpenAI is for using pre-built models
