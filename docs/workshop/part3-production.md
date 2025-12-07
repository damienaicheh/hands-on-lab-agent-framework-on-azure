---
published: true
type: workshop
title: "Part 3: Production Ready"
short_title: "Production Ready"
description: Build production-grade agent systems with orchestration, observability, and evaluation
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 60
tags: orchestration, observability, opentelemetry, evaluation, production, handoff
banner_url: ../assets/banner.jpg
navigation_levels: 1
sections_title:
  - Introduction
  - 🏠 Navigation
  - Code from Parts 1-2
  - Module 6 - Orchestration
  - Module 7 - Observability
  - Module 8 - Evaluation
  - Summary
---

# Part 3: Production Ready

![Workshop Banner](../assets/banner.jpg)

> 🌍 **[← Part 2: Knowledge Integration](/workshop/part2-knowledge.md)** | **[Part 4: Advanced & Resources →](/workshop/part4-advanced.md)**

---

## 🏠 Navigation

<div class="tip" data-title="Workshop Navigation">

> **📚 All Parts:**
> - [🏠 Workshop Home](/workshop/index.md)
> - [Part 1: Getting Started](/workshop/part1-basics.md)
> - [Part 2: Knowledge & Collaboration](/workshop/part2-knowledge.md)
> - [Part 3: Production Ready](/workshop/part3-production.md) *(current)*
> - [Part 4: Advanced & Resources](/workshop/part4-advanced.md)
>
> **🌍 This page in other languages:**
> - [🇫🇷 Français](/workshop/translations/fr/part3-production.fr.md)
> - [🇪🇸 Español](/workshop/translations/es/part3-production.es.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part3-production.hi.md)

</div>

---

## 📦 Code from Parts 1 & 2

Before starting this part, ensure you have the code from previous parts:

<details>
<summary>📁 Project Structure (click to expand)</summary>

```
helpdesk-agent/
├── .env
├── requirements.txt
└── src/
    ├── module1_simple_agent.py    # Part 1: Simple agent
    ├── module2_structured.py      # Part 1: Structured output
    ├── module3_tools.py           # Part 1: Function tools
    ├── module4_rag.py             # Part 2: AI Search RAG
    └── module5_group_chat.py      # Part 2: Group Chat + MCP
```

</details>

<details>
<summary>🔧 Key Components from Part 2 (click to expand)</summary>

```python
# RAG search tool from Module 4
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name="helpdesk-faq",
    credential=DefaultAzureCredential(),
)

@ai_function
def search_knowledge_base(query: str) -> list[dict]:
    """Search the FAQ knowledge base."""
    results = search_client.search(
        search_text=query,
        query_type="semantic",
        top=5,
    )
    return [{"title": r["title"], "content": r["content"]} for r in results]

# MCP client setup from Module 5
from agent_framework.mcp import MCPStdioClient, MCPTool

async def get_mcp_tools() -> list:
    """Get tools from MCP servers."""
    mslearn_client = await MCPStdioClient.create(
        command="npx",
        args=["-y", "@anthropic/mcp-mslearn"],
    )
    github_client = await MCPStdioClient.create(
        command="npx", 
        args=["-y", "@anthropic/mcp-github"],
        env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
    )
    return mslearn_client.tools + github_client.tools
```

</details>

<details>
<summary>📋 Environment Variables Needed (click to expand)</summary>

```bash
# .env file - ensure all these are set
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_SEARCH_ENDPOINT=https://your-search.search.windows.net
AZURE_SEARCH_INDEX_NAME=helpdesk-faq
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# New for Part 3:
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...
```

</details>

<div class="info" data-title="Haven't completed Parts 1-2?">

> Complete [Part 1](/workshop/part1-basics.md) and [Part 2](/workshop/part2-knowledge.md) first, or use the code snippets above to catch up.

</div>

---

| Module | Topic | What You'll Build |
|--------|-------|-------------------|
| 6 | **Orchestration** | Handoff workflow with specialists |
| 7 | **Observability** | OpenTelemetry tracing + Azure Monitor |
| 8 | **Evaluation** | Quality testing pipeline |

---

## Module 6 — Advanced Orchestration

Build a sophisticated orchestrator that coordinates multiple specialist agents.

### 📚 Concept: Handoff Pattern

Imagine calling a helpdesk: a **receptionist** (Orchestrator) answers, understands your problem, then **transfers** you to the right specialist.

```text
                                           ┌──────────────────┐
                                     ┌────▶│ ⚡ Quick Resolver │
                                     │     └──────────────────┘
                                     │
👤 User ───▶ 🎯 Orchestrator ───▶ 🔍 Analyst ──┼────▶ 📝 Ticket Creator
                                     │
                                     │     ┌──────────────────┐
                                     └────▶│ 🚨 Escalation    │
                                           └──────────────────┘
             
       request        analyze         route by complexity:
                                        • simple  → Quick Resolver
                                        • medium  → Ticket Creator
                                        • complex → Escalation
```

