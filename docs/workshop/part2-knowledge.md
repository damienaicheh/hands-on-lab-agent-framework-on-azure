---
published: true
type: workshop
title: "Part 2: Knowledge & Collaboration - Agent Framework on Azure"
short_title: "Part 2: Knowledge"
description: Azure AI Search integration and multi-agent Group Chat workflows with MCP.
level: intermediate
navigation_numbering: false
authors:
  - Olivier Mertens
  - Damien Aicheh
contacts:
  - "@olmertens"
  - "@damienaicheh"
duration_minutes: 65
tags: agent framework, azure ai search, rag, mcp, group chat
navigation_levels: 1
banner_url: ../assets/banner.jpg
sections_title:
  - Introduction
  - 🏠 Navigation
  - Code from Part 1
  - Module 4 - Knowledge Integration
  - Module 5 - Group Chat Workflow
  - Part 2 Complete
---

# Part 2: Knowledge & Collaboration

![Workshop Banner](../assets/banner.jpg)

> 🌍 **[← Part 1: Getting Started](/workshop/part1-basics.md)** | **[Part 3: Production Ready →](/workshop/part3-production.md)**

---

## 🏠 Navigation

<div class="tip" data-title="Workshop Navigation">

> **📚 All Parts:**
> - [🏠 Workshop Home](/workshop/index.md)
> - [Part 1: Getting Started](/workshop/part1-basics.md)
> - [Part 2: Knowledge & Collaboration](/workshop/part2-knowledge.md) *(current)*
> - [Part 3: Production Ready](/workshop/part3-production.md)
> - [Part 4: Advanced & Resources](/workshop/part4-advanced.md)
>
> **🌍 This page in other languages:**
> - [🇫🇷 Français](/workshop/translations/fr/part2-knowledge.fr.md)
> - [🇪🇸 Español](/workshop/translations/es/part2-knowledge.es.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part2-knowledge.hi.md)

</div>

---

## 📦 Code from Part 1

Before starting this part, ensure you have the code from Part 1. Here's a quick summary of what you built:

<details>
<summary>📁 Project Structure (click to expand)</summary>

```
helpdesk-agent/
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
└── src/
    ├── module1_simple_agent.py   # Simple streaming agent
    ├── module2_structured.py     # Pydantic structured output
    └── module3_tools.py          # Function tools with @ai_function
```

</details>

<details>
<summary>🔧 Core Components to Reuse (click to expand)</summary>

```python
# Base client setup (reuse in all modules)
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient

client = AzureOpenAIChatClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name="gpt-4o",
)

# Pydantic model from Module 2
from pydantic import BaseModel, Field
from typing import Literal

class TicketAnalysis(BaseModel):
    category: Literal["network", "hardware", "software", "access"]
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(max_length=200)
    suggested_actions: list[str]

# Function tools from Module 3
from agent_framework import ai_function

@ai_function
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """Create a new helpdesk ticket."""
    ticket_id = f"TKT-{hash(title) % 10000:04d}"
    return f"✅ Created ticket {ticket_id}: {title} (Priority: {priority})"
```

</details>

<div class="info" data-title="Haven't completed Part 1?">

> Complete [Part 1: Getting Started](/workshop/part1-basics.md) first, or copy the code above to catch up.

</div>

| Module | What You'll Build | Duration |
|--------|-------------------|----------|
| 4 | Azure AI Search / RAG integration | 30 min |
| 5 | Multi-agent Group Chat with MCP | 35 min |

---

## Module 4 — Knowledge Integration

### 🎯 Learning Objectives

- Understand RAG (Retrieval-Augmented Generation)
- Integrate Azure AI Search
- Build agents with citations

### 📚 Concept: What is RAG?

**RAG** = Retrieval-Augmented Generation

| Without RAG | With RAG |
|-------------|----------|
| Only training data | Searches your documents |
| Can't answer company questions | Uses your knowledge base |
| May hallucinate | Provides citations |
| Outdated knowledge | Always current |

**RAG Pipeline:**

