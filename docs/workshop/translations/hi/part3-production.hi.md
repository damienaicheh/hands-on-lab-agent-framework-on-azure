---
published: true
type: workshop
title: "भाग 3: प्रोडक्शन रेडीनेस"
short_title: "प्रोडक्शन"
description: ऑर्केस्ट्रेशन, ऑब्जर्वेबिलिटी और इवैल्यूएशन
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 90
tags: handoff, orchestration, opentelemetry, observability, evaluation, testing
banner_url: ../assets/banner.jpg
navigation_levels: 1
sections_title:
  - परिचय
  - 🏠 नेविगेशन
  - भाग 1-2 का कोड
  - मॉड्यूल अवलोकन
  - मॉड्यूल 6 - Orchestration
  - मॉड्यूल 7 - Observability
  - मॉड्यूल 8 - Evaluation
  - सारांश
---

# भाग 3: प्रोडक्शन रेडीनेस

![Workshop Banner](../assets/banner.jpg)

> 🌍 **[← भाग 2](./part2-knowledge.hi.md)** | **[🏠 होम](./index.hi.md)** | **[भाग 4 →](./part4-advanced.hi.md)**

---

## 🏠 नेविगेशन

<div class="tip" data-title="वर्कशॉप नेविगेशन">

> **📚 सभी भाग:**
> - [🏠 वर्कशॉप होम](./index.hi.md)
> - [भाग 1: बुनियादी बातें](./part1-basics.hi.md)
> - [भाग 2: नॉलेज इंटीग्रेशन](./part2-knowledge.hi.md)
> - [भाग 3: प्रोडक्शन रेडी](./part3-production.hi.md) *(वर्तमान)*
> - [भाग 4: एडवांस्ड और संसाधन](./part4-advanced.hi.md)
>
> **🌍 इस पेज को अन्य भाषाओं में:**
> - [🇬🇧 English](/workshop/part3-production.md)
> - [🇫🇷 Français](/workshop/translations/fr/part3-production.fr.md)
> - [🇪🇸 Español](/workshop/translations/es/part3-production.es.md)

</div>

---

## 📦 भाग 1 और 2 का कोड

<details>
<summary>📁 प्रोजेक्ट स्ट्रक्चर (क्लिक करें)</summary>

```text
helpdesk-agent/
├── src/
│   ├── module1_simple_agent.py      # Streaming के साथ बेसिक एजेंट
│   ├── module2_structured.py        # Pydantic Structured Output
│   ├── module3_tools.py             # Function Tools
│   ├── module4_ai_search.py         # RAG Integration
│   └── module5_group_chat.py        # MCP के साथ Multi-Agent
├── .env
└── requirements.txt
```

</details>

<details>
<summary>🔧 मुख्य कंपोनेंट्स (क्लिक करें)</summary>

```python
# RAG Search Tool (मॉड्यूल 4)
@function_tool
async def search_knowledge_base(query: str) -> str:
    """नॉलेज बेस में सर्च करें।"""
    search_client = SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
    )
    results = search_client.search(query, top=3)
    return "\n".join([doc["content"] for doc in results])

# MCP Client Setup (मॉड्यूल 5)
async with MCPServerStdio(
    params=StdioServerParameters(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", "./data"]
    )
) as mcp_server:
    tools = await mcp_server.list_tools()
```

</details>

<details>
<summary>🔐 Environment Variables (क्लिक करें)</summary>

```bash
# .env - पिछले भागों से आवश्यक वैल्यूज
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_KEY=xxx
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# भाग 2 में जोड़े गए
AZURE_SEARCH_ENDPOINT=https://xxx.search.windows.net
AZURE_SEARCH_KEY=xxx
AZURE_SEARCH_INDEX=helpdesk-index

# भाग 3 के लिए जोड़ें
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx
```

</details>

<div class="info" data-title="पिछले भाग पूरे नहीं किए?">

