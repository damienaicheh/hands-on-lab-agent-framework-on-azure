---
published: true
type: workshop
title: "भाग 1: बुनियादी बातें"
short_title: "बुनियादी बातें"
description: पूर्वापेक्षाएं, इंफ्रास्ट्रक्चर डिप्लॉयमेंट और पहले एजेंट्स
level: beginner
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 70
tags: prerequisites, terraform, simple-agent, structured-output, tools
banner_url: ../../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - परिचय
  - पूर्वापेक्षाएं
  - इंफ्रास्ट्रक्चर डिप्लॉय
  - मॉड्यूल 1 - सिंपल एजेंट
  - मॉड्यूल 2 - Structured Output
  - मॉड्यूल 3 - Function Tools
  - भाग 1 पूर्ण
---

# भाग 1: बुनियादी बातें

![वर्कशॉप बैनर](../../../assets/banner.jpg)

> 🌍 **[🏠 वर्कशॉप होम](./index.hi.md)** | **[भाग 2 →](./part2-knowledge.hi.md)**

यह भाग प्रारंभिक सेटअप और पहले मॉड्यूल्स को कवर करता है:

| सेक्शन | सामग्री |
|--------|---------|
| **पूर्वापेक्षाएं** | आवश्यक टूल्स और अकाउंट्स |
| **डिप्लॉयमेंट** | Terraform के साथ Azure इंफ्रास्ट्रक्चर |
| **मॉड्यूल 1** | Streaming के साथ सिंपल एजेंट |
| **मॉड्यूल 2** | Pydantic Structured Output |
| **मॉड्यूल 3** | Function Tools |

---

## पूर्वापेक्षाएं (Prerequisites)

### 🛠️ आवश्यक टूल्स