```
┌────────────────────────────────────────────────┐
│               RAG PIPELINE                     │
├────────────────────────────────────────────────┤
│  1️⃣  User: "How to reset VPN?"               │
│      ↓                                         │
│  2️⃣  Azure AI Search finds documents         │
│      ↓                                         │
│  3️⃣  Documents passed to LLM as context      │
│      ↓                                         │
│  4️⃣  Agent generates grounded answer         │
│      ↓                                         │
│  5️⃣  Response includes citations             │
└────────────────────────────────────────────────┘
```

<div class="info" data-title="Why Azure AI Search?">

> - **Hybrid search**: Keyword + semantic
> - **Vector embeddings**: Conceptual similarity
> - **Filtering**: By category, date, etc.
> - **Scale**: Millions of documents

</div>

### 🧠 Pseudo-code

```
1. SETUP: Use AzureAIAgentClient (not AzureOpenAIChatClient)
2. CONFIGURE SEARCH TOOL: type="azure_ai_search", index_name, connection_id
3. CREATE AGENT: Instructions for searching and citing
4. RUN: Agent auto-searches and cites sources
```

### 🔨 Step-by-Step Exercise

Create `src/module4_knowledge_agent.py`:

**Step 1: Import AI Agent Client**

<details>
<summary>💡 Hint</summary>

```python
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_ai import AzureAIAgentClient
```

</details>

**Step 2: Create Client Connection**

<details>
<summary>💡 Hint</summary>

```python
async with AzureAIAgentClient(
    async_credential=DefaultAzureCredential(),
    project_connection_string=os.getenv("AZURE_AI_PROJECT_CONNECTION"),
) as client:
    # Agent creation here
```

</details>

**Step 3: Configure AI Search Tool**

<details>
<summary>💡 Hint</summary>

```python
tools=[
    {
        "type": "azure_ai_search",
        "azure_ai_search": {
            "index_connection_id": os.getenv("AZURE_AI_SEARCH_CONNECTION_ID"),
            "index_name": "helpdesk-kb",
        }
    }
]
```

</details>

**Step 4: Write Instructions for Citations**

<details>
<summary>💡 Hint</summary>

```python
instructions="""You are a documentation expert.

1. Search the knowledge base for relevant articles
2. Provide accurate answers with citations
3. Always cite sources with [Source: title]
4. Say clearly if information is not found

Never make up information."""
```

</details>

### ✅ Full Solution

<details>
<summary>📄 Complete Module 4 Code</summary>