| Concept | Description |
|---------|-------------|
| **Coordinator** | The "boss" agent that routes requests |
| **Specialist** | Expert agents for specific task types |
| **Handoff** | Transfer of conversation between agents |
| **Return** | Specialist returns control to coordinator |

### 🧠 Pseudo-code

```
ALGORITHM: Helpdesk Orchestration

1. CREATE SPECIALISTS:
   - ComplexityAnalyst → determines difficulty
   - QuickResolver → handles simple issues
   - TicketCreator → creates formal tickets
   - EscalationAgent → escalates critical issues

2. CREATE ORCHESTRATOR as coordinator

3. CONFIGURE HANDOFF ROUTES:
   - Orchestrator → [Analyst]
   - Analyst → [Resolver, Creator, Escalation]
   - All specialists return to Orchestrator

4. PROCESS: User → Orchestrator → Analyst → Specialist → Response
```

### 🔨 Exercise: Build the Orchestrator

Create `src/module6_orchestration.py`.

<details>
<summary>💡 Hint: Specialist Agent Creation</summary>

```python
quick_resolver = ChatAgent(
    chat_client=client,
    name="QuickResolver",
    instructions="""Handle simple IT issues directly.
    Provide step-by-step solutions for:
    - Password resets
    - Browser cache clearing
    - Basic network troubleshooting""",
)
```

</details>

<details>
<summary>💡 Hint: HandoffBuilder Pattern</summary>

```python
workflow = (
    HandoffBuilder()
    .set_coordinator(orchestrator)
    .add_specialist(agents["analyst"])
    .add_specialist(agents["resolver"])
    .add_handoff(orchestrator, [agents["analyst"]])
    .add_handoff(agents["analyst"], [agents["resolver"], agents["creator"]])
    .enable_return_to_previous()
    .build()
)
```

</details>

<details>
<summary>💡 Hint: Streaming Events</summary>

```python
async for event in workflow.run_stream(ticket):
    if hasattr(event, 'text') and event.text:
        agent_name = getattr(event, 'agent_name', 'System')
        print(f"[{agent_name}]: {event.text}")
```

</details>

### ✅ Solution