> पहले [भाग 1](./part1-basics.hi.md) और [भाग 2](./part2-knowledge.hi.md) पूरा करें सभी कंपोनेंट्स के लिए।

</div>

---

यह भाग enterprise production patterns को कवर करता है:

| मॉड्यूल | सामग्री |
|--------|---------|
| **मॉड्यूल 6** | Handoff के साथ ऑर्केस्ट्रेशन |
| **मॉड्यूल 7** | OpenTelemetry ऑब्जर्वेबिलिटी |
| **मॉड्यूल 8** | इवैल्यूएशन और टेस्टिंग |

---

## मॉड्यूल 6 — Handoff ऑर्केस्ट्रेशन

Agents के बीच intelligent routing और context transfer।

### 📚 कॉन्सेप्ट: Handoff Pattern

```
┌─────────────────────────────────────────────────────────┐
│                 Handoff Pattern                         │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  👤 User: "मेरा laptop धीमा है"                         │
│       ↓                                                 │
│  🎯 Triage Agent                                        │
│       │ "यह hardware issue लग रहा है"                   │
│       ↓                                                 │
│  🔄 HANDOFF (context transfer)                          │
│       │ - Conversation history                          │
│       │ - Extracted entities                            │
│       │ - Handoff reason                                │
│       ↓                                                 │
│  🔧 Hardware Agent                                      │
│       │ "आइए diagnose करते हैं..."                      │
│       ↓                                                 │
│  👤 User: Specialized response                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Handoff vs Direct Routing

| Direct Routing | Handoff |
|----------------|---------|
| Simple keyword matching | Context-aware decision |
| No history transfer | Full conversation context |
| Abrupt transitions | Smooth user experience |
| Static rules | Dynamic routing |

### 🧠 Pseudocode

```
ALGORITHM: Handoff Orchestration

1. TRIAGE AGENT परिभाषित करें:
   - Initial query analyze करें
   - Category identify करें
   - handoff_to() function call करें

2. SPECIALIST AGENTS परिभाषित करें:
   - NetworkAgent, HardwareAgent, etc.
   - प्रत्येक में विशेष instructions

3. HANDOFF TOOLS बनाएं:
   - @handoff decorator use करें
   - Target agent specify करें
   - Context automatically transfer

4. ORCHESTRATOR:
   - Handoff events manage करें
   - Conversation state maintain करें
   - User को seamless experience दें
```

### 🔨 एक्सरसाइज

`src/module6_handoff_orchestration.py` बनाएं।

<details>
<summary>💡 Hint: Handoff Tool परिभाषित करना</summary>

```python
from agent_framework import handoff

@handoff(target_agent="hardware_specialist")
def escalate_to_hardware(reason: str, context: dict) -> None:
    """Issue को hardware specialist को transfer करें।
    
    Args:
        reason: Transfer करने का कारण
        context: Relevant context information
    """
    pass  # Framework handles the actual handoff
```

</details>

<details>
<summary>💡 Hint: Triage Agent</summary>

```python
triage_agent = client.create_agent(
    name="TriageAgent",
    instructions="""आप IT support का first point of contact हैं।
    User की problem analyze करें और सही specialist को route करें।
    
    Categories:
    - NETWORK: VPN, WiFi, connectivity
    - HARDWARE: Laptop, peripherals, physical
    - SOFTWARE: Applications, OS, updates
    
    Appropriate handoff tool use करें।""",
    tools=[
        escalate_to_network,
        escalate_to_hardware,
        escalate_to_software,
    ],
)
```

</details>

<details>
<summary>💡 Hint: Orchestrator Setup</summary>

```python
from agent_framework import HandoffOrchestrator

orchestrator = HandoffOrchestrator(
    triage_agent=triage_agent,
    specialist_agents={
        "network_specialist": network_agent,
        "hardware_specialist": hardware_agent,
        "software_specialist": software_agent,
    },
    max_handoffs=3,  # Infinite loops से बचने के लिए
)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 6</summary>

