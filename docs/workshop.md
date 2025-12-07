---
published: true
type: workshop
title: Product Hands-on Lab - Agent Framework on Azure
short_title: Agent Framework on Azure
description: Build a complete Helpdesk Ops Assistant with Microsoft Agent Framework on Azure - from single agent to multi-agent orchestration with MCP servers, AI Search, and Redis.
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
banner_url: assets/banner.jpg
audience: developers, architects, AI engineers
sections_title:
  - Introduction
  - Prerequisites
  - Deploy Infrastructure
  - Module 1 - Simple Agent
  - Module 2 - Complexity Analyst
  - Module 3 - Function Tools
  - Module 4 - Knowledge Integration
  - Module 5 - Group Chat Workflow
  - Module 6 - Orchestration
  - Module 7 - Observability
  - Module 8 - Evaluation
  - Module 9 - Redis Integration
  - Conclusion
---

# Helpdesk Ops Assistant - Agent Framework on Azure

> 🌍 **Available in other languages:** [Français](translations/workshop.fr.md) | [Español](translations/workshop.es.md) | [हिंदी](translations/workshop.hi.md)

Welcome to this hands-on lab! You will build a **mini-helpdesk powered by AI agents** that processes internal tickets using:

- 🔍 **Azure AI Search** for enterprise FAQ knowledge
- 🔧 **MCP Servers** for GitHub ticketing and Microsoft Learn documentation
- 🤖 **Multi-agent orchestration** with Microsoft Agent Framework
- 📊 **Observability** with OpenTelemetry and Azure AI Foundry

## 🎯 Scenario: Helpdesk Ops Assistant

You will build a complete helpdesk system with multiple specialized agents:

| Agent | Role | Tools/Integrations |
|-------|------|-------------------|
| **Orchestrator** | Routes requests, chooses workflow (Solo vs Group Chat) | Workflow control |
| **Complexity Analyst** | Analyzes tickets, produces structured output, suggests strategy | Function tools |
| **Learn Agent** | Queries Microsoft Learn documentation | MCP mslearn server |
| **GitHub Agent** | Creates/manages GitHub issues, labels, comments | MCP github server |

