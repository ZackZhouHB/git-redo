# Lab 02 — VNet & Networking

AWS Equivalent: VPC, Subnets, Security Groups, NACLs, NAT Gateway, VPC Peering
Cost: ~$5 (NAT Gateway charges)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
VPC                     →  VNet (Virtual Network)
Subnet                  →  Subnet (same concept)
Security Group          →  NSG (Network Security Group) — attached to subnet or NIC
NACL                    →  NSG (Azure merges SG + NACL into one)
Internet Gateway        →  Implicit (VNets have internet access by default)
NAT Gateway             →  NAT Gateway (same concept)
VPC Peering             →  VNet Peering
Route Table             →  Route Table (UDR — User Defined Routes)
Elastic IP              →  Public IP Address
ALB                     →  Application Gateway
NLB                     →  Azure Load Balancer
AWS PrivateLink         →  Azure Private Link / Private Endpoint
```

Key difference: Azure NSG = AWS Security Group + NACL combined.
NSGs can attach to subnets OR individual NICs.

## Hands-On

### 1. Create a VNet with Subnets
```bash
az group create --name rg-lab02 --location australiaeast

# Create VNet (like aws ec2 create-vpc)
az network vnet create \
  --resource-group rg-lab02 \
  --name vnet-lab02 \
  --address-prefix 10.0.0.0/16 \
  --subnet-name subnet-web \
  --subnet-prefix 10.0.1.0/24

# Add another subnet
az network vnet subnet create \
  --resource-group rg-lab02 \
  --vnet-name vnet-lab02 \
  --name subnet-app \
  --address-prefix 10.0.2.0/24

# List subnets
az network vnet subnet list --resource-group rg-lab02 --vnet-name vnet-lab02 -o table
```

### 2. Create an NSG (Security Group + NACL)
```bash
# Create NSG
az network nsg create --resource-group rg-lab02 --name nsg-web

# Allow HTTP inbound (like SG inbound rule)
az network nsg rule create \
  --resource-group rg-lab02 \
  --nsg-name nsg-web \
  --name AllowHTTP \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --destination-port-ranges 80 443

# Allow SSH
az network nsg rule create \
  --resource-group rg-lab02 \
  --nsg-name nsg-web \
  --name AllowSSH \
  --priority 110 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --destination-port-ranges 22

# Associate NSG to subnet
az network vnet subnet update \
  --resource-group rg-lab02 \
  --vnet-name vnet-lab02 \
  --name subnet-web \
  --network-security-group nsg-web

# List rules
az network nsg rule list --resource-group rg-lab02 --nsg-name nsg-web -o table
```

### 3. VNet Peering (like VPC Peering)
```bash
# Create a second VNet
az network vnet create \
  --resource-group rg-lab02 \
  --name vnet-lab02-peer \
  --address-prefix 10.1.0.0/16 \
  --subnet-name subnet-default \
  --subnet-prefix 10.1.1.0/24

# Peer VNet1 → VNet2
az network vnet peering create \
  --resource-group rg-lab02 \
  --name peer-vnet1-to-vnet2 \
  --vnet-name vnet-lab02 \
  --remote-vnet vnet-lab02-peer \
  --allow-vnet-access

# Peer VNet2 → VNet1 (must be bidirectional, same as AWS)
az network vnet peering create \
  --resource-group rg-lab02 \
  --name peer-vnet2-to-vnet1 \
  --vnet-name vnet-lab02-peer \
  --remote-vnet vnet-lab02 \
  --allow-vnet-access
```

### 4. Public IP & DNS
```bash
# Create a public IP (like Elastic IP)
az network public-ip create \
  --resource-group rg-lab02 \
  --name pip-lab02 \
  --sku Standard \
  --allocation-method Static

az network public-ip show --resource-group rg-lab02 --name pip-lab02 --query ipAddress -o tsv
```

## Cleanup
```bash
az group delete --name rg-lab02 --yes --no-wait
```

## Key Takeaways
- VNet = VPC, but no explicit Internet Gateway needed
- NSG = Security Group + NACL combined — simpler model
- NSG rules use priority numbers (lower = higher priority)
- VNet Peering must be created in both directions
- Azure has no "default VPC" — you always create your own