```python
"""Module 6: Handoff Orchestration।"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import handoff, HandoffOrchestrator
from agent_framework.azure_openai import AzureOpenAIChatClient


# Handoff tools परिभाषित करें
@handoff(target_agent="network_specialist")
def escalate_to_network(reason: str, symptoms: list[str]) -> None:
    """Network specialist को transfer करें।
    
    Args:
        reason: Transfer का कारण
        symptoms: Observed network symptoms
    """
    pass


@handoff(target_agent="hardware_specialist")
def escalate_to_hardware(reason: str, device_info: dict) -> None:
    """Hardware specialist को transfer करें।
    
    Args:
        reason: Transfer का कारण
        device_info: Affected device की जानकारी
    """
    pass


@handoff(target_agent="software_specialist")
def escalate_to_software(reason: str, application: str) -> None:
    """Software specialist को transfer करें।
    
    Args:
        reason: Transfer का कारण
        application: Problematic application का नाम
    """
    pass


@handoff(target_agent="triage")
def return_to_triage(reason: str) -> None:
    """अगर issue out of scope हो तो triage को वापस भेजें।
    
    Args:
        reason: Return करने का कारण
    """
    pass


async def main() -> None:
    """Handoff orchestration demonstrate करें।"""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Triage agent
    triage_agent = client.create_agent(
        name="TriageAgent",
        instructions="""आप IT support का initial contact हैं।
        
        PROCESS:
        1. User की problem ध्यान से सुनें
        2. Category identify करें:
           - NETWORK: VPN, WiFi, internet, connectivity issues
           - HARDWARE: Physical devices, laptops, peripherals
           - SOFTWARE: Applications, OS, installations, updates
        3. Appropriate escalation tool use करें
        4. User को बताएं कि specialist connect करे रहे हैं
        
        ALWAYS gather basic information before handoff:
        - Device type
        - When problem started
        - Any error messages""",
        tools=[escalate_to_network, escalate_to_hardware, escalate_to_software],
    )
    
    # Specialist agents
    network_agent = client.create_agent(
        name="NetworkSpecialist",
        instructions="""आप senior network engineer हैं।
        
        EXPERTISE:
        - VPN configuration और troubleshooting
        - WiFi connectivity issues
        - Network security
        - DNS और proxy settings
        
        Detailed diagnostic steps provide करें।
        अगर hardware issue लगे तो return_to_triage use करें।""",
        tools=[return_to_triage],
    )
    
    hardware_agent = client.create_agent(
        name="HardwareSpecialist",
        instructions="""आप hardware support technician हैं।
        
        EXPERTISE:
        - Laptop और desktop issues
        - Peripherals (keyboard, mouse, monitor)
        - Battery और power issues
        - Physical damage assessment
        
        Warranty और replacement options suggest करें जहां applicable।
        Software issue लगे तो return_to_triage use करें।""",
        tools=[return_to_triage],
    )
    
    software_agent = client.create_agent(
        name="SoftwareSpecialist",
        instructions="""आप software support expert हैं।
        
        EXPERTISE:
        - Application installation और configuration
        - OS updates और patches
        - License और activation issues
        - Performance optimization
        
        Step-by-step installation guides provide करें।
        Hardware issue लगे तो return_to_triage use करें।""",
        tools=[return_to_triage],
    )
    
    # Orchestrator setup
    orchestrator = HandoffOrchestrator(
        triage_agent=triage_agent,
        specialist_agents={
            "network_specialist": network_agent,
            "hardware_specialist": hardware_agent,
            "software_specialist": software_agent,
        },
        max_handoffs=3,
        handoff_message="🔄 आपको {agent_name} से connect कर रहे हैं...",
    )
    
    # Test conversation
    conversation = [
        "हेलो, मेरा laptop बहुत धीमा हो गया है",
        "हाँ, यह Dell Latitude है, करीब 2 साल पुराना",
        "Windows update के बाद से ऐसा हुआ है",
        "धन्यवाद, अभी try करता हूं",
    ]
    
    print("🎯 Handoff Orchestration Demo")
    print("=" * 60)
    
    for message in conversation:
        print(f"\n👤 User: {message}")
        result = await orchestrator.run(message)
        print(f"\n🤖 {result.current_agent}: {result.text}")
        
        if result.handoff_occurred:
            print(f"   📋 Handoff: {result.handoff_from} → {result.handoff_to}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module6_handoff_orchestration.py
```

