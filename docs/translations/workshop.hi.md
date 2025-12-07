---
published: true
type: workshop
title: प्रैक्टिकल वर्कशॉप - Azure पर Agent Framework
short_title: Agent Framework on Azure
description: Microsoft Agent Framework के साथ Azure पर एक पूर्ण Helpdesk Assistant बनाएं - सरल agent से लेकर MCP servers, AI Search और Redis के साथ multi-agent orchestration तक।
level: intermediate
navigation_numbering: false
authors:
  - Olivier Mertens
  - Damien Aicheh
contacts:
  - "@olmertens"
  - "@damienaicheh"
duration_minutes: 300
tags: microsoft foundry, agent framework, ai search, managed redis, mcp, group chat, orchestration, observability, evaluation
navigation_levels: 3
banner_url: ../assets/banner.jpg
audience: डेवलपर्स, आर्किटेक्ट्स, AI इंजीनियर्स
sections_title:
  - परिचय
  - पूर्वापेक्षाएं
  - Infrastructure Deploy करें
  - Module 1 - Simple Agent
  - Module 2 - Complexity Analyzer
  - Module 3 - Function Tools
  - Module 4 - Knowledge Integration
  - Module 5 - Group Chat Workflow
  - Module 6 - Orchestration
  - Module 7 - Observability
  - Module 8 - Evaluation
  - Module 9 - Redis Integration
  - निष्कर्ष
---

# Helpdesk Ops Assistant - Azure पर Agent Framework

> 🌍 **अन्य भाषाओं में उपलब्ध:** [English](../workshop.md) | [Français](workshop.fr.md) | [Español](workshop.es.md)

इस प्रैक्टिकल वर्कशॉप में आपका स्वागत है! आप एक **AI-powered mini-helpdesk** बनाएंगे जो internal tickets को process करता है:

- 🔍 **Azure AI Search** - कंपनी FAQ knowledge के लिए
- 🔧 **MCP Servers** - GitHub ticket management और Microsoft Learn documentation के लिए
- 🤖 **Multi-agent Orchestration** - Microsoft Agent Framework के साथ
- 📊 **Observability** - OpenTelemetry और Microsoft Foundry के साथ

## 🎯 परिदृश्य: Helpdesk Ops Assistant

आप कई specialized agents के साथ एक complete helpdesk system बनाएंगे:

| Agent | भूमिका | Tools/Integrations |
|-------|--------|-------------------|
| **Orchestrator** | Queries route करे, workflow चुने (Solo vs Group Chat) | Workflow control |
| **Complexity Analyzer** | Tickets analyze करे, structured output produce करे, strategy suggest करे | Function tools |
| **Learn Agent** | Microsoft Learn documentation query करे | MCP server mslearn |
| **GitHub Agent** | GitHub issues create/manage करे, labels, comments | MCP server github |

## 📚 Workshop Modules

| Module | विषय | अवधि |
|--------|------|------|
| 1 | Simple Agent बनाएं | 20 मिनट |
| 2 | Complexity Analyzer Agent | 25 मिनट |
| 3 | Function Tools | 30 मिनट |
| 4 | Knowledge Integration (Foundry IQ) | 30 मिनट |
| 5 | Group Chat Workflow | 35 मिनट |
| 6 | Advanced Orchestration | 30 मिनट |
| 7 | Observability | 25 मिनट |
| 8 | Evaluation | 30 मिनट |
| 9 | Redis Integration | 25 मिनट |

---

## पूर्वापेक्षाएं

### 🖥️ Local Development Environment

इस workshop शुरू करने से पहले, सुनिश्चित करें कि आपके machine पर निम्नलिखित tools installed हैं:

#### Required Tools