## 📚 Workshop Modules

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
| **Python 3.11+** | Python runtime | [Download Python](https://www.python.org/downloads/) |

<div class="tip" data-title="Windows Installation">

> You can install these tools using `winget` in PowerShell:
> ```powershell
> winget install -e --id Microsoft.AzureCLI
> winget install -e --id Hashicorp.Terraform
> winget install -e --id Git.Git
> winget install -e --id Microsoft.VisualStudioCode
> winget install -e --id Python.Python.3.11
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

<details>
<summary>🤖 Maximize Copilot for This Workshop (click to expand)</summary>

**Set up Copilot for Agent Framework development:**

1. **Create workspace instructions** - Add `.github/copilot-instructions.md` with content like:

        This project uses Microsoft Agent Framework for AI agents.
        - Use Azure OpenAI with DefaultAzureCredential
        - Use async/await patterns for all agent operations
        - Use Pydantic for structured output
        - Use @ai_function decorator for tools
        - Follow OpenTelemetry patterns for observability

2. **Use the right Copilot mode for each task**:
   - **Ask**: Questions about Agent Framework concepts
   - **Edit**: Modify existing agent code
   - **Agent**: Build new agents autonomously
   - **Plan**: Design multi-agent architectures

3. **Leverage MCP servers**: Install Azure MCP and GitHub MCP extensions for enhanced capabilities

</details>

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

### 🐍 Python Environment Setup

Create and activate a Python virtual environment:

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install Agent Framework with all extras
pip install agent-framework[azure,redis,viz] --pre
```

<div class="hint" data-title="Virtual Environment Issues?">

> **Common issues and solutions:**
>
> 1. **"python" not recognized**: Use `python3` instead of `python` on Linux/Mac
> 2. **Activation fails on Windows PowerShell**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` first
> 3. **pip install fails**: Try `python -m pip install --upgrade pip` then retry
> 4. **Wrong Python version**: Verify with `python --version` (need 3.11+)
>
> To verify activation worked, your terminal prompt should show `(.venv)` prefix.

</div>

<div class="hint" data-title="☁️ Use Azure MCP to Check Environment Variables">

> **Ask Copilot with Azure MCP to verify your Azure configuration:**
>
> 1. **Verify Azure CLI login**:
>    ```
>    What Azure account am I currently logged into? 
>    Show tenant ID and subscription name.
>    ```
>
> 2. **Check required environment variables**:
>    ```
>    Check if AZURE_OPENAI_ENDPOINT and AZURE_AI_SEARCH_ENDPOINT 
>    are set in my environment and if they point to valid Azure resources
>    ```
>
> 3. **Validate Azure OpenAI access**:
>    ```
>    Can my current Azure identity access the Azure OpenAI resource 
>    at my AZURE_OPENAI_ENDPOINT? What role assignments do I have?
>    ```
>
> This catches configuration issues before you run any code!

</div>

### ☁️ Azure Requirements

- An active Azure subscription with **Owner** or **Contributor** role
- Sufficient quota for the following services:
  - Azure AI Foundry
  - Azure AI Search
  - Azure Managed Redis
  - Azure OpenAI models (GPT-4o recommended)

### ✅ Verification

After installation, verify your setup by running these commands:

```powershell
# Check Azure CLI
az --version

# Check Terraform
terraform --version

# Check Python
python --version

# Check Agent Framework
pip show agent-framework

# Login to Azure (replace with your tenant)
az login --tenant <your-tenant-id-or-domain.com>

# Display your account details
az account show
```

<div class="warning" data-title="Important">

> Make sure you are logged into the correct Azure subscription before proceeding with the infrastructure deployment.

</div>

<div class="hint" data-title="☁️ Use Azure MCP to Verify Your Setup">

> **If you have Azure MCP Server extension installed, ask Copilot to verify your environment:**
>
> 1. **Check your Azure authentication**:
>    ```
>    What Azure tenant and subscription am I currently logged into?
>    ```
>
> 2. **Verify subscription quotas** before deployment:
>    ```
>    Check if I have enough quota for Azure OpenAI GPT-4o deployment 
>    in my current subscription
>    ```
>
> 3. **List available regions**:
>    ```
>    Which Azure regions support Azure AI Foundry and Azure Managed Redis?
>    ```
>
> This helps catch authentication and quota issues BEFORE you start deploying!

</div>

<div class="warning" data-title="🆘 Need Help?">

> **Stuck during setup? Here's how to get help:**
>
> - 📖 Check the [Troubleshooting Guide](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/wiki/Troubleshooting)
> - 🐛 [Report a setup issue](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[SETUP]%20&labels=setup,help-wanted)
> - 💬 [Ask in Discussions](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions/categories/q-a)
>
> When reporting issues, please include:
> - Your OS and Python version
> - The exact error message
> - Which step you were on

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

<div class="hint" data-title="Terraform Deployment Issues?">

> **Common deployment problems:**
>
> 1. **"Provider not found"**: Run `terraform init -upgrade` to refresh providers
> 2. **Quota exceeded**: Check Azure Portal → Subscriptions → Usage + quotas
> 3. **Region not available**: Try changing the `location` variable in `variables.tf`
> 4. **Authentication error**: Ensure `az login` was successful and run `az account show` to verify
> 5. **State lock error**: If deployment was interrupted, run `terraform force-unlock <LOCK_ID>`
>
> **To view detailed logs:**
> ```bash
> export TF_LOG=DEBUG
> terraform apply
> ```

</div>

<div class="info" data-title="Deployment Time">

> The infrastructure deployment may take 15-30 minutes to complete depending on the Azure region and resource availability.

</div>

### Configure Environment Variables

After deployment, set up your environment variables:

```bash
# Export Terraform outputs
export AZURE_OPENAI_ENDPOINT=$(terraform output -raw azure_openai_endpoint)
export AZURE_OPENAI_API_KEY=$(terraform output -raw azure_openai_api_key)
export AZURE_AI_SEARCH_ENDPOINT=$(terraform output -raw azure_ai_search_endpoint)
export AZURE_AI_SEARCH_KEY=$(terraform output -raw azure_ai_search_key)
export REDIS_CONNECTION_STRING=$(terraform output -raw redis_connection_string)
```

<div class="hint" data-title="☁️ Use Azure MCP to Verify Deployed Resources">

> **Ask Copilot with Azure MCP to validate your deployment:**
>
> 1. **Check deployed resources**:
>    ```
>    List all resources in my resource group that were just deployed 
>    for the helpdesk workshop
>    ```
>
> 2. **Verify Azure OpenAI deployment**:
>    ```
>    What OpenAI model deployments exist in my Azure OpenAI resource? 
>    Is gpt-4o deployed and what's its endpoint?
>    ```
>
> 3. **Check AI Search index**:
>    ```
>    List the indexes in my Azure AI Search service. 
>    Is the helpdesk-kb index created?
>    ```
>
> 4. **Validate Redis connectivity**:
>    ```
>    What's the status of my Azure Managed Redis instance? 
>    Is it running and accessible?
>    ```

</div>

<div class="tip" data-title="🐛 Deployment Failed?">

> **If Terraform deployment fails:**
>
> 1. Check the error message carefully
> 2. Common fixes are in the hint above ("Terraform Deployment Issues?")
> 3. Still stuck? [Report the deployment issue](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[DEPLOY]%20Terraform%20failed&labels=infrastructure,bug) with:
>    - Full error message
>    - Your Azure region
>    - Terraform version (`terraform --version`)

</div>

---

## Module 1 — Creating a Simple Agent

In this module, you will discover the Microsoft Agent Framework and create your first agent.

### 🎯 Learning Objectives

- Understand Agent Framework core concepts
- Create a basic agent with Azure AI Foundry
- Run the agent and handle responses

### 📖 Key Concepts

**Agent Framework** is Microsoft's unified framework for building AI agents that supports:

- Multiple LLM providers (Azure OpenAI, OpenAI, Anthropic, etc.)
- Tool calling and function execution
- Multi-agent orchestration
- Observability with OpenTelemetry

<details>
<summary>🤖 Use GitHub Copilot to Help! (click to expand)</summary>

**Copilot can help you understand the Agent Framework:**

1. **Ask Copilot Chat** (`Ctrl+Shift+I`): `@workspace Explain what AzureOpenAIChatClient does and how to configure it`
2. **Inline suggestions**: Start typing `client = Azure` and let Copilot autocomplete
3. **Get documentation**: Select code and ask `/explain` to understand each parameter

**Pro tip**: Create a custom instruction file `.github/copilot-instructions.md`:
```markdown
We use Microsoft Agent Framework with Azure OpenAI.
Always use DefaultAzureCredential for authentication.
Use async/await patterns for all agent operations.
```

</details>

### 💻 Create Your First Agent

Create a new file `src/module1_simple_agent.py`:

```python
"""Module 1: Simple Agent - Basic helpdesk greeting agent."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Create and run a simple helpdesk agent."""
    
    # Create Azure OpenAI client with Azure Identity
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Create the agent with instructions
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="""You are a friendly IT helpdesk assistant.
        
        Your role is to:
        - Greet users warmly
        - Understand their IT issues
        - Provide initial guidance
        - Escalate complex issues appropriately
        
        Always be professional and empathetic.""",
    )
    
    # Run the agent with a simple query
    query = "Hi, my laptop won't connect to the VPN and I have an important meeting in 30 minutes!"
    print(f"User: {query}")
    
    result = await agent.run(query)
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 🚀 Run Your Agent

```bash
python src/module1_simple_agent.py
```

<div class="hint" data-title="Authentication Errors?">

> **Azure Identity Troubleshooting:**
>
> 1. **DefaultAzureCredential failed**: Ensure you're logged in with `az login`
> 2. **Endpoint not found**: Verify `AZURE_OPENAI_ENDPOINT` is set correctly (should start with `https://`)
> 3. **Deployment not found**: Check deployment name matches exactly in Azure AI Foundry
> 4. **403 Forbidden**: Your Azure account may not have access to the OpenAI resource
>
> **Debug credential chain:**
> ```python
> from azure.identity import DefaultAzureCredential
> credential = DefaultAzureCredential(logging_enable=True)
> token = credential.get_token("https://cognitiveservices.azure.com/.default")
> print(f"Token acquired: {token.token[:20]}...")
> ```

</div>

<div class="task" data-title="Exercise">

> Try modifying the agent's instructions to be more specific about VPN troubleshooting steps. What changes in the response?

</div>

### 🔄 Streaming Responses

For better UX, use streaming:

```python
async def main_streaming() -> None:
    """Run agent with streaming response."""
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="You are a friendly IT helpdesk assistant.",
    )
    
    query = "My email is not syncing on my phone"
    print(f"User: {query}")
    print("Agent: ", end="")
    
    async for update in agent.run_stream(query):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # New line at end
```

<div class="info" data-title="Best Practice">

> Use `run_stream()` for real-time user interfaces to provide immediate feedback while the agent generates its response.

</div>

---

## Module 2 — Complexity Analysis Agent

Build an agent that analyzes tickets and produces structured output.

### 🎯 Learning Objectives

- Create structured output using Pydantic models
- Implement data contracts for agent responses
- Build a ticket analysis pipeline

<details>
<summary>🤖 Copilot for Pydantic Models (click to expand)</summary>

**Let Copilot generate your data contracts:**

