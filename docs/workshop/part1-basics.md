---
published: true
type: workshop
title: "Part 1: Getting Started - Agent Framework on Azure"
short_title: "Part 1: Basics"
description: Prerequisites, infrastructure deployment, and your first agents with Microsoft Agent Framework.
level: intermediate
navigation_numbering: false
authors:
  - Olivier Mertens
  - Damien Aicheh
contacts:
  - "@olmertens"
  - "@damienaicheh"
duration_minutes: 75
tags: agent framework, azure openai, pydantic, function tools
navigation_levels: 1
banner_url: assets/banner.jpg
sections_title:
  - Introduction
  - 🏠 Navigation
  - Prerequisites
  - Deploy Infrastructure
  - Module 1 - Simple Agent
  - Module 2 - Structured Output
  - Module 3 - Function Tools
  - Part 1 Complete
---

# Part 1: Getting Started

![Workshop Banner](assets/banner.jpg)

> 🌍 **[← Back to Workshop Index](/workshop/index.md)** | **[Part 2: Knowledge & Collaboration →](/workshop/part2-knowledge.md)**

---

## 🏠 Navigation

<div class="tip" data-title="Workshop Navigation">

> **📚 All Parts:**
> - [🏠 Workshop Home](/workshop/index.md)
> - [Part 1: Getting Started](/workshop/part1-basics.md) *(current)*
> - [Part 2: Knowledge & Collaboration](/workshop/part2-knowledge.md)
> - [Part 3: Production Ready](/workshop/part3-production.md)
> - [Part 4: Advanced & Resources](/workshop/part4-advanced.md)
>
> **🌍 This page in other languages:**
> - [🇫🇷 Français](/workshop/translations/fr/part1-basics.fr.md)
> - [🇪🇸 Español](/workshop/translations/es/part1-basics.es.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part1-basics.hi.md)

</div>

This part covers the foundation: setting up your environment and building your first agents.

| Module | What You'll Build | Duration |
|--------|-------------------|----------|
| Setup | Prerequisites & Infrastructure | 25 min |
| 1 | Simple Agent with streaming | 20 min |
| 2 | Complexity Analyst with Pydantic | 15 min |
| 3 | Function Tools with @ai_function | 15 min |

---

## Prerequisites

### 🖥️ Local Development Environment

