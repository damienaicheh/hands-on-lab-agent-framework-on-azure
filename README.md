# Agent Framework on Azure - Hands-On Lab

Welcome to this hands-on lab! You will learn how to build agentic applications using the Agent Framework on Azure.

## 📚 Workshop

Access the full workshop documentation: [Workshop Guide](docs/workshop.md)

Or view it online: `https://aka.ms/ws?src=gh:microsoft/hands-on-lab-agent-framework-on-azure/docs/`

## 📋 Prerequisites

### Local Development Tools

| Tool | Description | Installation |
|------|-------------|--------------|
| **Azure CLI** | Azure command-line interface | [Install](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| **Terraform** | Infrastructure as Code | [Install](https://learn.microsoft.com/azure/developer/terraform/quickstart-configure) |
| **Git** | Version control | [Install](https://learn.microsoft.com/devops/develop/git/install-and-set-up-git) |
| **VS Code** | Code editor | [Download](https://code.visualstudio.com/download) |

**Quick install (Windows PowerShell):**

```powershell
winget install -e --id Microsoft.AzureCLI
winget install -e --id Hashicorp.Terraform
winget install -e --id Git.Git
winget install -e --id Microsoft.VisualStudioCode
```

### VS Code Extensions

**Required:**

```powershell
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension HashiCorp.terraform
code --install-extension ms-vscode.azure-account
code --install-extension ms-vscode.vscode-node-azure-pack
```

**Recommended for AI Development:**

```powershell
code --install-extension ms-windows-ai-studio.windows-ai-studio
code --install-extension ms-azuretools.azure-mcp
code --install-extension ms-azuretools.vscode-azure-github-copilot
code --install-extension ms-python.python
code --install-extension ms-toolsai.jupyter
code --install-extension ms-python.vscode-pylance
```

## 🚀 Deploy the infrastructure

First, you need to initialize the Terraform infrastructure by running the following command:

Login to your Azure account if you haven't already:

### Option 1: Local Environment

```bash
az login --tenant <yourtenantid or domain.com>
```

### Option 2: Github Codespace

You might need to specify `--use-device-code` parameter to ease the az cli authentication process:

```bash
az login --use-device-code --tenant <yourtenantid or domain.com>

# Display your account details
az account show
```

Set the ARM_SUBSCRIPTION_ID environment variable to your Azure subscription ID:

```bash
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

Then navigate to the `infra` directory and initialize terraform:

```bash
cd infra && terraform init
```

Then run the following command to deploy the infrastructure:

```bash
# Apply the deployment directly
terraform apply -auto-approve
```
