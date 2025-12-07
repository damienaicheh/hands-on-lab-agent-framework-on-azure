---
published: true
type: workshop
title: "Part 4: Advanced & Resources"
short_title: "Advanced & Resources"
description: Redis persistence, complete project structure, and production resources
level: advanced
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 45
tags: redis, persistence, architecture, production, resources, conclusion
banner_url: ../assets/banner.jpg
navigation_levels: 1
sections_title:
  - 🏠 Navigation
  - Code from Parts 1-3
  - Module 9 - Redis Integration
  - Conclusion
  - Resources
---

# Part 4: Advanced & Resources

![Workshop Banner](../assets/banner.jpg)

> 🌍 **[← Part 3: Production Ready](/workshop/part3-production.md)** | **[🏠 Workshop Index](/workshop/index.md)**

---

## 🏠 Navigation

<div class="tip" data-title="Workshop Navigation">

> **📚 All Parts:**
> - [🏠 Workshop Home](/workshop/index.md)
> - [Part 1: Getting Started](/workshop/part1-basics.md)
> - [Part 2: Knowledge & Collaboration](/workshop/part2-knowledge.md)
> - [Part 3: Production Ready](/workshop/part3-production.md)
> - [Part 4: Advanced & Resources](/workshop/part4-advanced.md) *(current)*
>
> **🌍 This page in other languages:**
> - [🇫🇷 Français](/workshop/translations/fr/part4-advanced.fr.md)
> - [🇪🇸 Español](/workshop/translations/es/part4-advanced.es.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part4-advanced.hi.md)

</div>

---

Final part of the workshop.

---

## 📦 Code from Parts 1-3

Before starting this part, ensure you have the complete codebase from previous parts:

<details>
<summary>📁 Complete Project Structure (click to expand)</summary>

```
helpdesk-agent/
├── .env                            # All environment variables
├── requirements.txt                # Dependencies
├── pyproject.toml                  # Project config
└── src/
    ├── module1_simple_agent.py     # Part 1: Simple streaming agent
    ├── module2_structured.py       # Part 1: Pydantic structured output
    ├── module3_tools.py            # Part 1: Function tools
    ├── module4_rag.py              # Part 2: AI Search RAG
    ├── module5_group_chat.py       # Part 2: Group Chat + MCP
    ├── module6_orchestration.py    # Part 3: Handoff orchestration
    ├── module7_observability.py    # Part 3: OpenTelemetry tracing
    └── module8_evaluation.py       # Part 3: Quality evaluation
```

</details>

<details>
<summary>🔧 Key Components from Part 3 (click to expand)</summary>

```python
# Orchestration pattern from Module 6
from agent_framework import HandoffOrchestrator

orchestrator = HandoffOrchestrator(
    agents=[analyst, resolver, escalator],
    default_agent=analyst,
)

# Observability setup from Module 7
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
)
tracer = trace.get_tracer(__name__)

# Evaluation pattern from Module 8
async def evaluate_agent() -> dict:
    """Evaluate agent against test cases."""
    test_cases = [
        {"input": "VPN not working", "expected_category": "network"},
        {"input": "Laptop won't start", "expected_category": "hardware"},
    ]
    # Run tests and compute metrics...
```

</details>

<details>
<summary>📋 All Environment Variables (click to expand)</summary>

```bash
# .env file - complete list for Part 4
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_INDEX_NAME=helpdesk-faq

# MCP & GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Observability
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...

# New for Part 4 - Redis
REDIS_CONNECTION_STRING=rediss://your-redis.redis.cache.windows.net:6380?password=xxx
```

</details>

<div class="info" data-title="Haven't completed Parts 1-3?">

> Complete all previous parts first:
> - [Part 1: Getting Started](/workshop/part1-basics.md)
> - [Part 2: Knowledge & Collaboration](/workshop/part2-knowledge.md)  
> - [Part 3: Production Ready](/workshop/part3-production.md)
>
> Or use the code snippets above to set up your project.

</div>

---

| Section | Content |
|---------|---------|
| **Module 9** | Redis persistence for memory |
| **Conclusion** | Architecture summary |
| **Resources** | Go further + links |

---

## Module 9 — Redis Integration

Add conversation persistence with Azure Managed Redis.

### 📚 Concept: Why Persistence?

| Without Persistence | With Redis |
|--------------------|------------|
| "What was my last issue?" → "I don't know" | "You reported VPN issues on Monday" |
| Repeat troubleshooting every time | Build on previous solutions |
| State lost on restart | Resume conversations anytime |