1. **Use Agent mode** (`Ctrl+Shift+I` → select "Agent"): Ask Copilot to *"Create a Pydantic model for IT ticket analysis with fields for category, severity, effort estimation, and recommended actions"*

2. **Inline completion**: Type `class TicketAnalysis(BaseModel):` and press Enter - Copilot suggests fields!

3. **Add validation**: Ask *"Add field validators to ensure severity is valid"*

**Reusable prompt** - Create `.github/prompts/pydantic-model.prompt.md` with a description like *"Generate Pydantic model for structured output"* and instructions to create a BaseModel with Field descriptions.

</details>

### 📖 Data Contracts

Define structured output for consistent agent responses:

```python
"""Module 2: Complexity Analyst - Structured ticket analysis."""
import asyncio
import os
from typing import Literal
from pydantic import BaseModel, Field
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


class TicketAnalysis(BaseModel):
    """Structured analysis of a helpdesk ticket."""
    
    ticket_id: str = Field(description="Unique ticket identifier")
    category: Literal["network", "hardware", "software", "access", "other"] = Field(
        description="Primary category of the issue"
    )
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Severity level based on business impact"
    )
    estimated_effort: Literal["quick_fix", "standard", "complex", "escalation"] = Field(
        description="Estimated effort to resolve"
    )
    summary: str = Field(description="Brief summary of the issue")
    recommended_actions: list[str] = Field(
        description="List of recommended actions to resolve"
    )
    requires_escalation: bool = Field(
        description="Whether this needs escalation to senior support"
    )
    suggested_documentation: list[str] = Field(
        description="Relevant documentation or Learn articles to cite"
    )


async def main() -> None:
    """Analyze a ticket and produce structured output."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="ComplexityAnalyst",
        instructions="""You are an expert IT ticket analyst.
        
        Analyze incoming tickets and provide:
        1. Categorization (network, hardware, software, access, other)
        2. Severity assessment (low, medium, high, critical)
        3. Effort estimation
        4. Recommended actions
        5. Escalation decision
        6. Relevant documentation references
        
        Be thorough but concise in your analysis.""",
    )
    
    # Sample ticket
    ticket = """
    TICKET-2024-1234
    Subject: Cannot access SharePoint after password reset
    
    Description:
    I reset my password yesterday as prompted by IT security.
    Since then, I cannot access SharePoint or OneDrive.
    I've tried logging out and back in, clearing cache, and using 
    a different browser. Nothing works.
    
    This is urgent as I have a client presentation tomorrow and 
    all my files are on SharePoint.
    
    User: john.doe@company.com
    Department: Sales
    """
    
    print("Analyzing ticket...")
    result = await agent.run(
        f"Analyze this ticket:\n{ticket}",
        response_format=TicketAnalysis,
    )
    
    # Parse structured response
    analysis = TicketAnalysis.model_validate_json(result.text)
    
    print(f"\n📋 Ticket Analysis: {analysis.ticket_id}")
    print(f"📁 Category: {analysis.category}")
    print(f"🚨 Severity: {analysis.severity}")
    print(f"⏱️ Effort: {analysis.estimated_effort}")
    print(f"📝 Summary: {analysis.summary}")
    print(f"🔧 Actions: {', '.join(analysis.recommended_actions)}")
    print(f"⬆️ Escalation Required: {analysis.requires_escalation}")
    print(f"📚 Documentation: {', '.join(analysis.suggested_documentation)}")


if __name__ == "__main__":
    asyncio.run(main())
```

<div class="tip" data-title="Structured Output">

> Using `response_format=TicketAnalysis` ensures the agent returns valid JSON matching your Pydantic model. This is crucial for building reliable pipelines.

</div>

---

## Module 3 — Function Tools

Extend your agent with native function tools for extraction and classification.

### 🎯 Learning Objectives

- Create function tools using `@ai_function` decorator
- Understand tool calling mechanics
- Build a toolkit for ticket processing

<details>
<summary>🤖 Copilot for Function Tools (click to expand)</summary>

**Use Copilot to generate @ai_function tools:**

1. **Describe what you need** in a comment like `# Create a function tool that extracts email addresses from text using regex` - then press Enter and let Copilot generate the full function!

2. **Use Edit mode** (`Ctrl+Shift+I` → "Edit"): Ask *"Add a new @ai_function that looks up user information from a simulated directory based on email address"*

3. **Generate tests**: Select your tool function and ask `/tests Generate unit tests for this function tool`

</details>

### 📖 Creating Tools

