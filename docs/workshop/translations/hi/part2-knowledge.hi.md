---
published: true
type: workshop
title: "भाग 2: नॉलेज इंटीग्रेशन"
short_title: "नॉलेज"
description: Azure AI Search RAG और MCP के साथ Multi-Agent Group Chat
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 60
tags: rag, azure-ai-search, multi-agent, mcp, group-chat
banner_url: ../../../assets/banner.jpg
navigation_levels: 2
sections_title:
  - परिचय
  - भाग 1 का कोड
  - मॉड्यूल 4 - Azure AI Search
  - मॉड्यूल 5 - Group Chat
  - भाग 2 पूर्ण
---

# भाग 2: नॉलेज इंटीग्रेशन

![वर्कशॉप बैनर](../../../assets/banner.jpg)

> 🌍 **[← भाग 1](./part1-basics.hi.md)** | **[🏠 होम](./index.hi.md)** | **[भाग 3 →](./part3-production.hi.md)**

## 📦 भाग 1 का कोड

<details>
<summary>📁 प्रोजेक्ट स्ट्रक्चर (क्लिक करें)</summary>

```text
helpdesk-agent/
├── src/
│   ├── module1_simple_agent.py      # Streaming के साथ बेसिक एजेंट
│   ├── module2_structured.py        # Pydantic Structured Output
│   └── module3_tools.py             # Function Tools
├── .env                             # Environment Variables
└── requirements.txt                 # Dependencies
```

</details>

<details>
<summary>🔧 मुख्य कंपोनेंट्स (क्लिक करें)</summary>

```python
# बेस क्लाइंट सेटअप (सभी मॉड्यूल्स)
from agents import Agent, Runner
from openai import AsyncAzureOpenAI

client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-10-21"
)

# Structured Output के लिए Pydantic मॉडल (मॉड्यूल 2)
class TicketExtraction(BaseModel):
    ticket_id: str
    customer_name: str
    issue_type: str
    priority: str
    summary: str

# Function Tools (मॉड्यूल 3)
@function_tool
def get_ticket_status(ticket_id: str) -> str:
    """टिकट की वर्तमान स्थिति प्राप्त करें।"""
    # टिकट लुकअप लॉजिक
    return f"Ticket {ticket_id}: In Progress"
```

</details>

<div class="info" data-title="भाग 1 पूरा नहीं किया?">

> पहले [भाग 1: बुनियादी बातें](./part1-basics.hi.md) पूरा करें बेस सेटअप के लिए।

</div>

---

यह भाग RAG और multi-agent collaboration को कवर करता है:

| मॉड्यूल | सामग्री |
|--------|---------|
| **मॉड्यूल 4** | Azure AI Search के साथ RAG |
| **मॉड्यूल 5** | MCP के साथ Group Chat |

---

## मॉड्यूल 4 — Azure AI Search RAG

Retrieval-Augmented Generation के साथ documents से जवाब दें।

### 📚 कॉन्सेप्ट: RAG क्या है?

```
┌─────────────────────────────────────────────────────────┐
│              RAG Architecture                           │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   👤 Query ──→ 🔍 Vector Search ──→ 📄 Documents        │
│        │               ↓                                │
│        │         Top K Results                          │
│        │               ↓                                │
│        └────────→ 🧠 LLM ←─── Context + Query           │
│                       ↓                                 │
│                  📝 Response                            │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### RAG के फायदे

| बिना RAG के | RAG के साथ |
|-------------|-------------|
| Training तक सीमित knowledge | Real-time documents |
| ग़लत जानकारी का risk (Hallucination) | Source-based answers |
| General responses | Context-specific |

### 🧠 Pseudocode

```
ALGORITHM: Helpdesk RAG Agent

1. SEARCH CLIENT कॉन्फ़िगर करें:
   - Azure AI Search endpoint
   - FAQ index से कनेक्ट करें

2. @ai_function के साथ RETRIEVAL TOOL परिभाषित करें:
   - search_faq(query) → results
   - Vector + Semantic search का उपयोग करें
   - Top 5 results return करें

3. RAG AGENT बनाएं:
   - Instructions: "sources cite करें"
   - Tool: search_faq

4. USER QUERY:
   - Agent → Tool call → Documents retrieve
   - Agent → Grounded response generate
```

### 🔨 एक्सरसाइज

`src/module4_rag_agent.py` बनाएं।

<details>
<summary>💡 Hint: Search Client Setup</summary>

```python
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=DefaultAzureCredential(),
)
```

</details>

<details>
<summary>💡 Hint: Search Tool परिभाषित करना</summary>

```python
@ai_function
def search_faq(query: str) -> list[dict]:
    """FAQ knowledge base में search करें।
    
    Args:
        query: User का question या search terms
    
    Returns:
        Relevant documents की list
    """
    results = search_client.search(
        search_text=query,
        query_type="semantic",
        semantic_configuration_name="default",
        top=5,
    )
    
    return [
        {
            "title": r["title"],
            "content": r["content"],
            "source": r["source"],
        }
        for r in results
    ]
