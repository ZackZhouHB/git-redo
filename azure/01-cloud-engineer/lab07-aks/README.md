# Lab 07 — AKS (Azure Kubernetes Service)

AWS Equivalent: EKS
Cost: ~$20 (control plane free, pay for nodes)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
EKS                     →  AKS (control plane is FREE in Azure!)
EKS Node Group          →  AKS Node Pool
ECR                     →  ACR (Azure Container Registry)
aws eks update-kubeconfig → az aks get-credentials
eksctl                  →  az aks create
Fargate (serverless)    →  AKS Virtual Nodes (ACI-backed)
App Mesh                →  Open Service Mesh / Istio add-on
```

Key difference: AKS control plane is FREE. EKS charges $0.10/hr (~$73/month).

## Hands-On

### 1. Create ACR (Container Registry)
```bash
az group create --name rg-lab07 --location australiaeast

# Create ACR (like ECR)
az acr create \
  --resource-group rg-lab07 \
  --name acrlab07$(date +%s | tail -c 8) \
  --sku Basic

export ACR_NAME=$(az acr list --resource-group rg-lab07 --query [0].name -o tsv)
```

### 2. Create AKS Cluster
```bash
# Create AKS (like: eksctl create cluster)
az aks create \
  --resource-group rg-lab07 \
  --name aks-lab07 \
  --node-count 1 \
  --node-vm-size Standard_B2s \
  --attach-acr $ACR_NAME \
  --generate-ssh-keys \
  --enable-managed-identity

# Get credentials (like: aws eks update-kubeconfig)
az aks get-credentials --resource-group rg-lab07 --name aks-lab07

# Verify
kubectl get nodes
kubectl get namespaces
```

### 3. Deploy an App
```bash
# Deploy nginx
kubectl create deployment nginx --image=nginx --replicas=2
kubectl expose deployment nginx --port=80 --type=LoadBalancer

# Wait for external IP
kubectl get svc nginx --watch
# Ctrl+C when EXTERNAL-IP appears, then curl it
```

### 4. Build & Push to ACR
```bash
# Create a simple app
mkdir -p /tmp/aks-app && cd /tmp/aks-app
cat > Dockerfile << 'EOF'
FROM nginx:alpine
RUN echo '<h1>Hello from AKS!</h1>' > /usr/share/nginx/html/index.html
EOF

# Build in ACR (like CodeBuild + ECR push — no local Docker needed!)
az acr build --registry $ACR_NAME --image myapp:v1 .

# Deploy from ACR
kubectl create deployment myapp --image=$ACR_NAME.azurecr.io/myapp:v1
kubectl expose deployment myapp --port=80 --type=LoadBalancer
```

### 5. Scale & Node Pools
```bash
# Scale deployment
kubectl scale deployment myapp --replicas=3

# Add a node pool (like adding a managed node group)
az aks nodepool add \
  --resource-group rg-lab07 \
  --cluster-name aks-lab07 \
  --name pool2 \
  --node-count 1 \
  --node-vm-size Standard_B2s

# List node pools
az aks nodepool list --resource-group rg-lab07 --cluster-name aks-lab07 -o table

# Scale node pool
az aks nodepool scale \
  --resource-group rg-lab07 \
  --cluster-name aks-lab07 \
  --name pool2 \
  --node-count 0
```

## Cleanup
```bash
az group delete --name rg-lab07 --yes --no-wait
```

## Key Takeaways
- AKS control plane is FREE (EKS charges ~$73/month)
- `az acr build` builds images in the cloud — no local Docker needed
- `az aks get-credentials` = `aws eks update-kubeconfig`
- ACR integrates natively with AKS via `--attach-acr`
- Use Standard_B2s nodes for learning (cheapest that works for k8s)