```python
"""Module 3: Function Tools - Extending agents with custom tools."""
import asyncio
import os
import re
from typing import Annotated
from pydantic import Field
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient


# Define tools using @ai_function decorator
@ai_function
def extract_ticket_id(
    text: Annotated[str, Field(description="Text containing a ticket ID")]
) -> str:
    """Extract ticket ID from text (format: TICKET-YYYY-NNNN)."""
    pattern = r"TICKET-\d{4}-\d{4}"
    match = re.search(pattern, text)
    if match:
        return f"Found ticket ID: {match.group()}"
    return "No ticket ID found in the provided text."


@ai_function
def extract_user_email(
    text: Annotated[str, Field(description="Text containing an email address")]
) -> str:
    """Extract user email from text."""
    pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    match = re.search(pattern, text)
    if match:
        return f"Found email: {match.group()}"
    return "No email address found in the provided text."


@ai_function
def classify_urgency(
    description: Annotated[str, Field(description="Ticket description to classify")],
    keywords: Annotated[list[str], Field(description="Urgency keywords to look for")]
) -> dict:
    """Classify ticket urgency based on keywords."""
    urgency_keywords = {
        "critical": ["urgent", "critical", "emergency", "immediately", "asap", "down"],
        "high": ["important", "soon", "deadline", "client", "presentation"],
        "medium": ["issue", "problem", "not working", "help"],
        "low": ["question", "wondering", "when", "how to"]
    }
    
    description_lower = description.lower()
    found_level = "low"
    found_keywords = []
    
    for level, kws in urgency_keywords.items():
        for kw in kws:
            if kw in description_lower:
                found_keywords.append(kw)
                if level in ["critical", "high"]:
                    found_level = level
                    break
    
    return {
        "urgency_level": found_level,
        "matched_keywords": found_keywords,
        "analysis": f"Classified as {found_level} based on: {', '.join(found_keywords) or 'no specific keywords'}"
    }


@ai_function
def lookup_user_info(
    email: Annotated[str, Field(description="User email to look up")]
) -> dict:
    """Look up user information from the directory (simulated)."""
    # Simulated user directory
    users = {
        "john.doe@company.com": {
            "name": "John Doe",
            "department": "Sales",
            "manager": "jane.smith@company.com",
            "vip": True,
            "phone": "+1-555-0101"
        },
        "alice.jones@company.com": {
            "name": "Alice Jones", 
            "department": "Engineering",
            "manager": "bob.wilson@company.com",
            "vip": False,
            "phone": "+1-555-0102"
        }
    }
    
    if email.lower() in users:
        return users[email.lower()]
    return {"error": f"User {email} not found in directory"}


async def main() -> None:
    """Run agent with function tools."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Create agent with tools
    agent = client.create_agent(
        name="TicketProcessor",
        instructions="""You are a ticket processing assistant.
        
        When given a ticket:
        1. Extract the ticket ID
        2. Extract the user email
        3. Look up user information
        4. Classify the urgency
        5. Provide a summary with all gathered information
        
        Use the available tools to gather information.""",
        tools=[
            extract_ticket_id,
            extract_user_email,
            classify_urgency,
            lookup_user_info,
        ],
    )
    
    ticket = """
    TICKET-2024-1234
    From: john.doe@company.com
    
    URGENT: Production server is down and clients cannot access 
    the application. This is affecting our biggest client's demo 
    scheduled for today at 3 PM.
    """
    
    print("Processing ticket with tools...")
    result = await agent.run(f"Process this ticket:\n{ticket}")
    print(f"\n{result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

<div class="info" data-title="Tool Calling">

> The `@ai_function` decorator automatically creates the function schema from type hints and docstrings. The agent decides when to call each tool based on the task.

</div>

<div class="hint" data-title="Tools Not Being Called?">

> **Debugging tool execution:**
>
> 1. **Tool never called**: Make your instructions more explicit about WHEN to use each tool
> 2. **Wrong parameters**: Check your type hints - use `Annotated[str, Field(description="...")]` for clarity
> 3. **Tool returns error**: Add try/except in your tool function and return helpful error messages
>
> **Test tools independently:**
> ```python
> # Test your tool before adding to agent
> result = extract_ticket_id("Check TICKET-2024-1234 please")
> print(result)  # Should show: "Found ticket ID: TICKET-2024-1234"
> ```
>
> **Enable verbose logging:**
> ```python
> import logging
> logging.basicConfig(level=logging.DEBUG)
> ```

</div>

---

## Module 4 — Knowledge Integration (Foundry IQ)

Connect your agent to Azure AI Search for enterprise knowledge.

### 🎯 Learning Objectives

- Integrate Azure AI Search as a knowledge source
- Use Foundry IQ for RAG-based responses
- Add citations to agent responses

### 📖 Azure AI Search Integration

```python
"""Module 4: Knowledge Integration - Connect to Azure AI Search."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_ai import AzureAIAgentClient


async def main() -> None:
    """Create agent with Azure AI Search integration."""
    
    # Use Azure AI Agent Service with built-in search
    async with AzureAIAgentClient(
        async_credential=DefaultAzureCredential(),
        project_connection_string=os.getenv("AZURE_AI_PROJECT_CONNECTION"),
    ) as client:
        
        # Create agent with Azure AI Search tool
        agent = await client.create_agent(
            name="LearnAgent",
            instructions="""You are a documentation expert.
            
            Your role is to:
            1. Search the knowledge base for relevant articles
            2. Provide accurate answers with citations
            3. Always cite your sources with [Source: title]
            4. Suggest related documentation for further reading
            
            Be precise and always back your answers with evidence.""",
            tools=[
                {
                    "type": "azure_ai_search",
                    "azure_ai_search": {
                        "index_connection_id": os.getenv("AZURE_AI_SEARCH_CONNECTION_ID"),
                        "index_name": "helpdesk-kb",
                    }
                }
            ],
        )
        
        # Query about VPN issues
        query = "How do I troubleshoot VPN connection issues after a password reset?"
        print(f"User: {query}\n")
        
        result = await agent.run(query)
        print(f"Agent: {result.text}")
        
        # Check for citations
        if hasattr(result, 'citations') and result.citations:
            print("\n📚 Citations:")
            for citation in result.citations:
                print(f"  - {citation.title}: {citation.url}")


if __name__ == "__main__":
    asyncio.run(main())
```

<div class="tip" data-title="Foundry IQ">

> Foundry IQ provides built-in RAG capabilities that automatically handle document chunking, embedding, and retrieval. This simplifies knowledge integration significantly.

</div>

<div class="hint" data-title="☁️ Use Azure MCP to Verify AI Search Setup">

> **Ask Copilot with Azure MCP to validate your knowledge base:**
>
> 1. **Check AI Search index schema**:
>    ```
>    Show me the schema of the 'helpdesk-kb' index in my Azure AI Search. 
>    What fields are searchable?
>    ```
>
> 2. **Verify document count**:
>    ```
>    How many documents are indexed in my helpdesk-kb Azure AI Search index?
>    ```
>
> 3. **Test a search query**:
>    ```
>    Run a test search query for 'VPN troubleshooting' on my 
>    Azure AI Search index and show the top results
>    ```
>
> 4. **Check connection string**:
>    ```
>    What's the connection ID for my Azure AI Search in AI Foundry?
>    ```

</div>

---

## Module 5 — Group Chat Workflow

Implement a workflow where multiple agents collaborate.

### 🎯 Learning Objectives

- Create multi-agent workflows
- Implement Group Chat orchestration
- Configure agent-to-agent communication

<details>
<summary>🤖 Copilot for Multi-Agent Design (click to expand)</summary>

**Use Copilot to architect multi-agent systems:**

1. **Plan with Copilot** (`Ctrl+Shift+I` → "Plan" mode): Ask *"Design a group chat workflow with a LearnAgent that searches documentation, a GitHubAgent that creates issues, and a GroupManager that coordinates them"*

2. **Create a custom agent** - Add `.github/agents/AgentArchitect.agent.md` with description *"Agent Framework Architecture Assistant"* and tools like `codebase` and `fetch`

3. **Fetch latest docs**: In chat, use `#fetch https://github.com/microsoft/agent-framework`

</details>

### 📖 Group Chat with Learn and GitHub Agents

```python
"""Module 5: Group Chat Workflow - Multi-agent collaboration."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.workflows import GroupChatBuilder