**Architecture:**

```
SESSION 1 (Monday)
┌────────────────────────────────────┐
│ User: "VPN keeps disconnecting"    │
│ Agent: "Try resetting adapter..."  │
│           ↓                        │
│     ┌──────────────┐               │
│     │ REDIS STORE  │               │
│     │ • History    │               │
│     │ • Context    │               │
│     └──────────────┘               │
└────────────────────────────────────┘
            ↓
SESSION 2 (Wednesday)  
┌────────────────────────────────────┐
│ User: "VPN issue again"            │
│ Agent: "I see you had this Monday. │
│         Let's try next steps..."   │
└────────────────────────────────────┘
```

| Component | Purpose |
|-----------|---------|
| **RedisProvider** | Semantic memory (facts, preferences) |
| **RedisChatMessageStore** | Conversation history |
| **thread_id** | Links sessions for same conversation |
| **user_id** | Groups data for specific user |

### 🧠 Pseudo-code

```
ALGORITHM: Agent with Redis Memory

1. CONFIGURE REDIS CONNECTION:
   - Connection string from environment
   - Define user_id, thread_id

2. CREATE REDIS PROVIDER:
   - For semantic memory
   - Set index_name and prefix

3. CREATE MESSAGE STORE FACTORY:
   - Returns RedisChatMessageStore
   - Set max_messages limit

4. CREATE AGENT WITH PROVIDERS:
   - context_providers=redis_provider
   - chat_message_store_factory=factory

5. SERIALIZE/DESERIALIZE:
   - thread.serialize() → Save
   - agent.deserialize_thread() → Resume
```

### 🔨 Exercise: Persistent Agent

Create `src/module9_redis_agent.py`.

<details>
<summary>💡 Hint: RedisProvider Configuration</summary>

```python
from agent_framework_redis import RedisProvider

redis_provider = RedisProvider(
    redis_url=os.getenv("REDIS_CONNECTION_STRING"),
    index_name="helpdesk_memory",
    prefix="helpdesk",
    application_id="helpdesk_assistant",
    agent_id="support_agent",
    user_id=user_id,
    thread_id=thread_id,
)
```

</details>

<details>
<summary>💡 Hint: Message Store Factory</summary>

```python
from agent_framework_redis import RedisChatMessageStore

def create_message_store():
    return RedisChatMessageStore(
        redis_url=redis_url,
        thread_id=thread_id,
        key_prefix="chat_messages",
        max_messages=100,
    )
```

</details>

<details>
<summary>💡 Hint: Agent with Persistence</summary>

```python
agent = client.create_agent(
    name="PersistentAssistant",
    instructions="You are a helpful IT assistant with memory...",
    context_providers=redis_provider,
    chat_message_store_factory=create_message_store,
)
```

</details>

<details>
<summary>💡 Hint: Thread Serialization</summary>

```python
# Save at end of session
serialized = await thread.serialize()

# Resume later
resumed_thread = await agent.deserialize_thread(serialized)
result = await agent.run("Continue our conversation", thread=resumed_thread)
```

</details>

### ✅ Solution