---

## मॉड्यूल 7 — OpenTelemetry ऑब्जर्वेबिलिटी

Azure Application Insights के साथ comprehensive tracing।

### 📚 कॉन्सेप्ट: ऑब्जर्वेबिलिटी क्यों?

```
┌─────────────────────────────────────────────────────────┐
│             Observability Pillars                       │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   📊 TRACES          📈 METRICS         📝 LOGS         │
│   ─────────          ────────           ────            │
│   Request flow       Performance        Events          │
│   Dependencies       Resource usage     Errors          │
│   Latency            Token counts       Debug info      │
│                                                         │
│   ──────────────────────────────────────────────────    │
│                 Azure Application Insights              │
│   ──────────────────────────────────────────────────    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Production में क्या देखना है

| Signal | Use Case |
|--------|----------|
| **Traces** | Agent execution flow follow करें |
| **Tool calls** | कौन से tools, कितनी बार |
| **Token usage** | Cost monitoring |
| **Latency** | Response time optimization |
| **Errors** | Failure patterns identify करें |

### 🧠 Pseudocode

```
ALGORITHM: OpenTelemetry Integration

1. AZURE MONITOR EXPORTER कॉन्फ़िगर करें:
   - Connection string से
   - Traces + Metrics + Logs

2. AGENT FRAMEWORK में TRACING enable करें:
   - configure_tracing() call करें
   - Custom attributes add करें

3. CUSTOM SPANS बनाएं:
   - Business operations trace करें
   - Context propagation

4. APPLICATION INSIGHTS में VISUALIZE करें:
   - End-to-end transactions
   - Performance dashboards
```

### 🔨 एक्सरसाइज

`src/module7_observability.py` बनाएं।

<details>
<summary>💡 Hint: OpenTelemetry Setup</summary>

```python
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

# Azure Monitor configure करें
configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
    enable_live_metrics=True,
)

tracer = trace.get_tracer(__name__)
```

</details>

<details>
<summary>💡 Hint: Framework Tracing Enable</summary>

```python
from agent_framework.telemetry import configure_tracing

configure_tracing(
    service_name="helpdesk-agent",
    enable_token_tracking=True,
    enable_tool_call_tracking=True,
    custom_attributes={
        "environment": "production",
        "version": "1.0.0",
    },
)
```

</details>

<details>
<summary>💡 Hint: Custom Spans</summary>

```python
with tracer.start_as_current_span("process_support_ticket") as span:
    span.set_attribute("ticket.id", ticket_id)
    span.set_attribute("ticket.priority", priority)
    
    result = await agent.run(query)
    
    span.set_attribute("response.tokens", result.usage.total_tokens)
    span.set_attribute("tools.called", len(result.tool_calls))
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 7</summary>