async def main() -> None:
    """Create a group chat with Learn and GitHub agents."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Agent 1: Learn Agent with MCP Microsoft Learn tool
    async with MCPStreamableHTTPTool(
        name="mslearn",
        description="Search Microsoft Learn documentation",
        url=os.getenv("MCP_MSLEARN_URL"),
        headers={"Authorization": f"Bearer {os.getenv('MCP_API_KEY')}"},
    ) as learn_tool:
        
        learn_agent = ChatAgent(
            chat_client=client,
            name="LearnAgent",
            instructions="""You are a documentation specialist.
            
            Your role is to:
            - Search Microsoft Learn for relevant documentation
            - Provide accurate citations with links
            - Summarize key points from documentation
            
            Always cite sources in format: [Doc: Title](URL)""",
            tools=learn_tool,
        )
        
        # Agent 2: GitHub Agent with MCP GitHub tool
        async with MCPStreamableHTTPTool(
            name="github",
            description="Manage GitHub issues and repositories",
            url=os.getenv("MCP_GITHUB_URL"),
            headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
        ) as github_tool:
            
            github_agent = ChatAgent(
                chat_client=client,
                name="GitHubAgent",
                instructions="""You are a GitHub issue manager.
                
                Your role is to:
                - Create issues with proper labels
                - Add comments with context from other agents
                - Link to relevant documentation
                
                Format issues clearly with sections for:
                - Problem Description
                - Steps to Reproduce
                - Relevant Documentation
                - Recommended Actions""",
                tools=github_tool,
            )
            
            # Create Group Chat workflow
            workflow = (
                GroupChatBuilder()
                .add_participant(learn_agent)
                .add_participant(github_agent)
                .set_manager(
                    agent=ChatAgent(
                        chat_client=client,
                        name="GroupManager",
                        instructions="""You manage the discussion between agents.
                        
                        Workflow:
                        1. First, ask LearnAgent to find relevant documentation
                        2. Then, ask GitHubAgent to create an issue with the findings
                        3. Summarize the outcome
                        
                        Select the next speaker based on the current task.""",
                    )
                )
                .with_max_rounds(5)
                .build()
            )
            
            # Run the group chat
            task = """
            A user reported: "Azure Functions deployment fails with 'Out of memory' error"
            
            Please:
            1. Find relevant Azure Functions memory documentation
            2. Create a GitHub issue with the findings and recommended solutions
            """
            
            print("Starting Group Chat workflow...\n")
            
            async for event in workflow.run_stream(task):
                if hasattr(event, 'agent_name') and hasattr(event, 'text'):
                    print(f"[{event.agent_name}]: {event.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

<div class="warning" data-title="MCP Configuration">

> Make sure your MCP servers are running and accessible. Configure the URLs and authentication in your environment variables.

</div>

<div class="hint" data-title="MCP Server Connection Issues?">

> **Troubleshooting MCP connections:**
>
> 1. **Connection refused**: Verify the MCP server URL is correct and server is running
> 2. **Authentication failed**: Check your API keys and tokens are valid
> 3. **Timeout errors**: MCP servers may need time to start - add retry logic
>
> **Test MCP connection manually:**
> ```python
> import httpx
> 
> async def test_mcp():
>     async with httpx.AsyncClient() as client:
>         response = await client.get(
>             os.getenv("MCP_MSLEARN_URL") + "/health",
>             headers={"Authorization": f"Bearer {os.getenv('MCP_API_KEY')}"}
>         )
>         print(f"MCP Status: {response.status_code}")
> ```
>
> **For GitHub MCP**, ensure your `GITHUB_TOKEN` has these scopes:
> - `repo` (for creating issues)
> - `read:org` (if using organization repos)

</div>

---

## Module 6 — Advanced Orchestration

Build a sophisticated orchestrator that coordinates all agents.

### 🎯 Learning Objectives

- Implement Handoff orchestration pattern
- Build the main Orchestrator agent
- Create conditional routing logic

<details>
<summary>🤖 Copilot for Orchestration Patterns (click to expand)</summary>

**Use Copilot Agent mode for complex refactoring:**

1. **Switch to Agent mode** and use a premium model (Claude Sonnet 4.5 or GPT-4o): Ask *"Refactor this code to use the HandoffBuilder pattern with an Orchestrator that routes based on complexity, Specialists for quick resolution/ticket creation/escalation, and proper handoff routes"*

2. **Review with Copilot**: Right-click → Copilot → Review to check your orchestration logic

3. **Debug handoffs**: Ask Copilot *"@workspace Why might my handoff workflow skip the ComplexityAnalyst and go directly to QuickResolver?"*

</details>

### 📖 Handoff Orchestration

```python
"""Module 6: Advanced Orchestration - Handoff workflow."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.workflows import HandoffBuilder


async def create_agents(client: AzureOpenAIChatClient) -> dict:
    """Create all specialist agents."""
    
    complexity_analyst = ChatAgent(
        chat_client=client,
        name="ComplexityAnalyst",
        instructions="""Analyze ticket complexity and recommend routing.
        
        Output format:
        - Complexity: simple | medium | complex
        - Recommended Handler: direct_response | create_ticket | escalate
        - Reasoning: brief explanation
        """,
    )
    
    quick_resolver = ChatAgent(
        chat_client=client,
        name="QuickResolver",
        instructions="""Handle simple IT issues directly.
        
        Provide step-by-step solutions for common problems like:
        - Password resets
        - Browser cache clearing
        - Basic network troubleshooting
        """,
    )
    
    ticket_creator = ChatAgent(
        chat_client=client,
        name="TicketCreator",
        instructions="""Create detailed support tickets.
        
        Format:
        - Title: Clear, concise issue title
        - Priority: Low | Medium | High | Critical
        - Category: Network | Hardware | Software | Access
        - Description: Detailed problem description
        - Steps to Reproduce: If applicable
        """,
    )
    
    escalation_agent = ChatAgent(
        chat_client=client,
        name="EscalationAgent",
        instructions="""Handle complex escalations.
        
        For escalated issues:
        1. Document all gathered information
        2. Identify the appropriate specialist team
        3. Create escalation report with full context
        4. Set up follow-up reminders
        """,
    )
    
    return {
        "analyst": complexity_analyst,
        "resolver": quick_resolver,
        "creator": ticket_creator,
        "escalation": escalation_agent,
    }