<details>
<summary>📄 Complete Module 9 Code</summary>

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
    
    redis_provider = RedisProvider(
        redis_url=redis_url,
        index_name="helpdesk_memory",
        prefix="helpdesk",
        application_id="helpdesk_assistant",
        agent_id="support_agent",
        user_id=user_id,
        thread_id=thread_id,
    )
    
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
        Remember user preferences, previous issues, and solutions.""",
        context_providers=redis_provider,
        chat_message_store_factory=create_message_store,
    )
    
    conversations = [
        "Hi, I'm having VPN issues again",
        "It's the same problem as last week",
        "What else can I try?",
    ]
    
    thread = agent.get_new_thread()
    print("💬 Starting persistent conversation\n")
    
    for message in conversations:
        print(f"User: {message}")
        result = await agent.run(message, thread=thread)
        print(f"Agent: {result.text}\n")
    
    # Save for later
    serialized = await thread.serialize()
    print(f"📦 Thread saved: {len(serialized)} bytes")
    
    # Resume later
    print("\n--- Session resumed ---\n")
    resumed_thread = await agent.deserialize_thread(serialized)
    result = await agent.run("What we discussed?", thread=resumed_thread)
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module9_redis_agent.py
```

<div class="hint" data-title="Redis Connection Issues?">

> - Use `rediss://` (SSL) not `redis://` for Azure
> - Format: `rediss://<name>.redis.cache.windows.net:6380?password=<key>`
> - Test: `redis.from_url(url).ping()` → should return `True`

</div>

<div class="task" data-title="🎯 Challenge">

> Add TTL to expire old conversations after 7 days. Create a helper to list all threads for a user.

</div>

---

## Conclusion

🎉 **Congratulations!** You've built a complete **Helpdesk Ops Assistant**!

### ✅ What You Learned

| Module | Skill |
|--------|-------|
| 1 | Basic agents with Agent Framework |
| 2 | Structured output with Pydantic |
| 3 | Function tools and tool calling |
| 4 | Knowledge integration with AI Search |
| 5 | Multi-agent Group Chat with MCP |
| 6 | Advanced orchestration with Handoff |
| 7 | Observability with OpenTelemetry |
| 8 | Agent evaluation and testing |
| 9 | Persistent memory with Redis |

### 📁 Project Structure

```
helpdesk-ops-assistant/
├── 📁 .github/
│   ├── 📁 agents/                      # Custom Copilot agents
│   │   └── AgentArchitect.agent.md
│   ├── 📁 prompts/                     # Reusable prompts
│   │   └── evaluate-agent.prompt.md
│   └── copilot-instructions.md         # Project-wide instructions
│
├── 📁 infra/                           # Terraform IaC
│   ├── aai.tf                          # Microsoft Foundry
│   ├── ai_search.tf                    # AI Search
│   ├── foundry.tf                      # AI Foundry workspace
│   ├── foundry_models.tf               # Model deployments
│   ├── managed_redis.tf                # Redis
│   ├── log.tf                          # App Insights
│   └── variables.tf
│
├── 📁 src/                             # Python modules
│   ├── module1_simple_agent.py
│   ├── module2_complexity_analyst.py
│   ├── module3_function_tools.py
│   ├── module4_knowledge_agent.py
│   ├── module5_group_chat.py
│   ├── module6_orchestration.py
│   ├── module7_observability.py
│   ├── module8_evaluation.py
│   └── module9_redis_agent.py
│
├── 📁 docs/                            # Workshop documentation
│   ├── workshop.md
│   └── 📁 assets/
│       └── banner.jpg
│
├── .env.example
├── requirements.txt
└── README.md
```

### 🏗️ Architecture Summary

```text
┌─────────────────────────────────────────────────────────────────────┐
│                           📥 INPUT                                  │
│                         👤 User                                     │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      🎯 ORCHESTRATION                               │
│                       🧠 Orchestrator                               │
└───────────┬──────────────────┼──────────────────┬───────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
       ┌─────────┐       ┌───────────┐      ┌────────────┐
       │⚡ Simple │       │👥 Group   │      │🚨 Escalation│
       │         │       │   Chat    │      │            │
       └────┬────┘       └─────┬─────┘      └────────────┘
            │                  │                   
            │           ┌──────┴──────┐            
            │           │  🤖 AGENTS  │            
            │           │ ┌──────────┐│            
            │           │ │📚 Learn  ││            
            │           │ │   Agent  ││            
            │           │ ├──────────┤│            
            │           │ │🐙 GitHub ││            
            │           │ │   Agent  ││            
            │           │ └────┬─────┘│            
            │           └──────┼──────┘            
            │                  │                   
            │                  ▼                   
            │         ┌───────────────┐            
            │         │🔍 AI Search   │            
            │         └───────────────┘            
            │                                      
            └───────────────┬──────────────────────
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        ☁️ AZURE SERVICES                            │
│       💾 Redis Cache         📊 Application Insights                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Resources

### 📚 Core Documentation

| Resource | Link |
|----------|------|
| **Agent Framework GitHub** | [🔗 microsoft/agent-framework](https://github.com/microsoft/agent-framework){target="_blank"} |
| **Agent Framework Docs** | [🔗 learn.microsoft.com](https://learn.microsoft.com/en-us/agent-framework/){target="_blank"} |
| **AI Agents for Beginners** | [🔗 Module 14: Agent Framework](https://microsoft.github.io/ai-agents-for-beginners/14-microsoft-agent-framework/){target="_blank"} |
| **Workflow Samples** | [🔗 Workflows README](https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/README.md){target="_blank"} |

### 🚀 Advanced Features

| Feature | Description | Link |
|---------|-------------|------|
| **Shared State** | Share state between agents | [🔗 Guide](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/shared-states){target="_blank"} |
| **Checkpoints** | Save/restore workflow state | [🔗 Guide](https://learn.microsoft.com/en-us/agent-framework/user-guide/workflows/checkpoints){target="_blank"} |
| **AG-UI** | Build agent UIs with streaming | [🔗 AG-UI Integration](https://learn.microsoft.com/en-us/agent-framework/integrations/ag-ui/){target="_blank"} |

### 🔐 Production & Security

| Topic | Description | Link |
|-------|-------------|------|
| **Azure APIM** | Secure and scale agent APIs | [🔗 APIM Docs](https://learn.microsoft.com/en-us/azure/api-management/){target="_blank"} |
| **GenAI Gateway** | Token-based rate limiting | [🔗 OpenAI Integration](https://learn.microsoft.com/en-us/azure/api-management/api-management-howto-integrate-openai){target="_blank"} |
| **Managed Identities** | Eliminate secrets | [🔗 MI Docs](https://learn.microsoft.com/en-us/azure/active-directory/managed-identities-azure-resources/){target="_blank"} |

### 🔌 MCP (Model Context Protocol)

| Topic | Description | Link |
|-------|-------------|------|
| **MCP Specification** | Open protocol for AI-data connections | [🔗 modelcontextprotocol.io](https://modelcontextprotocol.io/){target="_blank"} |
| **MCP Servers** | Pre-built servers (GitHub, Slack, etc.) | [🔗 Servers Registry](https://github.com/modelcontextprotocol/servers){target="_blank"} |
| **Azure MCP** | Official Azure MCP server | [🔗 Azure MCP](https://github.com/Azure/azure-mcp){target="_blank"} |

### 🏛️ AI Governance

| Topic | Description | Link |
|-------|-------------|------|
| **Content Safety** | Filter harmful content | [🔗 Content Safety](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/){target="_blank"} |
| **Prompt Shields** | Block prompt injection | [🔗 Prompt Shields](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/prompt-shields){target="_blank"} |
| **RAI Dashboard** | Monitor fairness & reliability | [🔗 RAI Dashboard](https://learn.microsoft.com/en-us/azure/machine-learning/concept-responsible-ai-dashboard){target="_blank"} |

### ☁️ Architecture Patterns

| Topic | Description | Link |
|-------|-------------|------|
| **AI on Azure** | Reference architectures | [🔗 AI Architecture](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/){target="_blank"} |
| **RAG Pattern** | Best practices for RAG | [🔗 RAG Guide](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide){target="_blank"} |
| **E2E Chat** | Enterprise chat baseline | [🔗 Baseline Chat](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/architecture/baseline-openai-e2e-chat){target="_blank"} |

---

### 📜 Custom Instructions for Copilot

Create `.github/copilot-instructions.md`:

```markdown
# Helpdesk Ops Assistant - Copilot Instructions

## Project Context
Microsoft Agent Framework project for IT helpdesk with multi-agent orchestration.

## Tech Stack
- Framework: Microsoft Agent Framework (agent-framework package)
- LLM: Azure OpenAI GPT-4o via AzureOpenAIChatClient
- Auth: DefaultAzureCredential (never hardcode keys)
- Async: All operations use async/await

## Code Patterns
- Use @ai_function for tools
- Use Pydantic with response_format= for structured output
- Wrap operations in OpenTelemetry spans

## Workflow Patterns
- Simple: Direct agent.run()
- Group Chat: GroupChatBuilder for collaboration
- Handoff: HandoffBuilder for routing
```

---

### 🐛 Found an Issue?

<div class="task" data-title="Help Us Improve">

> - 🐛 **Bug**: [Open an Issue](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[BUG]%20)
> - 💡 **Feature**: [Request Feature](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[FEATURE]%20)
> - 💬 **Questions**: [Discussions](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions)

</div>

---

### 🚀 Next Steps

1. Add more specialized agents for your use case
2. Implement production error handling
3. Set up CI/CD for agent deployment
4. Configure autoscaling for Azure Functions hosting

---

> 🌍 **[← Part 3: Production Ready](/workshop/part3-production.md)** | **[🏠 Workshop Index](/workshop/index.md)**

<div class="info" data-title="🎉 Workshop Complete!">

> **Thank you for completing this workshop!**
> 
> You've learned to build production-ready AI agents with Microsoft Agent Framework on Azure.
> 
> Share your experience and tag us on social media! 🚀

</div>
