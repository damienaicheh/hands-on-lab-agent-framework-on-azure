# Agent Framework on Azure - Hands-On Lab

Welcome to this hands-on lab! Build a complete **Helpdesk Ops Assistant** using the Microsoft Agent Framework on Azure.

## 🎯 What You'll Build

A mini-helpdesk powered by AI agents that processes internal tickets using:

- 🔍 **Azure AI Search** for enterprise FAQ knowledge
- 🔧 **MCP Servers** for GitHub ticketing and Microsoft Learn documentation
- 🤖 **Multi-agent orchestration** with Microsoft Agent Framework
- 📊 **Observability** with OpenTelemetry and Microsoft Foundry

## 📚 Workshop

Access the full workshop documentation: [Workshop Guide](docs/workshop.md)

Or view it online: `https://aka.ms/ws?src=gh:microsoft/hands-on-lab-agent-framework-on-azure/docs/`

## 📋 Workshop Modules

| Module | Topic | Duration |
|--------|-------|----------|
| 1 | Creating a Simple Agent | 20 min |
| 2 | Complexity Analysis Agent | 25 min |
| 3 | Function Tools | 30 min |
| 4 | Knowledge Integration (Foundry IQ) | 30 min |
| 5 | Group Chat Workflow | 35 min |
| 6 | Advanced Orchestration | 30 min |
| 7 | Observability | 25 min |
| 8 | Evaluation | 30 min |
| 9 | Redis Integration | 25 min |

## 📋 Prerequisites

### Local Development Tools

| Tool | Description | Installation |
|------|-------------|--------------|
| **Azure CLI** | Azure command-line interface | [Install](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| **Terraform** | Infrastructure as Code | [Install](https://learn.microsoft.com/azure/developer/terraform/quickstart-configure) |
| **Git** | Version control | [Install](https://learn.microsoft.com/devops/develop/git/install-and-set-up-git) |
| **VS Code** | Code editor | [Download](https://code.visualstudio.com/download) |
| **Python 3.11+** | Python runtime | [Download](https://www.python.org/downloads/) |

**Quick install (Windows PowerShell):**

```powershell
winget install -e --id Microsoft.AzureCLI
winget install -e --id Hashicorp.Terraform
winget install -e --id Git.Git
winget install -e --id Microsoft.VisualStudioCode
winget install -e --id Python.Python.3.11
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

First, you need to initialize the terraform infrastructure by running the following command:

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

## 🐍 Python Environment Setup

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.template .env
# Edit .env with your Azure resource values from Terraform outputs
```

## 📁 Project Structure

```text
├── docs/
│   └── workshop.md          # Full workshop guide (MOAW format)
├── infra/
│   └── *.tf                 # Terraform infrastructure
├── src/
│   ├── module1_simple_agent.py
│   ├── module2_complexity_analyst.py
│   ├── module3_function_tools.py
│   ├── module4_knowledge_integration.py
│   ├── module5_group_chat.py
│   ├── module6_orchestration.py
│   ├── module7_observability.py
│   ├── module8_evaluation.py
│   └── module9_redis.py
├── requirements.txt
├── .env.template
└── README.md
```

## 🤝 Contributing

Contributions are welcome! Please open an issue or pull request.

## 📄 License

This project is licensed under the MIT License.