async def main() -> None:
    """Run the orchestrated helpdesk workflow."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agents = await create_agents(client)
    
    # Create Orchestrator with Handoff pattern
    orchestrator = ChatAgent(
        chat_client=client,
        name="Orchestrator",
        instructions="""You are the main helpdesk orchestrator.
        
        Workflow:
        1. Receive incoming requests
        2. Route to ComplexityAnalyst for initial assessment
        3. Based on analysis:
           - Simple issues → QuickResolver
           - Medium issues → TicketCreator
           - Complex issues → EscalationAgent
        4. Compile final response for user
        
        Always provide status updates during the process.""",
    )
    
    # Build Handoff workflow
    workflow = (
        HandoffBuilder()
        .set_coordinator(orchestrator)
        .add_specialist(agents["analyst"])
        .add_specialist(agents["resolver"])
        .add_specialist(agents["creator"])
        .add_specialist(agents["escalation"])
        # Configure handoff routes
        .add_handoff(orchestrator, [agents["analyst"]])
        .add_handoff(agents["analyst"], [
            agents["resolver"],
            agents["creator"],
            agents["escalation"]
        ])
        # Enable return to coordinator after specialist completes
        .enable_return_to_previous()
        .build()
    )
    
    # Test with different ticket types
    tickets = [
        "I forgot my password and need to reset it",
        "The VPN keeps disconnecting every 5 minutes since the update",
        "Our entire department can't access the CRM and we have client calls in 1 hour",
    ]
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n{'='*60}")
        print(f"Processing Ticket {i}")
        print(f"{'='*60}")
        print(f"User: {ticket}\n")
        
        async for event in workflow.run_stream(ticket):
            if hasattr(event, 'text') and event.text:
                agent_name = getattr(event, 'agent_name', 'System')
                print(f"[{agent_name}]: {event.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

<div class="info" data-title="Handoff Pattern">

> The Handoff pattern allows agents to transfer control to specialists. The coordinator manages the flow while specialists handle specific tasks.

</div>

<div class="hint" data-title="Handoff Not Working as Expected?">

> **Common orchestration issues:**
>
> 1. **Wrong agent selected**: Be more explicit in your Orchestrator's instructions about routing criteria
> 2. **Infinite loop**: Ensure `enable_return_to_previous()` is configured or set `max_rounds`
> 3. **Agent not responding**: Each specialist needs clear instructions about their scope
>
> **Debug the handoff flow:**
> ```python
> async for event in workflow.run_stream(ticket):
>     # Log all events to see the flow
>     print(f"Event type: {type(event).__name__}")
>     if hasattr(event, 'agent_name'):
>         print(f"  From: {event.agent_name}")
>     if hasattr(event, 'handoff_to'):
>         print(f"  Handoff to: {event.handoff_to}")
> ```
>
> **Tip**: Start with 2 agents before scaling to 4+. Debug the simplest flow first!

</div>

---

## Module 7 — Observability

Enable tracing and monitoring with OpenTelemetry and Azure AI Foundry.

### 🎯 Learning Objectives

- Configure OpenTelemetry for agent tracing
- Visualize agent interactions in Azure AI Foundry
- Monitor tool calls and latency

<details>
<summary>🤖 Copilot for Observability Code (click to expand)</summary>

**Use Copilot to add tracing instrumentation:**

1. **Ask for best practices**: *"@workspace How should I configure OpenTelemetry with Azure Monitor for my Agent Framework application?"*

2. **Generate span code**: Select your async function and ask *"Add OpenTelemetry spans to trace this agent operation with attributes for user_id, query text, and response length"*

3. **Use Azure MCP** (if installed): The Azure MCP server can help with Application Insights connection strings, KQL queries, and Azure Monitor best practices

</details>

### 📖 Setting Up Observability

```python
"""Module 7: Observability - Tracing with OpenTelemetry."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework import ChatAgent, ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.observability import setup_observability
from opentelemetry import trace

# Configure Azure Monitor (Application Insights)
configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
)

# Setup Agent Framework observability
setup_observability(
    service_name="helpdesk-agents",
    enable_tracing=True,
    enable_metrics=True,
)

tracer = trace.get_tracer(__name__)


@ai_function
def check_system_status(
    system_name: str,
) -> dict:
    """Check the status of a system."""
    # Simulated status check
    return {
        "system": system_name,
        "status": "operational",
        "last_check": "2024-01-15T10:30:00Z",
    }


async def main() -> None:
    """Run agent with full observability."""
    
    with tracer.start_as_current_span("helpdesk_session") as span:
        span.set_attribute("user.id", "demo_user")
        span.set_attribute("session.type", "support_request")
        
        client = AzureOpenAIChatClient(
            credential=DefaultAzureCredential(),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name="gpt-4o",
        )
        
        agent = client.create_agent(
            name="ObservableAgent",
            instructions="You are a helpful assistant with system monitoring capabilities.",
            tools=[check_system_status],
        )
        
        queries = [
            "Check the status of the email system",
            "What about the VPN gateway?",
            "And the authentication service?",
        ]
        
        thread = agent.get_new_thread()
        
        for query in queries:
            with tracer.start_as_current_span("agent_query") as query_span:
                query_span.set_attribute("query.text", query)
                
                print(f"User: {query}")
                result = await agent.run(query, thread=thread)
                print(f"Agent: {result.text}\n")
                
                query_span.set_attribute("response.length", len(result.text))


if __name__ == "__main__":
    asyncio.run(main())
```

### 📊 Viewing Traces in Azure

After running your agent, view traces in:

1. **Azure AI Foundry** → Your Project → Tracing
2. **Application Insights** → Transaction Search

<div class="tip" data-title="Trace Analysis">

> Look for:
> - Agent run duration
> - Tool call frequency and latency
> - Token usage per interaction
> - Error rates and patterns

</div>

<div class="hint" data-title="Can't Find Your Traces?">

> **Locating traces in Azure Portal:**
>
> 1. **Azure AI Foundry**: Go to your project → **Tracing** tab → Filter by service name
> 2. **Application Insights**: Go to resource → **Transaction search** → Filter by operation name
>
> **Traces not appearing?**
> - Wait 2-3 minutes for ingestion delay
> - Verify `APPLICATIONINSIGHTS_CONNECTION_STRING` is correct
> - Check you called `configure_azure_monitor()` BEFORE creating agents
>
> **Query traces with KQL:**
> ```kusto
> traces
> | where cloud_RoleName == "helpdesk-agents"
> | where timestamp > ago(1h)
> | order by timestamp desc
> | take 50
> ```
>
> **Export traces for local analysis:**
> ```python
> from opentelemetry.sdk.trace.export import ConsoleSpanExporter
> # Add to see traces in console during development
> ```

</div>

<div class="hint" data-title="☁️ Use Azure MCP to Query Logs Directly">

> **Ask Copilot with Azure MCP to analyze your agent traces:**
>
> 1. **Check recent agent activity**:
>    ```
>    Query my Application Insights for traces from 'helpdesk-agents' 
>    service in the last hour. Show any errors.
>    ```
>
> 2. **Analyze performance**:
>    ```
>    What's the average response time for my agent operations 
>    in Application Insights today?
>    ```
>
> 3. **Find errors**:
>    ```
>    Show me any exceptions or failures logged by my helpdesk agents 
>    in the last 24 hours from Application Insights
>    ```
>
> 4. **Check token usage** (if logged):
>    ```
>    Query custom metrics for token usage in my agent application
>    ```
>
> **Pro tip**: Azure MCP can run KQL queries directly - no need to open Azure Portal!

</div>

---

## Module 8 — Evaluation

Implement evaluation for agent quality and performance.

### 🎯 Learning Objectives

- Create local evaluation tests
- Use Azure AI Foundry evaluators
- Set up batch testing workflows

<details>
<summary>🤖 Copilot for Test Generation (click to expand)</summary>

**Use Copilot to generate evaluation test cases:**

1. **Generate test dataset**: In Agent mode, ask Copilot to *"Generate 10 diverse test cases for IT helpdesk ticket analysis. Include edge cases for each severity level and category. Format as Python dict with input, expected_category, expected_severity."*

2. **Improve failing tests**: Paste your evaluation results and ask: *"These test cases are failing. Analyze the pattern and suggest improvements to my agent's instructions to fix them."*

3. **Create evaluation prompt** - Add `.github/prompts/evaluate-agent.prompt.md` with description *"Run agent evaluation"* and tools like `runCommands` and `codebase`.

</details>

### 📖 Local Evaluation

```python
"""Module 8: Evaluation - Testing agent quality."""
import asyncio
import os
import json
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


