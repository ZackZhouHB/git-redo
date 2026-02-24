# Lab 03 — Virtual Machines & Availability

AWS Equivalent: EC2, Launch Templates, ASG, ALB, Availability Zones
Cost: ~$10 (use B1s — free tier eligible)

## Concepts

```
AWS                     →  Azure
─────────────────────────────────────────
EC2 Instance            →  Virtual Machine (VM)
AMI                     →  VM Image (from Marketplace or custom)
Instance Type           →  VM Size (Standard_B1s, Standard_D2s_v3, etc.)
Key Pair                →  SSH Key (stored in Azure or provided)
User Data               →  Custom Data / cloud-init
Launch Template         →  VM Scale Set (VMSS) model
Auto Scaling Group      →  VM Scale Set (VMSS)
ALB + Target Group      →  Load Balancer + Backend Pool
Placement Group         →  Proximity Placement Group
Availability Zone       →  Availability Zone (same concept)
```

## Hands-On

### 1. Create a VM
```bash
az group create --name rg-lab03 --location australiaeast

# Create a simple Linux VM (like: aws ec2 run-instances)
az vm create \
  --resource-group rg-lab03 \
  --name vm-lab03 \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard

# This auto-creates: NIC, NSG, Public IP, OS Disk, VNet — all in one command
# AWS equivalent would need separate SG, subnet, key pair, etc.
```

### 2. Connect & Manage
```bash
# Get public IP
az vm show --resource-group rg-lab03 --name vm-lab03 -d --query publicIps -o tsv

# SSH in
ssh azureuser@<public-ip>

# Run command remotely (like SSM send-command)
az vm run-command invoke \
  --resource-group rg-lab03 \
  --name vm-lab03 \
  --command-id RunShellScript \
  --scripts "hostname && uname -a"

# List available VM sizes in region
az vm list-sizes --location australiaeast -o table | head -20

# Resize VM (like changing instance type — requires stop in some cases)
az vm resize --resource-group rg-lab03 --name vm-lab03 --size Standard_B2s
```

### 3. VM Scale Set (like ASG + Launch Template)
```bash
az vmss create \
  --resource-group rg-lab03 \
  --name vmss-lab03 \
  --image Ubuntu2204 \
  --vm-sku Standard_B1s \
  --instance-count 2 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --upgrade-policy-mode automatic \
  --load-balancer lb-lab03

# Scale out (like: aws autoscaling set-desired-capacity)
az vmss scale --resource-group rg-lab03 --name vmss-lab03 --new-capacity 3

# List instances
az vmss list-instances --resource-group rg-lab03 --name vmss-lab03 -o table

# Scale in
az vmss scale --resource-group rg-lab03 --name vmss-lab03 --new-capacity 1
```

### 4. Availability Zones
```bash
# Deploy VM to specific AZ (like --placement az1)
az vm create \
  --resource-group rg-lab03 \
  --name vm-lab03-az1 \
  --image Ubuntu2204 \
  --size Standard_B1s \
  --zone 1 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-sku Standard
```

## Cleanup
```bash
az group delete --name rg-lab03 --yes --no-wait
```

## Key Takeaways
- `az vm create` is a mega-command — creates NIC, NSG, VNet, disk, IP all at once
- VM Scale Sets = ASG + Launch Template combined
- Standard_B1s is the cheapest size (burstable, like t3.micro)
- Always use `--no-wait` on delete to avoid waiting
- `az vm run-command` = SSM Run Command equivalent
