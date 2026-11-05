# Azure Storage Guard & Container Scanning Pipeline

A hands-on project demonstrating basic DevSecOps automation: a Python tool to fix public cloud configurations and a GitHub Actions pipeline that breaks builds when vulnerable packages are detected.

---

## Architecture Overview

```text
[ Git Push ] ──► [ GitHub Actions ] ──► [ Build Docker Image ]
                                                │
                                                ▼
                                    [ Trivy Vulnerability Scan ]
                                                │
                                                ▼
                                    [ Custom Bash Check ]
                                      ├── (CVEs Found) ──► ❌ Fail Build & Block
                                      └── (Clean Scan) ──► 🔑 Login via OIDC ──► 🚀 Deploy to Azure
```

### 1. CI/CD Container Security Gate (`.github/workflows/deploy-secure-azure.yml`)
* **The Problem:** Deploying outdated or unpatched base container images introduces immediate security risks into production.
* **How it works:** On every code push, GitHub Actions uses **Trivy** to scan the application container. A **Bash** script uses `jq` to parse the scan results. If any `HIGH` or `CRITICAL` vulnerability is found, the script exits with an error code, stopping the deployment.
* **The Fix:** Swapping the old, bloated image reference (`FROM node:14`) with a minimal, pre-hardened base layer (`FROM node:20-alpine`) completely cuts out old packages and clears the security gate.

### 2. Automated Cloud Compliance Script (`remediate_storage.py`)
* **The Problem:** Public storage buckets remain one of the leading causes of cloud data leaks due to human misconfiguration.
* **How it works:** A lightweight **Python** script uses the official Azure SDK (`azure-mgmt-storage` and `azure-identity`) to pull a live list of storage accounts. If it encounters an account with public blob access enabled, it modifies the configuration to `False` on the fly to enforce encryption and strict access boundaries.

---

## Tech Stack
* **Cloud:** Microsoft Azure (Storage Accounts, Entra ID/IAM)
* **Automation:** Python 3.x, Bash
* **Tooling:** GitHub Actions, Aqua Security Trivy, `jq`
* **Containers:** Docker, Alpine Linux

---

## How to Set Up & Run

### Running the Python Script Locally
Make sure you have logged into your account using the Azure CLI (`az login`).

```bash
# Install the required packages
pip install -r requirements.txt

# Set your Azure Subscription ID
export AZURE_SUBSCRIPTION_ID="your-subscription-uuid"

# Run the remediation tool
python remediate_storage.py
```