<details>
<summary>📄 Complete Module 6 Code</summary>

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
        Output: Complexity (simple|medium|complex), Handler, Reasoning""",
    )
    
    quick_resolver = ChatAgent(
        chat_client=client,
        name="QuickResolver",
        instructions="""Handle simple IT issues directly.
        Provide step-by-step solutions for common problems.""",
    )
    
    ticket_creator = ChatAgent(
        chat_client=client,
        name="TicketCreator",
        instructions="""Create detailed support tickets.
        Format: Title, Priority, Category, Description""",
    )
    
    escalation_agent = ChatAgent(
        chat_client=client,
        name="EscalationAgent",
        instructions="""Handle complex escalations.
        Document info, identify team, create escalation report.""",
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
    
    orchestrator = ChatAgent(
        chat_client=client,
        name="Orchestrator",
        instructions="""You are the main helpdesk orchestrator.
        Route to ComplexityAnalyst first, then based on analysis:
        - Simple → QuickResolver
        - Medium → TicketCreator
        - Complex → EscalationAgent""",
    )
    
    workflow = (
        HandoffBuilder()
        .set_coordinator(orchestrator)
        .add_specialist(agents["analyst"])
        .add_specialist(agents["resolver"])
        .add_specialist(agents["creator"])
        .add_specialist(agents["escalation"])
        .add_handoff(orchestrator, [agents["analyst"]])
        .add_handoff(agents["analyst"], [
            agents["resolver"],
            agents["creator"],
            agents["escalation"]
        ])
        .enable_return_to_previous()
        .build()
    )
    
    tickets = [
        "I forgot my password and need to reset it",
        "The VPN keeps disconnecting every 5 minutes",
        "Entire department can't access CRM - client calls in 1 hour",
    ]
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n{'='*50}\nTicket {i}: {ticket}\n{'='*50}")
        async for event in workflow.run_stream(ticket):
            if hasattr(event, 'text') and event.text:
                agent_name = getattr(event, 'agent_name', 'System')
                print(f"[{agent_name}]: {event.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module6_orchestration.py
```

<div class="task" data-title="🎯 Challenge">

> Add a 5th specialist: `FeedbackAgent` that asks users to rate the support experience. Modify handoff routes so specialists can optionally handoff to FeedbackAgent.

</div>

---

## Module 7 — Observability

Enable tracing and monitoring with OpenTelemetry and Microsoft Foundry.

### 📚 Concept: Distributed Tracing

| Without Observability | With Observability |
|-----------------------|-------------------|
| "The agent is slow" | "Tool call took 3.2s at 14:32:05" |
| "The response was wrong" | "Model received 4500 tokens, no context" |
| Hours of log searching | Click to see exact trace |

**OpenTelemetry Concepts:**

| Term | Description |
|------|-------------|
| **Trace** | Complete journey of a request |
| **Span** | Single operation (nested hierarchy) |
| **Attributes** | Key-value metadata on spans |
| **Exporter** | Sends data to Azure Monitor |

### 🧠 Pseudo-code

```
ALGORITHM: Add Observability

1. CONFIGURE EXPORTER at startup:
   - configure_azure_monitor(connection_string)

2. SETUP FRAMEWORK OBSERVABILITY:
   - setup_observability(service_name, enable_tracing=True)

3. GET TRACER:
   - tracer = trace.get_tracer(__name__)

4. WRAP OPERATIONS IN SPANS:
   - with tracer.start_as_current_span("operation"):
   -     span.set_attribute("key", value)
   -     # Code automatically timed
```

### 🔨 Exercise: Add Tracing

Create `src/module7_observability.py`.

<details>
<summary>💡 Hint: Azure Monitor Setup</summary>

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
)
```

</details>

<details>
<summary>💡 Hint: Framework Observability</summary>

```python
from agent_framework.observability import setup_observability

setup_observability(
    service_name="helpdesk-agents",
    enable_tracing=True,
    enable_metrics=True,
)
```

</details>

<details>
<summary>💡 Hint: Creating Spans</summary>

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("helpdesk_session") as span:
    span.set_attribute("user.id", "demo_user")
    # Child spans automatically nested
    with tracer.start_as_current_span("agent_query") as query_span:
        query_span.set_attribute("query.text", query)
        result = await agent.run(query)
        query_span.set_attribute("response.length", len(result.text))
```

</details>

### ✅ Solution

<details>
<summary>📄 Complete Module 7 Code</summary>

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

# Configure BEFORE creating agents
configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
)

setup_observability(
    service_name="helpdesk-agents",
    enable_tracing=True,
    enable_metrics=True,
)

tracer = trace.get_tracer(__name__)


@ai_function
def check_system_status(system_name: str) -> dict:
    """Check the status of a system."""
    return {"system": system_name, "status": "operational"}


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
            instructions="You are a helpful assistant with monitoring.",
            tools=[check_system_status],
        )
        
        queries = ["Check email system", "Check VPN gateway"]
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

</details>

```bash
python src/module7_observability.py
```

**View traces in:**
- **Microsoft Foundry** → Your Project → Tracing
- **Application Insights** → Transaction Search

<div class="hint" data-title="Traces Not Appearing?">

> - Wait 2-3 minutes for ingestion delay
> - Verify `APPLICATIONINSIGHTS_CONNECTION_STRING` is correct
> - Ensure `configure_azure_monitor()` called BEFORE creating agents

</div>

<div class="task" data-title="🎯 Challenge">

> Add a custom metric to track token usage per query. Create an error boundary span that captures exceptions.

</div>

---

## Module 8 — Evaluation

Implement evaluation for agent quality and performance.

### 📚 Concept: Why Evaluate?

| Without Evaluation | With Evaluation |
|-------------------|-----------------|
| "The agent seems good" | "94% accuracy on classification" |
| "Users complain sometimes" | "15% failure rate on critical tickets" |
| Guessing at improvements | Data-driven prompt optimization |

**Evaluation Pipeline:**

```
TEST DATASET → AGENT → METRICS
  [inputs +     [run]    [accuracy,
   expected]              pass rate]
```

| Eval Type | Description | Use Case |
|-----------|-------------|----------|
| **Exact Match** | Output matches expected | Structured JSON |
| **LLM-as-Judge** | Model grades response | Open-ended text |
| **Human Eval** | People rate quality | Production validation |

### 🧠 Pseudo-code

```
ALGORITHM: Evaluate Agent Quality

1. DEFINE TEST DATASET:
   - input + expected_category + expected_severity

2. LOOP THROUGH TEST CASES:
   FOR each test_case:
       - Send input to agent
       - Parse JSON response
       - Compare to expected values
       - Record pass/fail

3. CALCULATE METRICS:
   - pass_rate = passed / total
   - category_accuracy = correct / total
   - severity_accuracy = correct / total

4. REPORT results and failing cases
```

### 🔨 Exercise: Build Evaluation

Create `src/module8_evaluation.py`.

<details>
<summary>💡 Hint: Test Dataset</summary>

```python
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
]
```

</details>

<details>
<summary>💡 Hint: Comparison Logic</summary>

```python
try:
    response = json.loads(result.text)
    category_match = response.get("category") == test_case["expected_category"]
    severity_match = response.get("severity") == test_case["expected_severity"]
    results.append({
        "category_correct": category_match,
        "severity_correct": severity_match,
        "overall_pass": category_match and severity_match,
    })
except json.JSONDecodeError:
    results.append({"error": "Invalid JSON", "overall_pass": False})
```

</details>

<details>
<summary>💡 Hint: Metrics Calculation</summary>

```python
total = len(results)
passed = sum(1 for r in results if r.get("overall_pass", False))
category_accuracy = sum(1 for r in results if r.get("category_correct", False)) / total
print(f"Pass Rate: {passed / total:.1%}")
print(f"Category Accuracy: {category_accuracy:.1%}")
```

</details>

### ✅ Solution

<details>
<summary>📄 Complete Module 8 Code</summary>

```python
"""Module 8: Evaluation - Testing agent quality."""
import asyncio
import os
import json
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


TEST_CASES = [
    {"input": "I can't log in to my email", "expected_category": "access", "expected_severity": "medium"},
    {"input": "URGENT: Production database is down!", "expected_category": "software", "expected_severity": "critical"},
    {"input": "How do I set up email forwarding?", "expected_category": "software", "expected_severity": "low"},
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
        {"category": "network|hardware|software|access|other",
         "severity": "low|medium|high|critical",
         "summary": "brief description"}""",
    )
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Running test {i}/{len(TEST_CASES)}...")
        result = await agent.run(f"Analyze: {test_case['input']}")
        
        try:
            response = json.loads(result.text)
            category_match = response.get("category") == test_case["expected_category"]
            severity_match = response.get("severity") == test_case["expected_severity"]
            results.append({
                "input": test_case["input"],
                "category_correct": category_match,
                "severity_correct": severity_match,
                "overall_pass": category_match and severity_match,
            })
        except json.JSONDecodeError:
            results.append({"input": test_case["input"], "error": "Invalid JSON", "overall_pass": False})
    
    total = len(results)
    passed = sum(1 for r in results if r.get("overall_pass", False))
    
    return {
        "total_tests": total,
        "passed": passed,
        "pass_rate": passed / total,
        "category_accuracy": sum(1 for r in results if r.get("category_correct", False)) / total,
        "severity_accuracy": sum(1 for r in results if r.get("severity_correct", False)) / total,
        "details": results,
    }