| टूल | वर्जन | उद्देश्य |
|-----|-------|----------|
| [Python](https://www.python.org/downloads/){target="_blank"} | 3.11+ | कोड एक्जीक्यूशन |
| [VS Code](https://code.visualstudio.com/){target="_blank"} | Latest | IDE |
| [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli){target="_blank"} | 2.50+ | Azure मैनेजमेंट |
| [Terraform](https://www.terraform.io/downloads){target="_blank"} | 1.5+ | Infrastructure as Code |
| [Git](https://git-scm.com/){target="_blank"} | Latest | वर्जन कंट्रोल |

### ☁️ आवश्यक अकाउंट्स

| अकाउंट | विवरण |
|--------|--------|
| **Azure** | Contributor रोल के साथ एक्टिव सब्सक्रिप्शन |
| **GitHub** | GitHub MCP सर्वर के लिए |

### 📦 अनुशंसित VS Code Extensions

```bash
code --install-extension ms-python.python
code --install-extension hashicorp.terraform
code --install-extension github.copilot
```

<div class="task" data-title="✅ वेरिफिकेशन">

> अपना सेटअप वेरिफाई करने के लिए यह रन करें:
> ```bash
> python --version && az --version && terraform --version
> ```

</div>

---

## इंफ्रास्ट्रक्चर डिप्लॉय करें

### 🏗️ डिप्लॉय होने वाला आर्किटेक्चर

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    📦 RESOURCE GROUP                              │
│                                                                     │
│  ┌───────────────┐ ┌─────────────┐ ┌──────────────┐ ┌────────────┐  │
│  │🧠 Azure AI    │ │🔍 AI Search │ │💾 Managed    │ │📊 App      │  │
│  │   Foundry    │ │             │ │   Redis      │ │ Insights   │  │
│  └───────────────┘ └─────────────┘ └──────────────┘ └────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 📁 प्रोजेक्ट सेटअप

```bash
# रिपॉजिटरी क्लोन करें
git clone https://github.com/yourorg/hands-on-lab-agent-framework-on-azure.git
cd hands-on-lab-agent-framework-on-azure

# Python एनवायरनमेंट बनाएं
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# डिपेंडेंसीज इंस्टॉल करें
pip install -r requirements.txt
```

### 🚀 Terraform से डिप्लॉय करें

```bash
# Azure में लॉगिन
az login
az account set --subscription "<YOUR_SUBSCRIPTION>"

# इंफ्रास्ट्रक्चर डिप्लॉय करें
cd infra
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

<details>
<summary>💡 Copilot Hint: .env कॉन्फ़िगरेशन</summary>

```
@workspace /infra में Terraform outputs के आधार पर .env फाइल जनरेट करें
```

</details>

### ⚙️ Environment Variables कॉन्फ़िगर करें

रूट में `.env` बनाएं:

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://<your-resource>.search.windows.net
AZURE_SEARCH_INDEX_NAME=helpdesk-faq

# Redis
REDIS_CONNECTION_STRING=rediss://<your-resource>.redis.cache.windows.net:6380?password=<key>

# Application Insights
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...
```

<div class="warning" data-title="⚠️ सुरक्षा">

> `.env` को Git में कभी न पुश करें। यह डिफ़ॉल्ट रूप से `.gitignore` में है।

</div>

---

## मॉड्यूल 1 — सिंपल एजेंट

Response streaming के साथ अपना पहला AI एजेंट बनाएं।

### 📚 कॉन्सेप्ट: एजेंट क्या है?

```
┌─────────────────────────────────────────────────┐
│                    एजेंट                        │
├─────────────────────────────────────────────────┤
│  📝 Instructions (System Prompt)                │
│  🧠 Model (GPT-4o)                              │
│  🔧 Tools (वैकल्पिक)                            │
│  💾 Memory (वैकल्पिक)                           │
└─────────────────────────────────────────────────┘
         ↓
    User Input → Reasoning → Response
```

### 🧠 Pseudocode

```
ALGORITHM: Streaming के साथ सिंपल एजेंट

1. CLIENT कॉन्फ़िगर करें:
   - DefaultAzureCredential का उपयोग करें
   - Azure OpenAI endpoint से कनेक्ट करें

2. AGENT बनाएं:
   - नाम और instructions परिभाषित करें
   - model (gpt-4o) स्पेसिफाई करें

3. STREAMING के साथ एक्जीक्यूट करें:
   - User message भेजें
   - प्रत्येक chunk के लिए:
     - रियल-टाइम में दिखाएं
```

### 🔨 एक्सरसाइज

`src/module1_simple_agent.py` बनाएं।

<details>
<summary>💡 Hint: Client कॉन्फ़िगरेशन</summary>

```python
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient

client = AzureOpenAIChatClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name="gpt-4o",
)
```

</details>

<details>
<summary>💡 Hint: Agent बनाना</summary>

```python
agent = client.create_agent(
    name="HelpdeskAssistant",
    instructions="आप एक IT असिस्टेंट हैं। संक्षिप्त और सहायक रहें।",
)
```

</details>

<details>
<summary>💡 Hint: Streaming</summary>

```python
async for chunk in agent.run_stream("मैं अपना पासवर्ड कैसे रीसेट करूं?"):
    print(chunk.text, end="", flush=True)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 1</summary>

```python
"""Module 1: Streaming के साथ सिंपल एजेंट।"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Streaming के साथ एक सिंपल एजेंट बनाएं और रन करें।"""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="HelpdeskAssistant",
        instructions="""आप एक मैत्रीपूर्ण और कुशल IT असिस्टेंट हैं।
        स्पष्ट step-by-step निर्देश प्रदान करें।
        यदि आवश्यक हो तो clarification जरूर पूछें।""",
    )
    
    print("🤖 Helpdesk एजेंट शुरू हुआ!\n")
    
    question = "मैं अपना ईमेल पासवर्ड कैसे रीसेट कर सकता हूं?"
    print(f"User: {question}\nAssistant: ", end="")
    
    async for chunk in agent.run_stream(question):
        print(chunk.text, end="", flush=True)
    
    print("\n")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module1_simple_agent.py
```

---

## मॉड्यूल 2 — Structured Output

Typed और validated responses के लिए Pydantic का उपयोग करें।

### 📚 कॉन्सेप्ट: Structured Output क्यों?

| बिना Structure के | Pydantic के साथ |
|-------------------|-----------------|
| "High priority, urgent" | `{"priority": "high", "score": 9}` |
| Parse करना मुश्किल | Typed और validated |
| Inconsistent | Schema guaranteed |

### 🧠 Pseudocode

```
ALGORITHM: Complexity Analyst

1. PYDANTIC MODEL परिभाषित करें:
   - Typed fields के साथ TicketAnalysis
   - priority: Literal["low", "medium", "high"]
   - complexity_score: int (1-10)
   - summary: str

2. response_format के साथ AGENT बनाएं:
   - Pydantic class पास करें
   - Framework JSON schema enforce करता है

3. TYPED OBJECT प्राप्त करें:
   - result.data TicketAnalysis का instance है
```

### 🔨 एक्सरसाइज

`src/module2_complexity_analyst.py` बनाएं।

<details>
<summary>💡 Hint: Pydantic Model</summary>

```python
from pydantic import BaseModel, Field
from typing import Literal

class TicketAnalysis(BaseModel):
    priority: Literal["low", "medium", "high"]
    complexity_score: int = Field(ge=1, le=10)
    summary: str = Field(max_length=200)
    suggested_actions: list[str]
```

</details>

<details>
<summary>💡 Hint: response_format के साथ Agent</summary>

```python
agent = client.create_agent(
    name="ComplexityAnalyst",
    instructions="Support tickets का विश्लेषण करें...",
    response_format=TicketAnalysis,
)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 2</summary>

```python
"""Module 2: Pydantic के साथ Structured Output।"""
import asyncio
import os
from pydantic import BaseModel, Field
from typing import Literal
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


class TicketAnalysis(BaseModel):
    """Support ticket का structured analysis।"""
    priority: Literal["low", "medium", "high"]
    complexity_score: int = Field(ge=1, le=10, description="1=simple, 10=बहुत complex")
    category: str = Field(description="Ticket की category")
    summary: str = Field(max_length=200)
    suggested_actions: list[str] = Field(max_items=5)
    estimated_time_minutes: int = Field(ge=5, le=480)


async def main() -> None:
    """Ticket का analysis करें और structured output दें।"""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="ComplexityAnalyst",
        instructions="""आप एक expert IT ticket analyst हैं।
        प्रत्येक ticket का विश्लेषण करें और structured analysis प्रदान करें।""",
        response_format=TicketAnalysis,
    )
    
    ticket = """
    Subject: बार-बार Blue Screen
    User: Finance Department
    Description: मेरे laptop में दिन में कई बार blue screen आता है।
    पिछले Windows update के बाद शुरू हुआ।
    Restart करके देखा लेकिन समस्या बनी हुई है।
    """
    
    print("📋 Ticket का analysis हो रहा है...\n")
    result = await agent.run(f"इस ticket का analysis करें:\n{ticket}")
    
    analysis: TicketAnalysis = result.data
    
    print(f"🎯 Priority: {analysis.priority.upper()}")
    print(f"📊 Complexity: {analysis.complexity_score}/10")
    print(f"📁 Category: {analysis.category}")
    print(f"📝 Summary: {analysis.summary}")
    print(f"⏱️ Estimated Time: {analysis.estimated_time_minutes} min")
    print("\n🔧 Suggested Actions:")
    for i, action in enumerate(analysis.suggested_actions, 1):
        print(f"   {i}. {action}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module2_complexity_analyst.py
```

---

## मॉड्यूल 3 — Function Tools

`@ai_function` decorator के साथ custom capabilities जोड़ें।

### 📚 कॉन्सेप्ट: Tool Calling

```
User: "VPN problem के लिए ticket बनाओ"
    ↓
Agent REASONS → "Ticket बनाना है"
    ↓
Agent CALLS → create_ticket(title="...", priority="high")
    ↓
Function EXECUTES → Returns {"ticket_id": "TK-123"}
    ↓
Agent RESPONDS → "मैंने ticket TK-123 बना दिया है"
```

### 🧠 Pseudocode

```
ALGORITHM: Tools के साथ Agent

1. @ai_function के साथ TOOLS परिभाषित करें:
   - get_ticket_status(ticket_id) → status
   - create_ticket(title, priority) → id
   - search_knowledge(query) → articles

2. tools=[...] के साथ AGENT बनाएं:
   - Decorated functions की list

3. AGENT DECIDES:
   - कब tools call करना है
   - कौन से parameters पास करने हैं
   - Results का उपयोग कैसे करना है
```

### 🔨 एक्सरसाइज

`src/module3_function_tools.py` बनाएं।

<details>
<summary>💡 Hint: Tools परिभाषित करना</summary>

```python
from agent_framework import ai_function

@ai_function
def get_ticket_status(ticket_id: str) -> dict:
    """Support ticket का status प्राप्त करें।
    
    Args:
        ticket_id: Ticket का ID (जैसे: TK-123)
    
    Returns:
        Ticket status की जानकारी
    """
    # Simulation
    return {
        "ticket_id": ticket_id,
        "status": "in_progress",
        "assignee": "tech_support",
    }
```

</details>

<details>
<summary>💡 Hint: Tools के साथ Agent</summary>

```python
agent = client.create_agent(
    name="ToolsAgent",
    instructions="मदद के लिए tools का उपयोग करें...",
    tools=[get_ticket_status, create_ticket, search_kb],
)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 3</summary>

```python
"""Module 3: Function Tools।"""
import asyncio
import os
from datetime import datetime
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient


# Simulated ticket store
TICKETS_DB = {}
TICKET_COUNTER = 100


@ai_function
def get_ticket_status(ticket_id: str) -> dict:
    """Support ticket का current status प्राप्त करें।
    
    Args:
        ticket_id: Ticket का ID (जैसे: TK-101)
    
    Returns:
        Ticket का status और जानकारी
    """
    if ticket_id in TICKETS_DB:
        return TICKETS_DB[ticket_id]
    return {"error": f"Ticket {ticket_id} नहीं मिला"}


@ai_function
def create_ticket(title: str, description: str, priority: str = "medium") -> dict:
    """नया support ticket बनाएं।
    
    Args:
        title: Problem का संक्षिप्त शीर्षक
        description: विस्तृत विवरण
        priority: low, medium, या high
    
    Returns:
        बनाए गए ticket की जानकारी
    """
    global TICKET_COUNTER
    TICKET_COUNTER += 1
    ticket_id = f"TK-{TICKET_COUNTER}"
    
    ticket = {
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat(),
    }
    TICKETS_DB[ticket_id] = ticket
    return ticket


@ai_function
def search_knowledge_base(query: str) -> list[dict]:
    """IT knowledge base में खोजें।
    
    Args:
        query: Search terms
    
    Returns:
        Relevant articles की list
    """
    # Simulated KB
    kb = [
        {"id": "KB001", "title": "Password Reset करना", "relevance": 0.9},
        {"id": "KB002", "title": "VPN Configure करना", "relevance": 0.85},
        {"id": "KB003", "title": "Blue Screen ठीक करना", "relevance": 0.8},
    ]
    return [a for a in kb if query.lower() in a["title"].lower()][:3]


async def main() -> None:
    """Function tools के साथ agent demonstrate करें।"""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="HelpdeskToolsAgent",
        instructions="""आप tools access वाले IT असिस्टेंट हैं।
        Tickets बनाने, solutions खोजने और status check करने के लिए tools का उपयोग करें।""",
        tools=[get_ticket_status, create_ticket, search_knowledge_base],
    )
    
    queries = [
        "एक urgent ticket बनाओ: गिरने के बाद मेरा laptop चालू नहीं हो रहा",
        "Ticket TK-101 का status क्या है?",
        "Knowledge base में VPN के बारे में जानकारी खोजो",
    ]
    
    for query in queries:
        print(f"\n👤 User: {query}")
        result = await agent.run(query)
        print(f"🤖 Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module3_function_tools.py
```

<div class="task" data-title="🎯 Challenge">

> एक `update_ticket_status` tool जोड़ें जो agent को ticket का status बदलने दे।

</div>

---

> 🌍 **[🏠 वर्कशॉप होम](./index.hi.md)** | **[भाग 2: नॉलेज इंटीग्रेशन →](./part2-knowledge.hi.md)**