```python
"""Module 4: Knowledge Integration - Azure AI Search."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_ai import AzureAIAgentClient


async def main() -> None:
    """Create agent with Azure AI Search integration."""
    
    async with AzureAIAgentClient(
        async_credential=DefaultAzureCredential(),
        project_connection_string=os.getenv("AZURE_AI_PROJECT_CONNECTION"),
    ) as client:
        
        agent = await client.create_agent(
            name="LearnAgent",
            instructions="""You are a documentation expert.
            
            1. Search the knowledge base for relevant articles
            2. Provide accurate answers with citations
            3. Always cite sources with [Source: title]
            4. Say clearly if information is not found
            
            Never make up information.""",
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
        
        query = "How do I troubleshoot VPN connection issues?"
        print(f"User: {query}\n")
        
        result = await agent.run(query)
        print(f"Agent: {result.text}")
        
        if hasattr(result, 'citations') and result.citations:
            print("\n📚 Citations:")
            for citation in result.citations:
                print(f"  - {citation.title}: {citation.url}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

<div class="hint" data-title="🤖 Verify with Azure MCP">

> Ask Copilot:
> - *"Show the schema of 'helpdesk-kb' index"*
> - *"How many documents in my AI Search?"*
> - *"Test search for 'VPN troubleshooting'"*

</div>

<div class="task" data-title="🎯 Challenge">

> Add a second index "product-docs" and search both!

</div>

---

## Module 5 — Group Chat Workflow

### 🎯 Learning Objectives

- Understand multi-agent collaboration
- Create Group Chat orchestration
- Connect agents via MCP

### 📚 Understanding Orchestration Patterns

The Microsoft Agent Framework provides **pre-built orchestration patterns** that allow you to quickly create complex multi-agent workflows. Understanding which pattern to choose is crucial for building effective agent systems.

<div class="info" data-title="📖 Official Documentation">

> For complete details on orchestration patterns, see the official documentation:
> **[Microsoft Agent Framework Workflows Orchestrations](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/orchestrations/overview){target="_blank"}**

</div>

#### Why Multi-Agent?

Traditional single-agent systems are limited in their ability to handle complex, multi-faceted tasks. By orchestrating multiple agents, each with specialized skills or roles, we can create systems that are more robust, adaptive, and capable of solving real-world problems collaboratively.

#### Supported Orchestrations

| Pattern | Description | Best Use Cases |
|---------|-------------|----------------|
| **Concurrent** | Broadcasts a task to all agents, collects results independently | Parallel analysis, independent subtasks, ensemble decision making |
| **Sequential** | Passes the result from one agent to the next in a defined order | Step-by-step workflows, pipelines, multi-stage processing |
| **Group Chat** ✅ | Coordinates multiple agents in a collaborative conversation with a manager controlling speaker selection and flow | Iterative refinement, collaborative problem-solving, content review |
| **Handoff** | Dynamically passes control between agents based on context or rules | Dynamic workflows, escalation, fallback, or expert handoff scenarios |
| **Magentic** | Inspired by MagenticOne | Complex, generalist multi-agent collaboration |

#### Why Group Chat for This Module?

We chose **Group Chat** orchestration because:

1. **Collaborative Problem-Solving**: Our helpdesk scenario requires multiple specialists (documentation expert, GitHub expert) to work together
2. **Manager-Controlled Flow**: The GroupManager coordinates which agent speaks and when, ensuring organized responses
3. **Iterative Refinement**: Agents can build on each other's contributions to provide comprehensive answers
4. **Natural Conversation**: The chat-like interaction feels natural for helpdesk scenarios

In **Module 6** (Part 3), we'll explore **Handoff** orchestration for dynamic routing and escalation patterns.

### 📚 Concept: Multi-Agent Collaboration

| Single Agent | Multi-Agent Group Chat |
|--------------|------------------------|
| Jack of all trades | Each is a specialist |
| Complex instructions | Focused roles |
| One perspective | Multiple perspectives |

**Group Chat Architecture:**

```
┌────────────────────────────────────────────────┐
│            GROUP CHAT WORKFLOW                 │
├────────────────────────────────────────────────┤
│                                                │
│  ┌──────────┐        ┌──────────┐             │
│  │LearnAgent│        │GitHubAgent│            │
│  │📚 Docs   │        │🐙 Issues  │            │
│  └────┬─────┘        └────┬─────┘             │
│       │                   │                    │
│       └─────────┬─────────┘                    │
│                 ↓                              │
│        ┌────────────────┐                      │
│        │ GroupManager   │ ← Orchestrates       │
│        └────────────────┘                      │
│                 │                              │
│  1. User asks about Azure Functions error      │
│  2. Manager → LearnAgent: Find docs            │
│  3. Manager → GitHubAgent: Create issue        │
│  4. Manager → User: Summary                    │
└────────────────────────────────────────────────┘
```

<div class="info" data-title="🔌 What is MCP?">

> **MCP** (Model Context Protocol) lets agents connect to external tools:
> - **MCP Server**: Exposes capabilities (search, create issues)
> - **MCP Client**: Your agent connects to servers
> - Examples: GitHub MCP, MS Learn MCP, Playwright MCP

</div>

### 🧠 Pseudo-code

```
1. CREATE CLIENT: Shared by all agents
2. CREATE SPECIALISTS:
   - LearnAgent: MCP for Microsoft Learn
   - GitHubAgent: MCP for GitHub operations
3. CREATE MANAGER: Coordinates workflow order
4. BUILD GROUP CHAT: GroupChatBuilder().add_participant()...
5. RUN STREAM: Each event shows which agent speaks
```

### 🔨 Step-by-Step Exercise

Create `src/module5_group_chat.py`:

**Step 1: Imports**

<details>
<summary>💡 Hint</summary>

```python
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.workflows import GroupChatBuilder
```

</details>

**Step 2: Create MCP Tool**

<details>
<summary>💡 Hint</summary>

```python
async with MCPStreamableHTTPTool(
    name="mslearn",
    description="Search Microsoft Learn documentation",
    url=os.getenv("MCP_MSLEARN_URL"),
    headers={"Authorization": f"Bearer {os.getenv('MCP_API_KEY')}"},
) as learn_tool:
    # Use learn_tool with agent
