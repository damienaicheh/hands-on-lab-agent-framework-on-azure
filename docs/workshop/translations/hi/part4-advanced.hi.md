---
published: true
type: workshop
title: "भाग 4: एडवांस्ड फीचर्स"
short_title: "एडवांस्ड"
description: Redis मेमोरी, निष्कर्ष और अगले कदम
level: advanced
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 50
tags: redis, memory, persistence, conclusion
banner_url: ../../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - परिचय
  - भाग 1-3 का कोड
  - मॉड्यूल 9 - Redis Integration
  - निष्कर्ष
  - संसाधन
---

# भाग 4: एडवांस्ड फीचर्स

![वर्कशॉप बैनर](../../../assets/banner.jpg)

> 🌍 **[← भाग 3](./part3-production.hi.md)** | **[🏠 होम](./index.hi.md)**

## 📦 भाग 1-3 का कोड

<details>
<summary>📁 पूर्ण प्रोजेक्ट स्ट्रक्चर (क्लिक करें)</summary>

```text
helpdesk-agent/
├── src/
│   ├── module1_simple_agent.py      # Streaming के साथ बेसिक एजेंट
│   ├── module2_structured.py        # Pydantic Structured Output
│   ├── module3_tools.py             # Function Tools
│   ├── module4_ai_search.py         # RAG Integration
│   ├── module5_group_chat.py        # MCP के साथ Multi-Agent
│   ├── module6_orchestration.py     # Handoff Orchestration
│   ├── module7_observability.py     # OpenTelemetry Traces
│   └── module8_evaluation.py        # Agent Evaluation
├── .env
└── requirements.txt
```

</details>

<details>
<summary>🔧 मुख्य कंपोनेंट्स (क्लिक करें)</summary>

```python
# Orchestration Pattern (मॉड्यूल 6)
triage_agent = Agent(
    name="Triage",
    instructions="उचित एजेंट को रूट करें",
    handoffs=[billing_agent, technical_agent]
)

# Observability Setup (मॉड्यूल 7)
from opentelemetry import trace
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
)

# Evaluation Pattern (मॉड्यूल 8)
from agents import evaluate

result = await evaluate(
    agent=support_agent,
    test_cases=test_dataset,
    evaluators=[accuracy_evaluator, relevance_evaluator]
)
```

</details>

<details>
<summary>🔐 सभी Environment Variables (क्लिक करें)</summary>

```bash
# .env - पूर्ण वर्कशॉप कॉन्फ़िगरेशन
# भाग 1: Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_KEY=xxx
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# भाग 2: Azure AI Search
AZURE_SEARCH_ENDPOINT=https://xxx.search.windows.net
AZURE_SEARCH_KEY=xxx
AZURE_SEARCH_INDEX=helpdesk-index

# भाग 3: Application Insights
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx

# भाग 4: Azure Managed Redis (अभी जोड़ें)
REDIS_CONNECTION_STRING=rediss://xxx.redis.cache.windows.net:6380
```

</details>

<div class="info" data-title="पिछले भाग पूरे नहीं किए?">

> पूर्ण सॉल्यूशन के लिए [भाग 1](./part1-basics.hi.md), [भाग 2](./part2-knowledge.hi.md) और [भाग 3](./part3-production.hi.md) पूरा करें।

</div>

---

यह अंतिम भाग advanced patterns और निष्कर्ष को कवर करता है:

| सेक्शन | सामग्री |
|--------|---------|
| **मॉड्यूल 9** | Redis के साथ Persistent Memory |
| **निष्कर्ष** | Summary और अगले कदम |
| **संसाधन** | आगे पढ़ने के लिए |

---

## मॉड्यूल 9 — Redis Persistent Memory

Stateful conversations के लिए Azure Managed Redis।

### 📚 कॉन्सेप्ट: Persistent Memory क्यों?

```
┌─────────────────────────────────────────────────────────┐
│              Memory Architecture                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   ┌──────────────┐        ┌──────────────────┐         │
│   │  In-Memory   │   vs   │   Redis Memory   │         │
│   └──────────────┘        └──────────────────┘         │
│   • Session-only          • Persistent                  │
│   • Single instance       • Distributed                 │
│   • Lost on restart       • Survives restarts           │
│   • Fast but volatile     • Fast AND durable            │
│                                                         │
│   ──────────────────────────────────────────────────    │
│                                                         │
│   User A ─────┐                                         │
│               ├──→ Redis ←──→ User context             │
│   User B ─────┘      │                                  │
│                      └──→ Conversation history          │
│                      └──→ User preferences              │
│                      └──→ Session state                 │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Memory Use Cases

| Use Case | उदाहरण |
|----------|--------|
| **Conversation History** | Previous interactions याद रखना |
| **User Preferences** | Language, notification settings |
| **Session State** | Current workflow position |
| **Shared Context** | Multi-agent shared memory |
| **Caching** | Frequent queries के results cache |

### 🧠 Pseudocode

```
ALGORITHM: Redis Memory Integration