```python
"""Module 7: OpenTelemetry Observability।"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace, metrics
from opentelemetry.trace import Status, StatusCode
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.telemetry import configure_tracing


# Azure Monitor configure करें
configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
    enable_live_metrics=True,
)

# Tracer और meter प्राप्त करें
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Custom metrics
request_counter = meter.create_counter(
    "helpdesk.requests.total",
    description="Total helpdesk requests",
)

response_time_histogram = meter.create_histogram(
    "helpdesk.response.duration",
    description="Response time in seconds",
    unit="s",
)


@ai_function
def search_knowledge_base(query: str) -> list[dict]:
    """Knowledge base में search करें।"""
    with tracer.start_as_current_span("kb_search") as span:
        span.set_attribute("search.query", query)
        
        # Simulated search
        results = [
            {"id": "KB001", "title": "VPN Setup", "score": 0.9},
        ]
        
        span.set_attribute("search.results_count", len(results))
        return results


async def process_request(agent, query: str, request_id: str) -> str:
    """Single request को trace के साथ process करें।"""
    
    with tracer.start_as_current_span("process_helpdesk_request") as span:
        span.set_attribute("request.id", request_id)
        span.set_attribute("request.query", query[:100])
        
        # Request counter increment करें
        request_counter.add(1, {"category": "support"})
        
        import time
        start_time = time.time()
        
        try:
            result = await agent.run(query)
            
            # Success attributes
            span.set_attribute("response.tokens.total", result.usage.total_tokens)
            span.set_attribute("response.tokens.prompt", result.usage.prompt_tokens)
            span.set_attribute("response.tokens.completion", result.usage.completion_tokens)
            span.set_attribute("response.tool_calls", len(result.tool_calls))
            span.set_status(Status(StatusCode.OK))
            
            # Response time record करें
            duration = time.time() - start_time
            response_time_histogram.record(duration, {"status": "success"})
            
            return result.text
            
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            span.record_exception(e)
            
            duration = time.time() - start_time
            response_time_histogram.record(duration, {"status": "error"})
            
            raise


async def main() -> None:
    """Observability features demonstrate करें।"""
    
    # Framework tracing configure करें
    configure_tracing(
        service_name="helpdesk-agent",
        enable_token_tracking=True,
        enable_tool_call_tracking=True,
        custom_attributes={
            "environment": os.getenv("ENVIRONMENT", "development"),
            "version": "1.0.0",
            "region": "eastus",
        },
    )
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="ObservableAgent",
        instructions="""आप helpdesk assistant हैं।
        User questions का जवाब देने के लिए knowledge base search करें।""",
        tools=[search_knowledge_base],
    )
    
    # Test requests
    requests = [
        ("REQ-001", "मैं VPN कैसे configure करूं?"),
        ("REQ-002", "मेरा password reset नहीं हो रहा"),
        ("REQ-003", "नया laptop का setup कैसे करें?"),
    ]
    
    print("🔭 Observability Demo")
    print("=" * 60)
    print("📊 Traces Application Insights में भेजे जा रहे हैं...")
    
    for request_id, query in requests:
        print(f"\n📨 Processing: {request_id}")
        try:
            response = await process_request(agent, query, request_id)
            print(f"✅ Response: {response[:100]}...")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("📈 Azure Portal में देखें:")
    print("   Application Insights → Transaction search")
    print("   Application Insights → Performance")
    print("   Application Insights → Live Metrics")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module7_observability.py
```

<div class="info" data-title="💡 Visualization">

> Azure Portal → Application Insights → **Transaction search** में traces देखें।
> **Live Metrics** real-time telemetry दिखाता है।

</div>

---

## मॉड्यूल 8 — इवैल्यूएशन और टेस्टिंग

Automated quality assessment agent responses का।

### 📚 कॉन्सेप्ट: Agent Evaluation