```

</details>

<details>
<summary>💡 Hint: RAG Agent</summary>

```python
agent = client.create_agent(
    name="FAQAgent",
    instructions="""आप FAQ-based assistant हैं।
    User questions का जवाब देने के लिए search_faq tool का उपयोग करें।
    हमेशा sources cite करें।
    Knowledge base में जानकारी नहीं होने पर स्पष्ट कहें।""",
    tools=[search_faq],
)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 4</summary>

```python
"""Module 4: Azure AI Search के साथ RAG Agent।"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient


# Search client initialize करें
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=DefaultAzureCredential(),
)


@ai_function
def search_faq(query: str) -> list[dict]:
    """Helpdesk FAQ knowledge base में search करें।
    
    Args:
        query: User का question या search keywords
    
    Returns:
        Relevant FAQ articles की list जिसमें title, content और source हैं
    """
    results = search_client.search(
        search_text=query,
        query_type="semantic",
        semantic_configuration_name="default",
        top=5,
        select=["title", "content", "category", "source"],
    )
    
    return [
        {
            "title": doc["title"],
            "content": doc["content"][:500],  # Preview truncate करें
            "category": doc.get("category", "General"),
            "source": doc.get("source", "FAQ"),
        }
        for doc in results
    ]


async def main() -> None:
    """Azure AI Search RAG के साथ FAQ agent demonstrate करें।"""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="FAQAssistant",
        instructions="""आप company की IT documentation-based assistant हैं।
        
        RULES:
        1. User questions का जवाब देने के लिए search_faq tool का उपयोग करें
        2. हमेशा specific document/article cite करें
        3. FAQ में जानकारी न मिलने पर स्पष्ट कहें
        4. "Based on FAQ..." के साथ prefix करें जब relevant documents हों
        5. Step-by-step instructions use करें जहां applicable हो""",
        tools=[search_faq],
    )
    
    questions = [
        "मैं VPN कैसे configure करूं?",
        "Office 365 license के लिए process क्या है?",
        "WiFi काम नहीं कर रहा, क्या करूं?",
    ]
    
    for question in questions:
        print(f"\n{'='*60}")
        print(f"👤 Question: {question}")
        print("-" * 60)
        
        result = await agent.run(question)
        print(f"🤖 Answer:\n{result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module4_rag_agent.py
```

---

## मॉड्यूल 5 — MCP के साथ Multi-Agent Group Chat

Model Context Protocol (MCP) के साथ specialized agents के बीच collaboration।

### 📚 कॉन्सेप्ट: MCP क्या है?

```
┌─────────────────────────────────────────────────────────┐
│                   MCP Architecture                      │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────┐    ┌──────────────────┐                 │
│   │  Agent   │◄──►│   MCP Client     │                 │
│   └──────────┘    └────────┬─────────┘                 │
│                            │ Protocol                   │
│                   ┌────────▼─────────┐                 │
│                   │   MCP Server     │                 │
│                   └────────┬─────────┘                 │
│                            │                            │
│              ┌─────────────┼─────────────┐             │
│              ▼             ▼             ▼             │
│         🔧 Tools      📚 Resources   💬 Prompts       │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Group Chat Pattern

```
┌─────────────────────────────────────────────┐
│              Group Chat                      │
├─────────────────────────────────────────────┤
│                                              │
│  👤 User: "VPN connection failed"            │
│       ↓                                      │
│  🔀 Orchestrator (routing)                   │
│       ↓                                      │
│  🔧 NetworkAgent: "Check settings..."        │
│       ↓                                      │
│  📚 KnowledgeAgent: "According to KB..."     │
│       ↓                                      │
│  ✅ Orchestrator: Combine & Respond          │
│                                              │
└─────────────────────────────────────────────┘
```

### 🧠 Pseudocode

```
ALGORITHM: MCP Group Chat

1. MCP SERVER को connect करें:
   - GitHub MCP server
   - Tools: search_issues, create_issue

2. SPECIALIZED AGENTS परिभाषित करें:
   - NetworkAgent: Network issues
   - HardwareAgent: Hardware issues
   - SoftwareAgent: Software issues
   - KnowledgeAgent: KB search (RAG)

3. GROUP CHAT बनाएं:
   - Agents की list
   - Orchestrator strategy

4. EXECUTION:
   - User message → Orchestrator
   - Orchestrator → Select best agent(s)
   - Agents → Collaborate/respond
   - Orchestrator → Final answer
```

### 🔨 एक्सरसाइज

`src/module5_group_chat_mcp.py` बनाएं।

<details>
<summary>💡 Hint: MCP Server कनेक्ट करना</summary>

```python
from agent_framework.mcp import MCPServerManager