1. REDIS CLIENT कॉन्फ़िगर करें:
   - Azure Managed Redis से connect करें
   - SSL/TLS enable करें

2. MEMORY PROVIDER बनाएं:
   - RedisMemoryProvider class
   - User session management
   - TTL configuration

3. AGENT में INTEGRATE करें:
   - memory=redis_memory
   - Automatic save/load

4. MEMORY OPERATIONS:
   - add_message(): New message save करें
   - get_history(): Previous messages लें
   - clear_session(): Session clean करें
```

### 🔨 एक्सरसाइज

`src/module9_redis_memory.py` बनाएं।

<details>
<summary>💡 Hint: Redis Connection</summary>

```python
import redis.asyncio as redis

redis_client = redis.Redis.from_url(
    os.getenv("REDIS_CONNECTION_STRING"),
    decode_responses=True,
    ssl=True,
)
```

</details>

<details>
<summary>💡 Hint: Memory Provider</summary>

```python
from agent_framework.memory import MemoryProvider

class RedisMemoryProvider(MemoryProvider):
    def __init__(self, redis_client, ttl_hours: int = 24):
        self.redis = redis_client
        self.ttl = ttl_hours * 3600
    
    async def add_message(self, session_id: str, role: str, content: str):
        key = f"chat:{session_id}"
        message = {"role": role, "content": content}
        await self.redis.rpush(key, json.dumps(message))
        await self.redis.expire(key, self.ttl)
    
    async def get_history(self, session_id: str) -> list[dict]:
        key = f"chat:{session_id}"
        messages = await self.redis.lrange(key, 0, -1)
        return [json.loads(m) for m in messages]
```

</details>

<details>
<summary>💡 Hint: Agent with Memory</summary>

```python
agent = client.create_agent(
    name="MemoryAgent",
    instructions="Previous conversation का context use करें...",
    memory=redis_memory,
)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 9</summary>