```
┌─────────────────────────────────────────────────────────┐
│              Evaluation Pipeline                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│   📋 Test Dataset         🧪 Evaluators                 │
│   ──────────────          ──────────                    │
│   - Questions             - Relevance                   │
│   - Expected context      - Groundedness               │
│   - Ground truth          - Coherence                   │
│                           - Fluency                     │
│         ↓                       ↓                       │
│   ┌──────────────────────────────────────┐              │
│   │           Agent Under Test            │              │
│   └──────────────────────────────────────┘              │
│                     ↓                                   │
│               📊 Metrics                                │
│               ──────────                                │
│               - Scores (1-5)                            │
│               - Pass/Fail rates                         │
│               - Comparison over time                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Evaluation Metrics

| Metric | क्या मापता है |
|--------|---------------|
| **Relevance** | Answer question से match करता है? |
| **Groundedness** | Sources पर आधारित है? |
| **Coherence** | Logically consistent है? |
| **Fluency** | Well-written है? |
| **Similarity** | Expected answer से कितना मिलता है? |

### 🧠 Pseudocode

```
ALGORITHM: Agent Evaluation

1. TEST DATASET लोड करें:
   - Questions
   - Expected answers
   - Context documents

2. EVALUATORS परिभाषित करें:
   - RelevanceEvaluator
   - GroundednessEvaluator
   - CoherenceEvaluator
   - SimilarityEvaluator

3. प्रत्येक test case के लिए:
   - Agent से response लें
   - प्रत्येक evaluator run करें
   - Scores collect करें

4. REPORT GENERATE करें:
   - Aggregate metrics
   - Pass/fail analysis
   - Recommendations
```

### 🔨 एक्सरसाइज

`src/module8_evaluation.py` बनाएं।

<details>
<summary>💡 Hint: Test Dataset</summary>

```python
test_cases = [
    {
        "question": "VPN कैसे configure करें?",
        "expected_context": "VPN setup requires...",
        "ground_truth": "Settings > Network > VPN से configure करें...",
    },
    {
        "question": "Password कैसे reset करें?",
        "expected_context": "Password reset policy...",
        "ground_truth": "IT portal पर जाएं और forgot password click करें...",
    },
]
```

</details>

<details>
<summary>💡 Hint: Evaluators Setup</summary>

```python
from agent_framework.evaluation import (
    RelevanceEvaluator,
    GroundednessEvaluator,
    CoherenceEvaluator,
    SimilarityEvaluator,
)

evaluators = [
    RelevanceEvaluator(model_config=model_config),
    GroundednessEvaluator(model_config=model_config),
    CoherenceEvaluator(model_config=model_config),
    SimilarityEvaluator(),
]
```

</details>

<details>
<summary>💡 Hint: Evaluation Run</summary>

```python
from agent_framework.evaluation import evaluate

results = await evaluate(
    agent=agent,
    test_cases=test_cases,
    evaluators=evaluators,
    output_path="evaluation_results.json",
)
```

</details>

### ✅ समाधान

<details>
<summary>📄 पूरा कोड मॉड्यूल 8</summary>

```python
"""Module 8: Agent Evaluation।"""
import asyncio
import json
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.evaluation import (
    RelevanceEvaluator,
    GroundednessEvaluator,
    CoherenceEvaluator,
    SimilarityEvaluator,
    evaluate,
    EvaluationReport,
)


# Test dataset
TEST_CASES = [
    {
        "question": "मैं VPN कैसे configure करूं?",
        "expected_context": "VPN configuration के लिए Settings में जाना होगा",
        "ground_truth": """VPN configure करने के लिए:
        1. Settings > Network > VPN पर जाएं
        2. Add VPN connection click करें
        3. Company credentials enter करें
        4. Connect button press करें""",
    },
    {
        "question": "Password reset कैसे करें?",
        "expected_context": "Password reset IT portal से होता है",
        "ground_truth": """Password reset के लिए:
        1. IT portal (it.company.com) पर जाएं
        2. Forgot Password click करें
        3. Employee ID enter करें
        4. Email में link आएगा""",
    },
    {
        "question": "नया software कैसे install करें?",
        "expected_context": "Software installation Software Center से",
        "ground_truth": """Software install करने के लिए:
        1. Software Center खोलें
        2. Available software browse करें
        3. Required software select करें
        4. Install click करें""",
    },
]