| Tool | Description | Installation |
|------|-------------|--------------|
| **Azure CLI** | Azure command-line interface | [Install](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| **Terraform** | Infrastructure as Code | [Install](https://learn.microsoft.com/azure/developer/terraform/quickstart-configure) |
| **Git** | Version control | [Install](https://learn.microsoft.com/devops/develop/git/install-and-set-up-git) |
| **VS Code** | Code editor | [Download](https://code.visualstudio.com/download) |
| **Python 3.11+** | Runtime | [Download](https://www.python.org/downloads/) |

<details>
<summary>💻 Windows Installation (click to expand)</summary>

Run PowerShell as Administrator:

```powershell
winget install -e --id Microsoft.AzureCLI
winget install -e --id Hashicorp.Terraform
winget install -e --id Git.Git
winget install -e --id Microsoft.VisualStudioCode
winget install -e --id Python.Python.3.11
```

</details>

<details>
<summary>🐧 Linux/macOS Installation (click to expand)</summary>

**Ubuntu/Debian:**
```bash
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
sudo apt update && sudo apt install terraform git python3.11 python3.11-venv
sudo snap install code --classic
```

**macOS (Homebrew):**
```bash
brew install azure-cli terraform git python@3.11
brew install --cask visual-studio-code
```

</details>

### 🧩 VS Code Extensions

```powershell
# Required
code --install-extension GitHub.copilot
code --install-extension GitHub.copilot-chat
code --install-extension HashiCorp.terraform
code --install-extension ms-vscode.azure-account
code --install-extension ms-python.python

# Recommended for AI development
code --install-extension ms-windows-ai-studio.windows-ai-studio
code --install-extension ms-azuretools.azure-mcp
```

### 🐍 Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux/Mac)
source .venv/bin/activate

# Install Agent Framework
pip install agent-framework[azure,redis,viz] --pre
```

<div class="hint" data-title="🔧 Troubleshooting">

> - **"python" not found**: Use `python3` on Linux/Mac
> - **Activation fails on Windows**: Run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
> - **Prompt should show**: `(.venv)` prefix when activated

</div>

### ☁️ Azure Requirements

- Azure subscription with **Owner** or **Contributor** role
- Quota for: Microsoft Foundry, AI Search, Managed Redis, OpenAI (GPT-4o)

### ✅ Verification

```powershell
az --version          # Azure CLI installed
terraform --version   # Terraform installed
python --version      # Python 3.11+
az login --tenant <your-tenant>
az account show       # Verify correct subscription
```

---

## Deploy Infrastructure

### Login to Azure

```bash
# Standard login
az login --tenant <your-tenant-id>

# Or with device code (for Codespaces)
az login --use-device-code --tenant <your-tenant-id>
```

### Set Subscription

```bash
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

### Deploy with Terraform

```bash
cd infra
terraform init
terraform apply -auto-approve
```

<div class="info" data-title="⏱️ Deployment Time">

> Infrastructure deployment takes **15-30 minutes**.

</div>

### Configure Environment Variables

After deployment:

```bash
export AZURE_OPENAI_ENDPOINT=$(terraform output -raw azure_openai_endpoint)
export AZURE_OPENAI_API_KEY=$(terraform output -raw azure_openai_api_key)
export AZURE_AI_SEARCH_ENDPOINT=$(terraform output -raw azure_ai_search_endpoint)
export AZURE_AI_SEARCH_KEY=$(terraform output -raw azure_ai_search_key)
export REDIS_CONNECTION_STRING=$(terraform output -raw redis_connection_string)
```

<div class="hint" data-title="🤖 Azure MCP Verification">

> Ask Copilot with Azure MCP:
> - *"List all resources in my resource group"*
> - *"What OpenAI model deployments exist?"*
> - *"Is the helpdesk-kb index created in AI Search?"*

</div>

---

## Module 1 — Simple Agent

### 🎯 Learning Objectives

- Understand AI agents vs simple LLM calls
- Create a basic agent with Microsoft Foundry
- Handle sync and streaming responses

### 📚 Concept: What is an AI Agent?

| Simple LLM Call | AI Agent |
|-----------------|----------|
| One-shot response | Multi-turn with memory |
| No external actions | Can call tools |
| Raw text output | Structured responses |

**Agent Framework components:**

```
┌────────────────────────────────────────┐
│           AGENT FRAMEWORK              │
├────────────────────────────────────────┤
│  🤖 Agent       → Brain + instructions │
│  🔧 Tools       → Functions to call    │
│  💬 ChatClient  → Azure OpenAI conn    │
│  🧵 Thread      → Conversation memory  │
└────────────────────────────────────────┘
```

### 🧠 Pseudo-code

```
1. SETUP: Import asyncio, azure.identity, agent_framework
2. CREATE CLIENT: Connect to Azure OpenAI with DefaultAzureCredential
3. CREATE AGENT: Name + instructions defining personality
4. RUN: Send query, get response
5. OUTPUT: Print agent's response
```

### 🔨 Step-by-Step Exercise

Create `src/module1_simple_agent.py`:

**Step 1: Imports**

<details>
<summary>💡 Hint</summary>

```python
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient
```

</details>

**Step 2: Create Client**

<details>
<summary>💡 Hint</summary>

```python
client = AzureOpenAIChatClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name="gpt-4o",
)
```

</details>

**Step 3: Create Agent**

<details>
<summary>💡 Hint</summary>

```python
agent = client.create_agent(
    name="HelpdeskGreeter",
    instructions="""You are a friendly IT helpdesk assistant.
    - Greet users warmly
    - Understand their IT issues
    - Provide initial guidance
    - Escalate complex issues appropriately""",
)
```

</details>

**Step 4: Run Agent**

<details>
<summary>💡 Hint</summary>

```python
query = "Hi, my laptop won't connect to the VPN!"
result = await agent.run(query)
print(f"Agent: {result.text}")
```

</details>

### ✅ Full Solution

<details>
<summary>📄 Complete Module 1 Code</summary>

```python
"""Module 1: Simple Agent - Basic helpdesk greeting agent."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Create and run a simple helpdesk agent."""
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="""You are a friendly IT helpdesk assistant.
        - Greet users warmly
        - Understand their IT issues  
        - Provide initial guidance
        - Escalate complex issues appropriately""",
    )
    
    query = "Hi, my laptop won't connect to the VPN!"
    print(f"User: {query}")
    result = await agent.run(query)
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

### 🚀 Run It

```bash
python src/module1_simple_agent.py
```

<div class="task" data-title="🎯 Challenge">

> Add streaming with `agent.run_stream()` to print tokens in real-time!

</div>

---

## Module 2 — Structured Output

### 🎯 Learning Objectives

- Use Pydantic for structured AI output
- Create a ticket analysis agent
- Get predictable JSON responses

### 📚 Concept: Why Structured Output?

| Free Text | Structured JSON |
|-----------|-----------------|
| "High priority network issue" | `{"severity": "high", "category": "network"}` |
| Hard to parse | Easy to use in code |
| Inconsistent format | Always matches schema |

### 🧠 Pseudo-code

```
1. DEFINE SCHEMA: Pydantic model with fields (category, severity, summary)
2. CREATE AGENT: With instructions about the schema
3. RUN with response_format: Agent returns matching JSON
4. USE DATA: Access fields like analysis.category, analysis.severity
```

### 🔨 Step-by-Step Exercise

Create `src/module2_complexity_analyst.py`:

**Step 1: Define Pydantic Model**

<details>
<summary>💡 Hint</summary>

```python
from pydantic import BaseModel, Field
from typing import Literal

class TicketAnalysis(BaseModel):
    """Structured analysis of a helpdesk ticket."""
    category: Literal["hardware", "software", "network", "access", "other"]
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(description="Brief summary of the issue")
    suggested_action: str = Field(description="Recommended next step")
```

</details>

**Step 2: Create Agent with response_format**

<details>
<summary>💡 Hint</summary>

```python
agent = client.create_agent(
    name="ComplexityAnalyst",
    instructions="""Analyze IT tickets and provide structured output.
    Categorize issues, assess severity, and suggest actions.""",
)

result = await agent.run(
    ticket_text,
    response_format=TicketAnalysis,  # Key parameter!
)
```

</details>

### ✅ Full Solution

<details>
<summary>📄 Complete Module 2 Code</summary>

```python
"""Module 2: Complexity Analyst - Structured ticket analysis."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient
from pydantic import BaseModel, Field
from typing import Literal


class TicketAnalysis(BaseModel):
    """Structured analysis of a helpdesk ticket."""
    category: Literal["hardware", "software", "network", "access", "other"]
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(description="Brief summary of the issue")
    suggested_action: str = Field(description="Recommended next step")


async def main() -> None:
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="ComplexityAnalyst",
        instructions="""Analyze IT tickets and provide structured output.
        Assess severity based on business impact and urgency.""",
    )
    
    ticket = """
    Subject: VPN not working - URGENT
    From: CEO
    Body: I cannot connect to VPN and I have a board meeting in 20 minutes!
    """
    
    result = await agent.run(ticket, response_format=TicketAnalysis)
    analysis = result.response
    
    print(f"Category: {analysis.category}")
    print(f"Severity: {analysis.severity}")
    print(f"Summary: {analysis.summary}")
    print(f"Action: {analysis.suggested_action}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

<div class="task" data-title="🎯 Challenge">

> Add a `priority_score` field (1-10) and an `estimated_resolution_time` field!

</div>

---

## Module 3 — Function Tools

### 🎯 Learning Objectives

- Create tools with `@ai_function` decorator
- Let agents decide when to call functions
- Build a toolkit for ticket management

### 📚 Concept: What are Function Tools?

Function tools let agents **take actions**, not just answer questions:

```
┌──────────────────────────────────────────────────┐
│              TOOL CALLING FLOW                   │
├──────────────────────────────────────────────────┤
│  👤 User: "Create a ticket for my VPN issue"    │
│      ↓                                           │
│  🤖 Agent thinks: "I should use create_ticket"  │
│      ↓                                           │
│  🔧 Agent calls: create_ticket(title, desc)     │
│      ↓                                           │
│  ✅ Tool returns: "Ticket #123 created"         │
│      ↓                                           │
│  🤖 Agent: "I've created ticket #123 for you"   │
└──────────────────────────────────────────────────┘
```

### 🧠 Pseudo-code

```
1. DEFINE TOOL: @ai_function decorator + type hints
2. REGISTER: Pass tools=[...] when creating agent
3. RUN: Agent automatically decides when to use tools
4. RESULT: Tool output is incorporated in response
```

### 🔨 Step-by-Step Exercise

Create `src/module3_function_tools.py`:

**Step 1: Create a Tool**

<details>
<summary>💡 Hint</summary>

```python
from agent_framework import ai_function

@ai_function
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """Create a new helpdesk ticket.
    
    Args:
        title: Short title for the ticket
        description: Detailed description of the issue
        priority: low, medium, high, or critical
        
    Returns:
        Confirmation message with ticket ID
    """
    ticket_id = f"TKT-{hash(title) % 10000:04d}"
    return f"✅ Created ticket {ticket_id}: {title} (Priority: {priority})"
```

</details>

**Step 2: Create Agent with Tools**

<details>
<summary>💡 Hint</summary>

```python
agent = client.create_agent(
    name="TicketManager",
    instructions="""You are a helpdesk ticket manager.
    Use the create_ticket tool to log new issues.""",
    tools=[create_ticket],  # Register the tool
)
```

</details>

### ✅ Full Solution

<details>
<summary>📄 Complete Module 3 Code</summary>

```python
"""Module 3: Function Tools - Ticket management with tools."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework import ai_function


@ai_function
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """Create a new helpdesk ticket."""
    ticket_id = f"TKT-{hash(title) % 10000:04d}"
    return f"✅ Created ticket {ticket_id}: {title} (Priority: {priority})"


@ai_function
def search_kb(query: str) -> str:
    """Search the knowledge base for solutions."""
    # Simulated KB search
    return f"📚 Found 3 articles matching '{query}'"


@ai_function
def escalate_ticket(ticket_id: str, reason: str) -> str:
    """Escalate a ticket to L2 support."""
    return f"🚨 Escalated {ticket_id} to L2: {reason}"


async def main() -> None:
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="TicketManager",
        instructions="""You are a helpdesk ticket manager.
        - Use create_ticket for new issues
        - Use search_kb to find existing solutions
        - Use escalate_ticket for complex problems""",
        tools=[create_ticket, search_kb, escalate_ticket],
    )
    
    query = "My VPN isn't working and I need a ticket created. It's urgent!"
    print(f"User: {query}")
    result = await agent.run(query)
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

<div class="task" data-title="🎯 Challenge">

> Add a `get_ticket_status(ticket_id: str)` tool that returns mock status!

</div>

---

## ✅ Part 1 Complete!

You've learned:

| Module | Skill |
|--------|-------|
| 1 | Creating agents with instructions |
| 2 | Structured output with Pydantic |
| 3 | Function tools with @ai_function |

<div class="info" data-title="Next Steps">

> **[Continue to Part 2: Knowledge & Collaboration →](/workshop/part2-knowledge.md)**
>
> Learn about Azure AI Search integration and multi-agent Group Chat!

</div>