```python
"""Module 9: Redis Persistent Memory।"""
import asyncio
import json
import os
from datetime import datetime
from typing import Optional
import redis.asyncio as redis
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.memory import MemoryProvider


class RedisMemoryProvider(MemoryProvider):
    """Azure Managed Redis के साथ persistent memory।"""
    
    def __init__(
        self,
        redis_client: redis.Redis,
        ttl_hours: int = 24,
        max_messages: int = 50,
    ):
        self.redis = redis_client
        self.ttl = ttl_hours * 3600
        self.max_messages = max_messages
    
    async def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
        metadata: Optional[dict] = None,
    ) -> None:
        """Conversation में message add करें।"""
        key = f"chat:{session_id}:messages"
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
        }
        
        await self.redis.rpush(key, json.dumps(message))
        await self.redis.ltrim(key, -self.max_messages, -1)
        await self.redis.expire(key, self.ttl)
    
    async def get_history(
        self,
        session_id: str,
        limit: int = 20,
    ) -> list[dict]:
        """Conversation history retrieve करें।"""
        key = f"chat:{session_id}:messages"
        messages = await self.redis.lrange(key, -limit, -1)
        return [json.loads(m) for m in messages]
    
    async def set_context(
        self,
        session_id: str,
        context: dict,
    ) -> None:
        """Session context store करें।"""
        key = f"chat:{session_id}:context"
        await self.redis.set(key, json.dumps(context))
        await self.redis.expire(key, self.ttl)
    
    async def get_context(self, session_id: str) -> dict:
        """Session context retrieve करें।"""
        key = f"chat:{session_id}:context"
        context = await self.redis.get(key)
        return json.loads(context) if context else {}
    
    async def clear_session(self, session_id: str) -> None:
        """Session का सारा data clear करें।"""
        keys = await self.redis.keys(f"chat:{session_id}:*")
        if keys:
            await self.redis.delete(*keys)


class HelpdeskSessionManager:
    """Helpdesk sessions manage करें।"""
    
    def __init__(self, memory: RedisMemoryProvider):
        self.memory = memory
    
    async def start_session(self, user_id: str) -> str:
        """नया session start करें।"""
        session_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        await self.memory.set_context(session_id, {
            "user_id": user_id,
            "started_at": datetime.now().isoformat(),
            "status": "active",
            "issue_category": None,
            "escalated": False,
        })
        
        return session_id
    
    async def update_category(self, session_id: str, category: str) -> None:
        """Issue category update करें।"""
        context = await self.memory.get_context(session_id)
        context["issue_category"] = category
        await self.memory.set_context(session_id, context)
    
    async def mark_escalated(self, session_id: str) -> None:
        """Session को escalated mark करें।"""
        context = await self.memory.get_context(session_id)
        context["escalated"] = True
        context["escalated_at"] = datetime.now().isoformat()
        await self.memory.set_context(session_id, context)


async def main() -> None:
    """Redis persistent memory demonstrate करें।"""
    
    # Redis client
    redis_client = redis.Redis.from_url(
        os.getenv("REDIS_CONNECTION_STRING"),
        decode_responses=True,
    )
    
    # Memory provider
    memory = RedisMemoryProvider(
        redis_client=redis_client,
        ttl_hours=24,
        max_messages=50,
    )
    
    # Session manager
    session_manager = HelpdeskSessionManager(memory)
    
    # Client
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Agent with memory
    agent = client.create_agent(
        name="MemoryAgent",
        instructions="""आप persistent memory वाले helpdesk assistant हैं।
        
        CAPABILITIES:
        - Previous conversation याद रखें
        - User के issues track करें
        - Context-aware responses दें
        
        BEHAVIOR:
        - Returning users को recognize करें
        - Previous issues reference करें
        - Personalized experience दें""",
        memory=memory,
    )
    
    # Demo: Multi-turn conversation
    print("💾 Redis Memory Demo")
    print("=" * 60)
    
    # Start session
    session_id = await session_manager.start_session("user_123")
    print(f"📝 Session started: {session_id}")
    
    # Conversation
    messages = [
        "हेलो, मेरा VPN काम नहीं कर रहा है",
        "हाँ, error message है 'Connection timeout'",
        "मेरा OS Windows 11 है",
        "धन्यवाद, यह काम कर गया!",
    ]
    
    for message in messages:
        print(f"\n👤 User: {message}")
        
        # Add user message to memory
        await memory.add_message(session_id, "user", message)
        
        # Get response with history
        history = await memory.get_history(session_id)
        result = await agent.run_with_history(message, history)
        
        # Add assistant response to memory
        await memory.add_message(session_id, "assistant", result.text)
        
        print(f"🤖 Agent: {result.text}")
    
    # Show stored context
    print("\n" + "=" * 60)
    print("📊 Stored Session Context:")
    context = await memory.get_context(session_id)
    print(json.dumps(context, indent=2, ensure_ascii=False))
    
    # Show conversation history
    print("\n📜 Conversation History:")
    history = await memory.get_history(session_id)
    for msg in history:
        role_icon = "👤" if msg["role"] == "user" else "🤖"
        print(f"  {role_icon} {msg['content'][:50]}...")
    
    # Cleanup
    await redis_client.close()


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module9_redis_memory.py
```

### 🔧 Advanced: Semantic Memory

<details>
<summary>📄 Vector-based Memory Search</summary>

```python
class SemanticMemoryProvider(RedisMemoryProvider):
    """Embeddings के साथ semantic memory search।"""
    
    async def search_similar(
        self,
        session_id: str,
        query: str,
        top_k: int = 5,
    ) -> list[dict]:
        """Semantically similar messages खोजें।"""
        
        # Query का embedding generate करें
        query_embedding = await self.get_embedding(query)
        
        # Redis vector search
        key = f"chat:{session_id}:vectors"
        results = await self.redis.ft(key).search(
            query_embedding,
            top_k=top_k,
        )
        
        return results
```

</details>

<div class="task" data-title="🎯 Challenge">

> User preferences (language, notification settings) store करने के लिए memory extend करें।

</div>

---

## 🏁 निष्कर्ष

### 🎯 आपने क्या सीखा

इस workshop में आपने complete AI agent development lifecycle सीखा:

```
┌─────────────────────────────────────────────────────────┐
│                Workshop Journey                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  भाग 1: बुनियादी बातें                                  │
│  ├── ✅ Simple Agent with Streaming                     │
│  ├── ✅ Structured Output (Pydantic)                    │
│  └── ✅ Function Tools                                  │
│                                                         │
│  भाग 2: नॉलेज इंटीग्रेशन                                │
│  ├── ✅ Azure AI Search RAG                             │
│  └── ✅ Multi-Agent Group Chat (MCP)                    │
│                                                         │
│  भाग 3: प्रोडक्शन रेडीनेस                               │
│  ├── ✅ Handoff Orchestration                           │
│  ├── ✅ OpenTelemetry Observability                     │
│  └── ✅ Evaluation & Testing                            │
│                                                         │
│  भाग 4: एडवांस्ड फीचर्स                                 │
│  └── ✅ Redis Persistent Memory                         │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### 🏗️ Complete Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    👤 USER INTERFACE                               │
│              🌐 Web App          🔌 API                           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🎯 ORCHESTRATION LAYER                          │
│           🔀 Triage Agent         🔄 Handoff Manager               │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
         ┌─────────────────┼─────────────────┐
         │                 │                 │
         ▼                 ▼                 ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│ 📡 Network     │ │ 💻 Hardware    │ │ 📦 Software    │
│    Agent      │ │    Agent      │ │    Agent      │
└───────┬───────┘ └───────┬───────┘ └───────┬───────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    📚 KNOWLEDGE LAYER                             │
│             🔍 Azure AI Search    🔌 MCP Servers                   │
└─────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   ☁️ AZURE INFRASTRUCTURE                         │
│        🧠 Azure OpenAI    💾 Redis Memory    📊 App Insights       │
└─────────────────────────────────────────────────────────────────────┘
```

### 💡 Best Practices Summary

| Category | Recommendation |
|----------|----------------|
| **Design** | Single responsibility agents बनाएं |
| **Prompts** | Clear, specific instructions दें |
| **Tools** | Typed parameters के साथ document करें |
| **Memory** | Session और persistent memory अलग रखें |
| **Observability** | सब कुछ trace करें, custom metrics add करें |
| **Evaluation** | Automated tests CI/CD में integrate करें |
| **Security** | Credentials के लिए Managed Identity use करें |

### 🚀 अगले कदम

<div class="columns">

**🏢 Production Deployment**
- [ ] Azure Container Apps पर deploy करें
- [ ] Auto-scaling configure करें
- [ ] Blue-green deployment setup करें

**🔒 Security Hardening**
- [ ] Managed Identity enable करें
- [ ] API rate limiting add करें
- [ ] Input validation strengthen करें

**📈 Advanced Features**
- [ ] Voice interface integrate करें
- [ ] Multi-language support add करें
- [ ] Custom MCP servers बनाएं

</div>

---

## 📚 संसाधन

### Official Documentation

| Resource | Link |
|----------|------|
| Microsoft Foundry | [learn.microsoft.com/azure/ai-foundry](https://learn.microsoft.com/azure/ai-studio/){target="_blank"} |
| Azure OpenAI | [learn.microsoft.com/azure/ai-services/openai](https://learn.microsoft.com/azure/ai-services/openai/){target="_blank"} |
| Azure AI Search | [learn.microsoft.com/azure/search](https://learn.microsoft.com/azure/search/){target="_blank"} |
| Azure Managed Redis | [learn.microsoft.com/azure/redis](https://learn.microsoft.com/azure/azure-cache-for-redis/){target="_blank"} |
| Model Context Protocol | [modelcontextprotocol.io](https://modelcontextprotocol.io/){target="_blank"} |

### Community & Samples

| Resource | Link |
|----------|------|
| Azure Samples GitHub | [github.com/Azure-Samples](https://github.com/Azure-Samples){target="_blank"} |
| AI Agents Samples | [github.com/Azure-Samples/ai-agents](https://github.com/Azure-Samples){target="_blank"} |
| MCP Servers | [github.com/modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers){target="_blank"} |

### Hindi Resources

| Resource | Link |
|----------|------|
| Azure in Hindi | [docs.microsoft.com/hi-in/azure](https://learn.microsoft.com/hi-in/azure/){target="_blank"} |
| Python Documentation | [docs.python.org/hi](https://docs.python.org/3/){target="_blank"} |

---

## 🙏 धन्यवाद!

इस workshop में भाग लेने के लिए धन्यवाद! हमें आशा है कि आपने AI agents development के बारे में बहुत कुछ सीखा।

<div class="tip" data-title="💬 Feedback">

> अपना feedback share करें: [Workshop Survey Link]
> 
> Questions? GitHub Issues में पूछें या discussion start करें।

</div>

### 👥 Contributors

| Role | Name |
|------|------|
| Author | Olivier Mertens |
| Technical Review | Microsoft AI Team |
| Hindi Translation | AI-assisted with verification |

---

> 🌍 **[← भाग 3: प्रोडक्शन](./part3-production.hi.md)** | **[🏠 वर्कशॉप होम](./index.hi.md)**