mcp_manager = MCPServerManager()
await mcp_manager.connect_server(
    name="github",
    command="npx",
    args=["-y", "@modelcontextprotocol/server-github"],
    env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
)
```

</details>

<details>
<summary>💡 Hint: MCP Tools के साथ Agent</summary>

```python
github_tools = mcp_manager.get_tools("github")

issue_agent = client.create_agent(
    name="GitHubIssueAgent",
    instructions="GitHub issues manage करें...",
    tools=github_tools,
)
```

</details>

<details>
<summary>💡 Hint: Group Chat Setup</summary>

```python
from agent_framework import GroupChat

group_chat = GroupChat(
    agents=[network_agent, hardware_agent, knowledge_agent],
    orchestrator_strategy="round_robin",  # या "smart_routing"
)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 5</summary>

```python
"""Module 5: MCP के साथ Multi-Agent Group Chat।"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function, GroupChat
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.mcp import MCPServerManager


async def main() -> None:
    """MCP integration के साथ multi-agent group chat demonstrate करें।"""
    
    # MCP manager initialize करें
    mcp_manager = MCPServerManager()
    
    # GitHub MCP server से connect करें
    await mcp_manager.connect_server(
        name="github",
        command="npx",
        args=["-y", "@modelcontextprotocol/server-github"],
        env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
    )
    
    github_tools = mcp_manager.get_tools("github")
    
    # Client setup करें
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Specialized agents बनाएं
    network_agent = client.create_agent(
        name="NetworkSpecialist",
        instructions="""आप network issues के expert हैं।
        VPN, WiFi, connectivity problems handle करें।
        Diagnosis steps और solutions provide करें।""",
    )
    
    hardware_agent = client.create_agent(
        name="HardwareSpecialist",
        instructions="""आप hardware issues के expert हैं।
        Laptops, peripherals, physical equipment problems handle करें।
        Replacement आवश्यक होने पर escalation recommend करें।""",
    )
    
    software_agent = client.create_agent(
        name="SoftwareSpecialist",
        instructions="""आप software issues के expert हैं।
        Applications, OS, updates problems handle करें।
        Configuration और installation guide करें।""",
    )
    
    github_agent = client.create_agent(
        name="GitHubAgent",
        instructions="""आप GitHub integration specialist हैं।
        MCP tools से issues search और create करें।
        Support issues के लिए GitHub use करें जहां relevant हो।""",
        tools=github_tools,
    )
    
    # Group Chat बनाएं
    group_chat = GroupChat(
        agents=[network_agent, hardware_agent, software_agent, github_agent],
        orchestrator_instructions="""आप IT support orchestrator हैं।
        User query के आधार पर सबसे relevant agent(s) select करें।
        Multiple agents को collaborate करने दें अगर जरूरी हो।
        Final cohesive response synthesize करें।""",
        strategy="smart_routing",
    )
    
    # Test scenarios
    scenarios = [
        "VPN disconnect हो जाता है हर 10 minutes में",
        "नया laptop setup करना है और software install करने हैं",
        "यह recurring issue है, GitHub में track करना चाहिए",
    ]
    
    for scenario in scenarios:
        print(f"\n{'='*60}")
        print(f"👤 User: {scenario}")
        print("-" * 60)
        
        result = await group_chat.run(scenario)
        
        print(f"\n🤖 Response:\n{result.text}")
        print(f"\n📊 Agents involved: {', '.join(result.agents_used)}")
    
    # MCP cleanup
    await mcp_manager.disconnect_all()


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
# GitHub token set करें
export GITHUB_TOKEN="your-github-token"

python src/module5_group_chat_mcp.py
```

### 🔧 Advanced: Custom MCP Server

<details>
<summary>📄 Custom MCP Server Example</summary>

```python
"""Custom MCP server for helpdesk tools."""
from mcp.server import Server
from mcp.types import Tool

app = Server("helpdesk-mcp")

@app.tool()
async def check_system_status(system_name: str) -> dict:
    """IT system का status check करें।"""
    # Integration with monitoring system
    return {
        "system": system_name,
        "status": "operational",
        "uptime": "99.9%",
    }

@app.tool()
async def create_incident(
    title: str,
    priority: str,
    affected_system: str,
) -> dict:
    """Incident management में नई incident बनाएं।"""
    return {
        "incident_id": "INC-001",
        "status": "created",
    }
```

</details>

<div class="task" data-title="🎯 Challenge">

> एक custom MCP server बनाएं जो internal ticketing system से connect करे।

</div>

---

> 🌍 **[← भाग 1: बुनियादी बातें](./part1-basics.hi.md)** | **[🏠 होम](./index.hi.md)** | **[भाग 3: प्रोडक्शन →](./part3-production.hi.md)**