@ai_function
def search_knowledge_base(query: str) -> list[dict]:
    """Knowledge base search simulation।"""
    # Simulated responses
    kb_responses = {
        "vpn": "VPN configuration Settings > Network > VPN में है...",
        "password": "Password reset IT portal से होता है...",
        "software": "Software Center से install करें...",
    }
    
    for key, response in kb_responses.items():
        if key in query.lower():
            return [{"content": response, "source": "KB"}]
    
    return []


async def main() -> None:
    """Agent evaluation demonstrate करें।"""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Agent under test
    agent = client.create_agent(
        name="HelpdeskAgent",
        instructions="""आप IT helpdesk assistant हैं।
        Knowledge base search करके accurate answers दें।
        Sources cite करें।""",
        tools=[search_knowledge_base],
    )
    
    # Model config for evaluators
    model_config = {
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "deployment_name": "gpt-4o",
        "credential": DefaultAzureCredential(),
    }
    
    # Evaluators setup
    evaluators = [
        RelevanceEvaluator(model_config=model_config),
        GroundednessEvaluator(model_config=model_config),
        CoherenceEvaluator(model_config=model_config),
        SimilarityEvaluator(),
    ]
    
    print("🧪 Agent Evaluation Starting...")
    print("=" * 60)
    
    # Run evaluation
    results = await evaluate(
        agent=agent,
        test_cases=TEST_CASES,
        evaluators=evaluators,
        parallel=True,
    )
    
    # Print results
    print("\n📊 Evaluation Results")
    print("-" * 60)
    
    for i, case_result in enumerate(results.case_results):
        print(f"\n📋 Test Case {i + 1}: {TEST_CASES[i]['question'][:40]}...")
        print(f"   Response: {case_result.response[:80]}...")
        print(f"   Scores:")
        for metric, score in case_result.scores.items():
            status = "✅" if score >= 4 else "⚠️" if score >= 3 else "❌"
            print(f"      {status} {metric}: {score:.2f}/5")
    
    # Summary
    print("\n" + "=" * 60)
    print("📈 Summary")
    print("-" * 60)
    
    for metric, avg_score in results.aggregate_scores.items():
        status = "✅" if avg_score >= 4 else "⚠️" if avg_score >= 3 else "❌"
        print(f"   {status} {metric}: {avg_score:.2f}/5")
    
    print(f"\n   Pass Rate: {results.pass_rate:.1%}")
    print(f"   Total Tests: {results.total_cases}")
    print(f"   Passed: {results.passed_cases}")
    print(f"   Failed: {results.failed_cases}")
    
    # Save results
    with open("evaluation_results.json", "w") as f:
        json.dump(results.to_dict(), f, indent=2)
    
    print("\n💾 Results saved to evaluation_results.json")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module8_evaluation.py
```

### 📊 CI/CD Integration

<details>
<summary>💡 GitHub Actions Example</summary>

```yaml
name: Agent Evaluation

on:
  pull_request:
    paths:
      - 'src/**'
      - 'prompts/**'

jobs:
  evaluate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run evaluation
        env:
          AZURE_OPENAI_ENDPOINT: ${{ secrets.AZURE_OPENAI_ENDPOINT }}
        run: python src/module8_evaluation.py
      
      - name: Check quality gates
        run: |
          python -c "
          import json
          with open('evaluation_results.json') as f:
              results = json.load(f)
          if results['pass_rate'] < 0.8:
              raise Exception(f'Pass rate {results[\"pass_rate\"]} below threshold 0.8')
          "
```

</details>

<div class="task" data-title="🎯 Challenge">

> Custom evaluator बनाएं जो response में Hindi language quality check करे।

</div>

---

> 🌍 **[← भाग 2: नॉलेज](./part2-knowledge.hi.md)** | **[🏠 होम](./index.hi.md)** | **[भाग 4: एडवांस्ड →](./part4-advanced.hi.md)**