# Test dataset
TEST_CASES = [
    {
        "input": "I can't log in to my email",
        "expected_category": "access",
        "expected_severity": "medium",
    },
    {
        "input": "URGENT: Production database is down!",
        "expected_category": "software",
        "expected_severity": "critical",
    },
    {
        "input": "How do I set up email forwarding?",
        "expected_category": "software",
        "expected_severity": "low",
    },
]


async def evaluate_agent() -> dict:
    """Run evaluation on the ticket analyst agent."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="TicketAnalyst",
        instructions="""Analyze IT tickets and respond with JSON:
        {
            "category": "network|hardware|software|access|other",
            "severity": "low|medium|high|critical",
            "summary": "brief description"
        }""",
    )
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Running test case {i}/{len(TEST_CASES)}...")
        
        result = await agent.run(f"Analyze: {test_case['input']}")
        
        try:
            response = json.loads(result.text)
            
            category_match = response.get("category") == test_case["expected_category"]
            severity_match = response.get("severity") == test_case["expected_severity"]
            
            results.append({
                "input": test_case["input"],
                "expected_category": test_case["expected_category"],
                "actual_category": response.get("category"),
                "category_correct": category_match,
                "expected_severity": test_case["expected_severity"],
                "actual_severity": response.get("severity"),
                "severity_correct": severity_match,
                "overall_pass": category_match and severity_match,
            })
        except json.JSONDecodeError:
            results.append({
                "input": test_case["input"],
                "error": "Invalid JSON response",
                "overall_pass": False,
            })
    
    # Calculate metrics
    total = len(results)
    passed = sum(1 for r in results if r.get("overall_pass", False))
    category_accuracy = sum(1 for r in results if r.get("category_correct", False)) / total
    severity_accuracy = sum(1 for r in results if r.get("severity_correct", False)) / total
    
    return {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total,
        "category_accuracy": category_accuracy,
        "severity_accuracy": severity_accuracy,
        "details": results,
    }


async def main() -> None:
    """Run evaluation and print results."""
    
    print("🧪 Running Agent Evaluation\n")
    
    metrics = await evaluate_agent()
    
    print("\n📊 Evaluation Results")
    print(f"{'='*40}")
    print(f"Total Tests: {metrics['total_tests']}")
    print(f"Passed: {metrics['passed']}")
    print(f"Failed: {metrics['failed']}")
    print(f"Pass Rate: {metrics['pass_rate']:.1%}")
    print(f"Category Accuracy: {metrics['category_accuracy']:.1%}")
    print(f"Severity Accuracy: {metrics['severity_accuracy']:.1%}")
    
    print("\n📋 Detailed Results:")
    for result in metrics['details']:
        status = "✅" if result.get('overall_pass') else "❌"
        print(f"{status} {result['input'][:50]}...")


if __name__ == "__main__":
    asyncio.run(main())
```

<div class="info" data-title="Azure AI Foundry Evaluation">

> For production evaluation, use Azure AI Foundry's built-in evaluators:
> - Groundedness
> - Relevance
> - Coherence
> - Fluency

</div>

<div class="hint" data-title="Low Evaluation Scores?">

> **Improving agent quality:**
>
> 1. **Low category accuracy**: Add more examples in instructions or use few-shot prompting
> 2. **Inconsistent JSON output**: Use `response_format=YourModel` to enforce structure
> 3. **Wrong severity classification**: Define explicit criteria in instructions
>
> **Debugging failed tests:**
> ```python
> # Print the raw response to see what went wrong
> for result in metrics['details']:
>     if not result.get('overall_pass'):
>         print(f"Failed: {result['input']}")
>         print(f"Expected: {result.get('expected_category')}, Got: {result.get('actual_category')}")
> ```
>
> **Improve with iteration:**
> 1. Analyze failure patterns
> 2. Update agent instructions with edge cases
> 3. Add more test cases for failing categories
> 4. Consider using a more capable model (GPT-4o vs GPT-4o-mini)

</div>

---

## Module 9 — Redis Integration

Add conversation persistence with Azure Managed Redis.

### 🎯 Learning Objectives

- Configure Redis for conversation storage
- Implement thread persistence
- Enable cross-session memory

<details>
<summary>🤖 Copilot for Redis Integration (click to expand)</summary>

**Use Copilot to implement persistence patterns:**

1. **Ask about Redis patterns**: *"@workspace How do I configure RedisChatMessageStore with Agent Framework for conversation persistence?"*

2. **Debug connection issues**: Paste the error and ask *"I'm getting this Redis connection error. What's wrong with my connection string and how do I fix it?"*

3. **Generate Redis utilities**: In Edit mode, ask *"Add helper functions for testing Redis connectivity, listing all conversation threads for a user, and clearing old conversations with TTL-based cleanup"*

**Azure MCP tip**: If you have Azure MCP server configured, ask *"What Redis SKU is deployed in my subscription?"*

</details>

### 📖 Redis Context Provider

```python
"""Module 9: Redis Integration - Persistent conversations."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework_redis import RedisProvider, RedisChatMessageStore


async def main() -> None:
    """Create agent with Redis-backed memory."""
    
    redis_url = os.getenv("REDIS_CONNECTION_STRING")
    user_id = "user_12345"
    thread_id = "helpdesk_session_001"
    
    # Create Redis provider for semantic memory
    redis_provider = RedisProvider(
        redis_url=redis_url,
        index_name="helpdesk_memory",
        prefix="helpdesk",
        application_id="helpdesk_assistant",
        agent_id="support_agent",
        user_id=user_id,
        thread_id=thread_id,
    )
    
    # Create chat message store for conversation history
    def create_message_store():
        return RedisChatMessageStore(
            redis_url=redis_url,
            thread_id=thread_id,
            key_prefix="chat_messages",
            max_messages=100,
        )
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="PersistentAssistant",
        instructions="""You are a helpful IT assistant with memory.
        
        You can remember:
        - User preferences
        - Previous issues and solutions
        - Common problems for this user
        
        Use this context to provide personalized support.""",
        context_providers=redis_provider,
        chat_message_store_factory=create_message_store,
    )
    
    # Simulate a multi-turn conversation
    conversations = [
        "Hi, I'm having VPN issues again",
        "It's the same problem as last week - keeps disconnecting",
        "Yes, I tried the steps you suggested before",
        "What else can I try?",
    ]
    
    thread = agent.get_new_thread()
    
    print("💬 Starting persistent conversation\n")
    
    for message in conversations:
        print(f"User: {message}")
        result = await agent.run(message, thread=thread)
        print(f"Agent: {result.text}\n")
    
    # Save thread for later resume
    serialized = await thread.serialize()
    print(f"📦 Thread saved: {len(serialized)} bytes")
    
    # Simulate resuming later
    print("\n--- Session resumed ---\n")
    
    resumed_thread = await agent.deserialize_thread(serialized)
    result = await agent.run(
        "Can you remind me what we discussed?",
        thread=resumed_thread
    )
    print(f"User: Can you remind me what we discussed?")
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