```

</details>

**Step 3: Create Specialist Agent**

<details>
<summary>💡 Hint</summary>

```python
learn_agent = ChatAgent(
    chat_client=client,
    name="LearnAgent",
    instructions="""Documentation specialist.
    - Search Microsoft Learn
    - Provide citations
    - Cite as: [Doc: Title](URL)""",
    tools=learn_tool,
)
```

</details>

**Step 4: Build Group Chat**

<details>
<summary>💡 Hint</summary>

```python
workflow = (
    GroupChatBuilder()
    .add_participant(learn_agent)
    .add_participant(github_agent)
    .set_manager(agent=manager)
    .with_max_rounds(5)
    .build()
)

async for event in workflow.run_stream(task):
    if hasattr(event, 'agent_name'):
        print(f"[{event.agent_name}]: {event.text}")
```

</details>

### ✅ Full Solution

<details>
<summary>📄 Complete Module 5 Code</summary>

```python
"""Module 5: Group Chat - Multi-agent collaboration."""
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
    
    async with MCPStreamableHTTPTool(
        name="mslearn",
        description="Search Microsoft Learn documentation",
        url=os.getenv("MCP_MSLEARN_URL"),
        headers={"Authorization": f"Bearer {os.getenv('MCP_API_KEY')}"},
    ) as learn_tool:
        
        learn_agent = ChatAgent(
            chat_client=client,
            name="LearnAgent",
            instructions="""Documentation specialist.
            - Search Microsoft Learn for documentation
            - Cite sources as [Doc: Title](URL)""",
            tools=learn_tool,
        )
        
        async with MCPStreamableHTTPTool(
            name="github",
            description="Manage GitHub issues",
            url=os.getenv("MCP_GITHUB_URL"),
            headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
        ) as github_tool:
            
            github_agent = ChatAgent(
                chat_client=client,
                name="GitHubAgent",
                instructions="""GitHub issue manager.
                - Create issues with proper labels
                - Add comments with context
                - Link to relevant documentation""",
                tools=github_tool,
            )
            
            manager = ChatAgent(
                chat_client=client,
                name="GroupManager",
                instructions="""Manage the discussion.
                Workflow:
                1. LearnAgent finds documentation
                2. GitHubAgent creates issue
                3. Summarize outcome""",
            )
            
            workflow = (
                GroupChatBuilder()
                .add_participant(learn_agent)
                .add_participant(github_agent)
                .set_manager(agent=manager)
                .with_max_rounds(5)
                .build()
            )
            
            task = """
            User reported: "Azure Functions deployment fails 
            with 'Out of memory' error"
            
            Find documentation and create an issue.
            """
            
            print("Starting Group Chat...\n")
            
            async for event in workflow.run_stream(task):
                if hasattr(event, 'agent_name') and hasattr(event, 'text'):
                    print(f"[{event.agent_name}]: {event.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

<div class="hint" data-title="MCP Connection Issues?">

> - **Connection refused**: Check MCP server URL
> - **Auth failed**: Verify API keys
> - **Timeout**: Add retry logic
>
> Test: `curl -H "Authorization: Bearer $MCP_API_KEY" $MCP_MSLEARN_URL/health`

</div>

<div class="task" data-title="🎯 Challenge">

> Add a third `CodeReviewAgent` and update the workflow!

</div>

---

## ✅ Part 2 Complete!

You've learned:

| Module | Skill |
|--------|-------|
| 4 | Azure AI Search / RAG integration |
| 5 | Multi-agent Group Chat with MCP |

<div class="info" data-title="Next Steps">

> **[Continue to Part 3: Production Ready →](/workshop/part3-production.md)**
>
> Learn about orchestration, observability, and evaluation!

</div>