| Tool | विवरण | Installation Link |
|------|--------|-------------------|
| **Azure CLI** | Azure के लिए Command-line interface | [Azure CLI Install करें](https://learn.microsoft.com/hi-in/cli/azure/install-azure-cli) |
| **Terraform** | Infrastructure as Code tool | [Terraform on Azure Install करें](https://learn.microsoft.com/hi-in/azure/developer/terraform/quickstart-configure) |
| **Git** | Version control system | [Git Install करें](https://learn.microsoft.com/hi-in/devops/develop/git/install-and-set-up-git) |
| **Visual Studio Code** | Code editor | [VS Code Download करें](https://code.visualstudio.com/download) |
| **Python 3.11+** | Python Runtime | [Python Download करें](https://www.python.org/downloads/) |

<div class="tip" data-title="Windows Installation">

> आप PowerShell में `winget` से ये tools install कर सकते हैं:
> ```powershell
> winget install -e --id Microsoft.AzureCLI
> winget install -e --id Hashicorp.Terraform
> winget install -e --id Git.Git
> winget install -e --id Microsoft.VisualStudioCode
> winget install -e --id Python.Python.3.11
> ```

</div>

### 🧩 Visual Studio Code Extensions

Visual Studio Code में निम्नलिखित extensions install करें:

#### Required Extensions

| Extension | ID | उद्देश्य |
|-----------|-----|---------|
| **GitHub Copilot** | `GitHub.copilot` | AI-assisted coding |
| **GitHub Copilot Chat** | `GitHub.copilot-chat` | Interactive AI chat |
| **HashiCorp Terraform** | `HashiCorp.terraform` | Terraform syntax & IntelliSense |
| **Azure Account** | `ms-vscode.azure-account` | Azure login integration |
| **Azure Tools** | `ms-vscode.vscode-node-azure-pack` | Azure development tools |

#### Recommended AI Development Extensions

| Extension | ID | उद्देश्य |
|-----------|-----|---------|
| **AI Toolkit** | `ms-windows-ai-studio.windows-ai-studio` | AI model development & testing |
| **Azure MCP Server** | `ms-azuretools.azure-mcp` | Azure Model Context Protocol server |
| **Azure Learn MCP** | `ms-azuretools.vscode-azure-github-copilot` | Azure documentation & best practices |
| **Python** | `ms-python.python` | Python language support |
| **Jupyter** | `ms-toolsai.jupyter` | Jupyter notebook support |
| **Pylance** | `ms-python.vscode-pylance` | Python IntelliSense |

<div class="hint" data-title="🤖 इस Workshop के लिए Copilot को Maximize करें">

> **Agent Framework development के लिए Copilot configure करें:**
>
> 1. **Workspace instructions बनाएं** - `.github/copilot-instructions.md` add करें:
>    ```markdown
>    यह project Microsoft Agent Framework का use करता है AI agents के लिए।
>    - Azure OpenAI के साथ DefaultAzureCredential use करें
>    - सभी agent operations के लिए async/await patterns use करें
>    - Structured output के लिए Pydantic use करें
>    - Tools के लिए @ai_function decorator use करें
>    - Observability के लिए OpenTelemetry patterns follow करें
>    ```
>
> 2. **हर task के लिए सही Copilot mode use करें**:
>    - **Ask**: Agent Framework concepts के बारे में questions
>    - **Edit**: Existing agent code modify करना
>    - **Agent**: नए agents autonomously build करना
>    - **Plan**: Multi-agent architectures design करना
>
> 3. **MCP servers use करें**: Enhanced capabilities के लिए Azure MCP और GitHub MCP extensions install करें

</div>

<div class="task" data-title="Extensions Install करें">

> Command line से extensions install करें:
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

### 🐍 Python Environment Setup

Python virtual environment बनाएं और activate करें:

```bash
# Virtual environment बनाएं
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Agent Framework सभी extras के साथ install करें
pip install agent-framework[azure,redis,viz] --pre
```

<div class="hint" data-title="Virtual Environment में समस्या?">

> **सामान्य समस्याएं और समाधान:**
>
> 1. **"python" recognized नहीं**: Linux/Mac पर `python` के बजाय `python3` use करें
> 2. **Windows PowerShell पर activation fail**: पहले `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` run करें
> 3. **pip install fail**: `python -m pip install --upgrade pip` try करें फिर retry करें
> 4. **Wrong Python version**: `python --version` से verify करें (3.11+ चाहिए)
>
> यह verify करने के लिए कि activation work हुई, आपके terminal prompt में `(.venv)` prefix दिखना चाहिए।

</div>

<div class="hint" data-title="☁️ Environment Variables Verify करने के लिए Azure MCP Use करें">

> **Azure MCP के साथ Copilot से Azure setup verify करवाएं:**
>
> 1. **Azure CLI connection verify करें**:
>    ```
>    मैं currently किस Azure account में logged in हूं?
>    Tenant ID और subscription name दिखाएं।
>    ```
>
> 2. **Required environment variables check करें**:
>    ```
>    Check करें कि AZURE_OPENAI_ENDPOINT और AZURE_AI_SEARCH_ENDPOINT 
>    मेरे environment में set हैं और valid Azure resources को point करते हैं
>    ```
>
> 3. **Azure OpenAI access validate करें**:
>    ```
>    क्या मेरी current Azure identity मेरे AZURE_OPENAI_ENDPOINT पर 
>    Azure OpenAI resource access कर सकती है? मुझे कौन से roles assigned हैं?
>    ```
>
> यह code run करने से पहले configuration issues detect करता है!

</div>

### ☁️ Azure Prerequisites

- **Owner** या **Contributor** role के साथ active Azure subscription
- निम्नलिखित services के लिए पर्याप्त quota:
  - Microsoft Foundry
  - Azure AI Search
  - Azure Managed Redis
  - Azure OpenAI models (GPT-4o recommended)

### ✅ Verification

Installation के बाद, ये commands run करके अपना setup verify करें:

```powershell
# Azure CLI verify करें
az --version

# Terraform verify करें
terraform --version

# Python verify करें
python --version

# Agent Framework verify करें
pip show agent-framework

# Azure में login करें (अपने tenant से replace करें)
az login --tenant <your-tenant-id-or-domain.com>

# Account details दिखाएं
az account show
```

<div class="warning" data-title="महत्वपूर्ण">

> Infrastructure deployment proceed करने से पहले सुनिश्चित करें कि आप सही Azure subscription में logged in हैं।

</div>

<div class="warning" data-title="🆘 मदद चाहिए?">

> **Setup के दौरान stuck? यहां मदद लें:**
>
> - 📖 [Troubleshooting Guide](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/wiki/Troubleshooting) देखें
> - 🐛 [Setup issue report करें](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[SETUP]%20&labels=setup,help-wanted)
> - 💬 [Discussions में question पूछें](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions/categories/q-a)
>
> Issues report करते समय, कृपया include करें:
> - आपका OS और Python version
> - Exact error message
> - आप किस step पर थे

</div>

---

## Infrastructure Deploy करें

पहले, निम्नलिखित commands run करके Terraform infrastructure initialize करें।

### Option 1: Local Environment

अपने Azure account में login करें:

```bash
az login --tenant <your-tenant-id या domain.com>
```

### Option 2: GitHub Codespace

Azure CLI authentication process facilitate करने के लिए `--use-device-code` parameter specify करना पड़ सकता है:

```bash
az login --use-device-code --tenant <your-tenant-id या domain.com>

# Account details दिखाएं
az account show
```

### Environment Variables Set करें

`ARM_SUBSCRIPTION_ID` environment variable को अपने Azure subscription ID से set करें:

```bash
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

### Terraform से Deploy करें

`infra` directory में navigate करें और Terraform initialize करें:

```bash
cd infra && terraform init
```

फिर infrastructure deploy करने के लिए निम्नलिखित command run करें:

```bash
# Deployment directly apply करें
terraform apply -auto-approve
```

<div class="hint" data-title="Terraform Deployment में समस्या?">

> **सामान्य deployment issues:**
>
> 1. **"Provider not found"**: Providers refresh करने के लिए `terraform init -upgrade` run करें
> 2. **Quota exceeded**: Azure Portal → Subscriptions → Usage + quotas check करें
> 3. **Region unavailable**: `variables.tf` में `location` variable change करने की कोशिश करें
> 4. **Authentication error**: Ensure करें कि `az login` successful था और verify करने के लिए `az account show` run करें
> 5. **State lock error**: अगर deployment interrupt हुआ था, `terraform force-unlock <LOCK_ID>` run करें
>
> **Detailed logs देखने के लिए:**
> ```bash
> export TF_LOG=DEBUG
> terraform apply
> ```

</div>

<div class="info" data-title="Deployment Time">

> Azure region और resource availability के आधार पर infrastructure deployment में 15-30 minutes लग सकते हैं।

</div>

---

## Module 1 — Simple Agent बनाएं

इस module में, आप Microsoft Agent Framework discover करेंगे और अपना पहला agent बनाएंगे।

### 🎯 Learning Objectives

- Agent Framework के fundamental concepts समझें
- Microsoft Foundry के साथ basic agent बनाएं
- Agent run करें और responses handle करें

### 📖 Key Concepts

**Agent Framework** Microsoft का unified framework है AI agents बनाने के लिए जो support करता है:

- Multiple LLM providers (Azure OpenAI, OpenAI, Anthropic, etc.)
- Tool calling और function execution
- Multi-agent orchestration
- OpenTelemetry के साथ observability

<div class="hint" data-title="🤖 मदद के लिए GitHub Copilot Use करें!">

> **Copilot Agent Framework समझने में आपकी मदद कर सकता है:**
>
> 1. **Copilot Chat से पूछें** (`Ctrl+Shift+I`): `@workspace बताएं AzureOpenAIChatClient क्या करता है और इसे configure कैसे करें`
> 2. **Inline suggestions**: `client = Azure` type करना शुरू करें और Copilot को complete करने दें
> 3. **Documentation पाएं**: Code select करें और हर parameter समझने के लिए `/explain` पूछें
>
> **Tip**: Custom instructions file बनाएं `.github/copilot-instructions.md`:
> ```markdown
> हम Microsoft Agent Framework Azure OpenAI के साथ use करते हैं।
> Authentication के लिए हमेशा DefaultAzureCredential use करें।
> सभी agent operations के लिए async/await patterns use करें।
> ```

</div>

### 💻 अपना पहला Agent बनाएं

एक नई file बनाएं `src/module1_simple_agent.py`:

```python
"""Module 1: Simple Agent - Basic helpdesk welcome agent."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Simple helpdesk agent बनाएं और run करें।"""
    
    # Azure Identity के साथ Azure OpenAI client बनाएं
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Instructions के साथ agent बनाएं
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="""आप एक friendly IT helpdesk assistant हैं।
        
        आपकी भूमिका है:
        - Users का गर्मजोशी से स्वागत करें
        - उनकी IT problems समझें
        - Initial guidance provide करें
        - Complex issues को appropriately escalate करें
        
        हमेशा professional और empathetic रहें।""",
    )
    
    # Simple query के साथ agent run करें
    query = "नमस्ते, मेरा laptop VPN से connect नहीं हो रहा और मेरी 30 minutes में important meeting है!"
    print(f"User: {query}")
    
    result = await agent.run(query)
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 🚀 अपना Agent Run करें

```bash
python src/module1_simple_agent.py
```

<div class="hint" data-title="Authentication Errors?">

> **Azure Identity troubleshooting:**
>
> 1. **DefaultAzureCredential fails**: Ensure करें कि आप `az login` से logged in हैं
> 2. **Endpoint not found**: Verify करें कि `AZURE_OPENAI_ENDPOINT` correctly set है (`https://` से start होना चाहिए)
> 3. **Deployment not found**: Verify करें कि deployment name Microsoft Foundry में exactly match करता है
> 4. **403 Forbidden**: आपके Azure account को OpenAI resource का access नहीं हो सकता
>
> **Credential chain debug करें:**
> ```python
> from azure.identity import DefaultAzureCredential
> credential = DefaultAzureCredential(logging_enable=True)
> token = credential.get_token("https://cognitiveservices.azure.com/.default")
> print(f"Token acquired: {token.token[:20]}...")
> ```

</div>

<div class="task" data-title="Exercise">

> Agent instructions को modify करने की कोशिश करें VPN troubleshooting steps के बारे में more specific होने के लिए। Response में क्या बदलता है?

</div>

---

## निष्कर्ष

बधाई हो! 🎉 आपने एक complete **Helpdesk Ops Assistant** बनाया:

### ✅ आपने क्या सीखा

| Module | Skill |
|--------|-------|
| 1 | Agent Framework के साथ basic agents बनाना |
| 2 | Pydantic models के साथ structured output |
| 3 | Function tools और tool calling |
| 4 | Azure AI Search के साथ knowledge integration |
| 5 | Multi-agent Group Chat workflows |
| 6 | Handoff के साथ advanced orchestration |
| 7 | OpenTelemetry के साथ observability |
| 8 | Agent evaluation और testing |
| 9 | Redis के साथ persistent memory |

### 📚 Additional Resources

#### Agent Framework & Learning

- [Microsoft Agent Framework - GitHub](https://github.com/microsoft/agent-framework)
- [AI Agents for Beginners - Microsoft Agent Framework Module](https://microsoft.github.io/ai-agents-for-beginners/14-microsoft-agent-framework/)
- [Agent Framework Workflows Samples](https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/README.md)
- [Orchestrations Overview](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview)

#### Azure AI & Observability

- [Microsoft Foundry](https://learn.microsoft.com/azure/ai-studio/)
- [Tracing Agents with Azure AI SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/trace-agents-sdk?view=foundry-classic)
- [Model Context Protocol](https://modelcontextprotocol.io/)

#### Workshop Inspiration

- [GitHub Copilot Hands-on Lab (MOAW Example)](https://moaw.dev/workshop/gh:Philess/GHCopilotHoL/main/docs/?step=0)

### 🐛 कोई Issue मिला? Feature Request?

हम इस workshop को बेहतर बनाना चाहते हैं! आपका feedback valuable है।

<div class="task" data-title="हमें बेहतर बनाने में मदद करें">

> **Issues report करें या improvements suggest करें:**
>
> - 🐛 **Bug या Error**: [Issue Open करें](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=bug_report.md&title=[BUG]%20)
> - 💡 **Feature Request**: [Feature Request करें](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=feature_request.md&title=[FEATURE]%20)
> - 📝 **Documentation**: [Doc Improvement Suggest करें](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[DOCS]%20)
> - 💬 **Questions**: [Discussion Start करें](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions)

</div>

<div class="info" data-title="Feedback">

> हमें आपकी प्रतिक्रिया सुनना अच्छा लगेगा! कृपया workshop repository पर issue या discussion open करें।

</div>