<div class="tip" data-title="Redis Best Practices">

> - Use separate prefixes for different applications
> - Set appropriate TTL for conversation data
> - Index frequently searched fields for performance

</div>

<div class="hint" data-title="Redis Connection Problems?">

> **Troubleshooting Redis connectivity:**
>
> 1. **Connection refused**: Verify the Redis connection string format:
>    ```
>    rediss://<name>.redis.cache.windows.net:6380?password=<key>
>    ```
> 2. **SSL/TLS error**: Azure Managed Redis requires SSL - use `rediss://` not `redis://`
> 3. **Authentication failed**: Check access keys in Azure Portal → Redis → Access keys
>
> **Test Redis connection:**
> ```python
> import redis
> 
> r = redis.from_url(os.getenv("REDIS_CONNECTION_STRING"))
> r.ping()  # Should return True
> print("Redis connected successfully!")
> ```
>
> **Memory issues?**
> - Monitor memory usage in Azure Portal → Redis → Metrics
> - Set TTL on keys: `r.setex(key, 3600, value)` (1 hour expiry)
> - Use `SCAN` instead of `KEYS` for large datasets

</div>

<div class="hint" data-title="☁️ Use Azure MCP to Monitor Redis">

> **Ask Copilot with Azure MCP to check your Redis instance:**
>
> 1. **Check Redis status and metrics**:
>    ```
>    What's the current status of my Azure Managed Redis instance? 
>    Show memory usage and connection count.
>    ```
>
> 2. **Get connection details**:
>    ```
>    What's the hostname, port, and SSL configuration for my 
>    Azure Managed Redis resource?
>    ```
>
> 3. **Verify access keys**:
>    ```
>    List the access keys for my Azure Managed Redis 
>    (show primary key for connection string)
>    ```
>
> 4. **Check for issues**:
>    ```
>    Are there any alerts or health issues on my Azure Redis instance?
>    ```
>
> **Pro tip**: If Redis seems slow, ask:
> `What's the cache hit ratio and latency metrics for my Redis instance?`

</div>

---

## Conclusion

Congratulations! 🎉 You have built a complete **Helpdesk Ops Assistant** with:

### ✅ What You Learned

| Module | Skill |
|--------|-------|
| 1 | Creating basic agents with Agent Framework |
| 2 | Structured output with Pydantic models |
| 3 | Function tools and tool calling |
| 4 | Knowledge integration with Azure AI Search |
| 5 | Multi-agent Group Chat workflows |
| 6 | Advanced orchestration with Handoff |
| 7 | Observability with OpenTelemetry |
| 8 | Agent evaluation and testing |
| 9 | Persistent memory with Redis |

### 🏗️ Architecture Summary

```
┌─────────────────────────────────────────────────────────────┐
│                     User Request                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATOR                              │
│            (Routes to appropriate workflow)                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          │               │               │
          ▼               ▼               ▼
    ┌──────────┐    ┌──────────┐    ┌──────────────┐
    │  Simple  │    │  Group   │    │  Escalation  │
    │  Flow    │    │  Chat    │    │  Flow        │
    └──────────┘    └──────────┘    └──────────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
        ┌──────────┐            ┌──────────┐
        │  Learn   │            │  GitHub  │
        │  Agent   │            │  Agent   │
        │ (MCP)    │            │ (MCP)    │
        └──────────┘            └──────────┘
```

### 📚 Additional Resources

#### Agent Framework & Learning

- [Microsoft Agent Framework - GitHub](https://github.com/microsoft/agent-framework)
- [AI Agents for Beginners - Microsoft Agent Framework Module](https://microsoft.github.io/ai-agents-for-beginners/14-microsoft-agent-framework/)
- [Agent Framework Workflows Samples](https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/README.md)
- [Orchestrations Overview](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview)

#### Azure AI & Observability

- [Azure AI Foundry](https://learn.microsoft.com/azure/ai-studio/)
- [Tracing Agents with Azure AI SDK](https://learn.microsoft.com/en-us/azure/ai-foundry/how-to/develop/trace-agents-sdk?view=foundry-classic)
- [Model Context Protocol](https://modelcontextprotocol.io/)

#### Workshop Inspiration

- [GitHub Copilot Hands-on Lab (MOAW Example)](https://moaw.dev/workshop/gh:Philess/GHCopilotHoL/main/docs/?step=0)

### 🚀 Next Steps

1. Add more specialized agents for your use case
2. Implement production error handling
3. Set up CI/CD for agent deployment
4. Configure autoscaling for Azure Functions hosting

### 🐛 Found an Issue? Have a Feature Request?

We want to make this workshop better! Your feedback is invaluable.

<div class="task" data-title="Help Us Improve">

> **Report issues or suggest improvements:**
>
> - 🐛 **Bug or Error**: [Open an Issue](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=bug_report.md&title=[BUG]%20)
> - 💡 **Feature Request**: [Request a Feature](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=feature_request.md&title=[FEATURE]%20)
> - 📝 **Documentation**: [Suggest Doc Improvement](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[DOCS]%20)
> - 💬 **Questions**: [Start a Discussion](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions)

</div>

<details>
<summary>🤖 Use GitHub Copilot to Report Issues (click to expand)</summary>

**If you have the GitHub MCP Server configured, you can create issues directly from Copilot:**

1. **Report a bug you encountered**: Ask Copilot *"Create a GitHub issue in the hands-on-lab-agent-framework-on-azure repo for a bug I found in Module 3: [describe the issue]. Include steps to reproduce and error messages."*

2. **Suggest an improvement**: Ask *"Create a feature request issue for adding [your idea] to the Agent Framework workshop"*

3. **Ask about existing issues**: Ask *"Are there any open issues in the workshop repo related to Redis connection problems?"*

</details>

<div class="info" data-title="Feedback">

> We'd love your feedback! Please open an issue or discussion on the workshop repository.
