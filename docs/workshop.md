---
published: true
type: workshop
title: Product Hands-on Lab - Agent Framework on Azure
short_title: Agent Framework on Azure
description: This workshop will cover how to build agentic applications using the Agent Framework on Azure, leveraging various Azure services to create scalable and efficient solutions.
level: beginner # Required. Can be 'beginner', 'intermediate' or 'advanced'
navigation_numbering: false
authors: # Required. You can add as many authors as needed
  - Olivier Mertens
  - Damien Aicheh
contacts: # Required. Must match the number of authors
  - "@olmertens"
  - "@damienaicheh"
duration_minutes: 300
tags: microsoft foundry, agent framework, ai search, managed redis, csu, codespace, devcontainer
navigation_levels: 3
banner_url: assets/banner.jpg
audience: developers, architects, AI engineers
sections_title:
  - Introduction
  - Prerequisites
  - Deploy Infrastructure
---

# Product Hands-on Lab - Agent Framework on Azure

Welcome to this hands-on lab! In this workshop, you will learn how to build agentic applications using the Agent Framework on Azure.

---

## Prerequisites

### 🖥️ Local Development Environment

Before starting this workshop, ensure you have the following tools installed on your machine:

#### Required Tools

| Tool | Description | Installation Link |
|------|-------------|-------------------|
| **Azure CLI** | Command-line interface for Azure | [Install Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| **Terraform** | Infrastructure as Code tool | [Install Terraform on Azure](https://learn.microsoft.com/azure/developer/terraform/quickstart-configure) |
| **Git** | Version control system | [Install Git](https://learn.microsoft.com/devops/develop/git/install-and-set-up-git) |
| **Visual Studio Code** | Code editor | [Download VS Code](https://code.visualstudio.com/download) |

<div class="tip" data-title="Windows Installation">

> You can install these tools using `winget` in PowerShell:
> ```powershell
> winget install -e --id Microsoft.AzureCLI
> winget install -e --id Hashicorp.Terraform
> winget install -e --id Git.Git
> winget install -e --id Microsoft.VisualStudioCode
> ```

</div>

### 🧩 Visual Studio Code Extensions

Install the following extensions in Visual Studio Code:

#### Required Extensions

| Extension | ID | Purpose |
|-----------|-----|---------|
| **GitHub Copilot** | `GitHub.copilot` | AI-assisted coding |
| **GitHub Copilot Chat** | `GitHub.copilot-chat` | Interactive AI chat |
| **HashiCorp Terraform** | `HashiCorp.terraform` | Terraform syntax & IntelliSense |
| **Azure Account** | `ms-vscode.azure-account` | Azure sign-in integration |
| **Azure Tools** | `ms-vscode.vscode-node-azure-pack` | Azure development tools |

#### Recommended Extensions for AI Development

| Extension | ID | Purpose |
|-----------|-----|---------|
| **AI Toolkit** | `ms-windows-ai-studio.windows-ai-studio` | AI model development & testing |
| **Azure MCP Server** | `ms-azuretools.azure-mcp` | Azure Model Context Protocol server |
| **Azure Learn MCP** | `ms-azuretools.vscode-azure-github-copilot` | Azure documentation & best practices |
| **Python** | `ms-python.python` | Python language support |
| **Jupyter** | `ms-toolsai.jupyter` | Jupyter notebook support |
| **Pylance** | `ms-python.vscode-pylance` | Python IntelliSense |

<div class="task" data-title="Install Extensions">

> Install extensions via command line:
> ```powershell
> # Required Extensions
> code --install-extension GitHub.copilot
> code --install-extension GitHub.copilot-chat
> code --install-extension HashiCorp.terraform
> code --install-extension ms-vscode.azure-account
> code --install-extension ms-vscode.vscode-node-azure-pack
> 
> # Recommended AI Extensions
> code --install-extension ms-windows-ai-studio.windows-ai-studio
> code --install-extension ms-azuretools.azure-mcp
> code --install-extension ms-azuretools.vscode-azure-github-copilot
> code --install-extension ms-python.python
> code --install-extension ms-toolsai.jupyter
> code --install-extension ms-python.vscode-pylance
> ```

</div>

### ☁️ Azure Requirements

- An active Azure subscription with **Owner** or **Contributor** role
- Sufficient quota for the following services:
  - Azure AI Foundry
  - Azure AI Search
  - Azure Managed Redis
  - Azure OpenAI models

### ✅ Verification

After installation, verify your setup by running these commands:

```powershell
# Check Azure CLI
az --version

# Check Terraform
terraform --version

# Check Git
git --version

# Login to Azure (replace with your tenant)
az login --tenant <your-tenant-id-or-domain.com>

# Display your account details
az account show
```

<div class="warning" data-title="Important">

> Make sure you are logged into the correct Azure subscription before proceeding with the infrastructure deployment.

</div>

---

## Deploy the Infrastructure

First, you need to initialize the Terraform infrastructure by running the following commands.

### Option 1: Local Environment

Login to your Azure account:

```bash
az login --tenant <yourtenantid or domain.com>
```

### Option 2: GitHub Codespace

You might need to specify `--use-device-code` parameter to ease the Azure CLI authentication process:

```bash
az login --use-device-code --tenant <yourtenantid or domain.com>

# Display your account details
az account show
```

### Set Environment Variables

Set the `ARM_SUBSCRIPTION_ID` environment variable to your Azure subscription ID:

```bash
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

### Deploy with Terraform

Navigate to the `infra` directory and initialize Terraform:

```bash
cd infra && terraform init
```

Then run the following command to deploy the infrastructure:

```bash
# Apply the deployment directly
terraform apply -auto-approve
```

<div class="info" data-title="Deployment Time">

> The infrastructure deployment may take 15-30 minutes to complete depending on the Azure region and resource availability.

</div>