async def main() -> None:
    """Run evaluation and print results."""
    print("🧪 Running Agent Evaluation\n")
    metrics = await evaluate_agent()
    
    print(f"\n📊 Results")
    print(f"{'='*40}")
    print(f"Pass Rate: {metrics['pass_rate']:.1%}")
    print(f"Category Accuracy: {metrics['category_accuracy']:.1%}")
    print(f"Severity Accuracy: {metrics['severity_accuracy']:.1%}")
    
    print("\n📋 Details:")
    for r in metrics['details']:
        status = "✅" if r.get('overall_pass') else "❌"
        print(f"{status} {r['input'][:40]}...")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module8_evaluation.py
```

<div class="hint" data-title="Low Scores?">

> - **Low category accuracy**: Add examples in instructions
> - **Inconsistent JSON**: Use `response_format=YourModel`
> - **Debug failing tests**: Print raw response to see issues

</div>

<div class="task" data-title="🎯 Challenge">

> Add timing metrics to track response latency. Implement LLM-as-judge to evaluate response quality beyond exact match.

</div>

---

## Part 3 Summary

You've built **production-ready** agent systems:

| Module | Achievement |
|--------|-------------|
| **6** | ✅ Handoff orchestration with specialists |
| **7** | ✅ OpenTelemetry tracing + Azure Monitor |
| **8** | ✅ Quality evaluation pipeline |

**Key Patterns Learned:**

```
┌─────────────────────────────────────────────┐
│         PRODUCTION AGENT SYSTEM             │
├─────────────────────────────────────────────┤
│  📨 Request → 🎯 Orchestrator               │
│                    ↓                        │
│             [Route by complexity]           │
│                    ↓                        │
│  ⚡ Quick │ 📝 Ticket │ 🚨 Escalate          │
│                    ↓                        │
│  📊 Traces → Azure Monitor                  │
│  🧪 Eval → Quality Metrics                  │
└─────────────────────────────────────────────┘
```

> 🌍 **[← Part 2: Knowledge Integration](/workshop/part2-knowledge.md)** | **[Part 4: Advanced & Resources →](/workshop/part4-advanced.md)**
