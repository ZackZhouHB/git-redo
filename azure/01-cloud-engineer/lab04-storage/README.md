# Lab 04 — Storage Accounts & Blob Storage

AWS Equivalent: S3, EBS, EFS
Cost: ~$2

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
S3 Bucket               →  Storage Account → Container → Blobs
S3 Standard             →  Hot tier
S3 IA                   →  Cool tier
S3 Glacier              →  Archive tier
S3 Lifecycle Rules      →  Lifecycle Management Policies
S3 Versioning           →  Blob Versioning
S3 Static Website       →  Static Website Hosting (in Storage Account)
EBS                     →  Managed Disks
EFS                     →  Azure Files (SMB/NFS shares)
aws s3 cp               →  az storage blob upload / azcopy
```

Key difference: Azure has a "Storage Account" layer above containers.
One Storage Account can hold Blobs, Files, Queues, and Tables.

## Hands-On

### 1. Create a Storage Account
```bash
az group create --name rg-lab04 --location australiaeast

# Storage account name must be globally unique, 3-24 chars, lowercase+numbers only
az storage account create \
  --resource-group rg-lab04 \
  --name stlab04$(date +%s | tail -c 8) \
  --sku Standard_LRS \
  --kind StorageV2 \
  --access-tier Hot

# Save the name for later
export SA_NAME=$(az storage account list --resource-group rg-lab04 --query [0].name -o tsv)
echo "Storage Account: $SA_NAME"
```

### 2. Blob Storage (like S3)
```bash
# Get connection string (like getting S3 credentials)
export CONN=$(az storage account show-connection-string --name $SA_NAME -o tsv)

# Create a container (like S3 bucket)
az storage container create --name mycontainer --connection-string $CONN

# Upload a file
echo "Hello Azure from an AWS engineer!" > /tmp/hello.txt
az storage blob upload \
  --container-name mycontainer \
  --file /tmp/hello.txt \
  --name hello.txt \
  --connection-string $CONN

# List blobs (like: aws s3 ls)
az storage blob list --container-name mycontainer --connection-string $CONN -o table

# Download
az storage blob download \
  --container-name mycontainer \
  --name hello.txt \
  --file /tmp/hello-downloaded.txt \
  --connection-string $CONN
```

### 3. Access Tiers (like S3 storage classes)
```bash
# Change blob tier
az storage blob set-tier \
  --container-name mycontainer \
  --name hello.txt \
  --tier Cool \
  --connection-string $CONN
```

### 4. SAS Token (like S3 pre-signed URL)
```bash
# Generate SAS token (like: aws s3 presign)
az storage blob generate-sas \
  --container-name mycontainer \
  --name hello.txt \
  --permissions r \
  --expiry $(date -u -v+1H '+%Y-%m-%dT%H:%MZ') \
  --connection-string $CONN -o tsv
```

### 5. Azure Files (like EFS)
```bash
# Create a file share (SMB — mountable on VMs)
az storage share create --name myshare --connection-string $CONN --quota 5
```

## Cleanup
```bash
az group delete --name rg-lab04 --yes --no-wait
```

## Key Takeaways
- Storage Account is a parent resource — contains Blobs, Files, Queues, Tables
- Storage Account names are globally unique (like S3 bucket names)
- Blob tiers: Hot (frequent) → Cool (30 days) → Archive (180 days)
- SAS tokens = pre-signed URLs
- Azure Files = managed SMB/NFS file shares (like EFS)
- `azcopy` is the high-performance tool for bulk transfers (like `aws s3 sync`)
