---
published: true
type: workshop
title: "Parte 3: Listo para Producción"
short_title: "Producción"
description: Orquestación avanzada, observabilidad y evaluación
level: advanced
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 65
tags: orquestación, handoff, opentelemetry, evaluación, producción
banner_url: ../../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - Introducción
  - Código de las Partes 1-2
  - Módulo 6 - Orquestación
  - Módulo 7 - Observabilidad
  - Módulo 8 - Evaluación
  - Resumen
---

# Parte 3: Listo para Producción

![Banner del Taller](../../../assets/banner.jpg)

> 🌍 **[← Parte 2: Conocimiento](./part2-knowledge.es.md)** | **[Parte 4 →](./part4-advanced.es.md)**

## 📦 Código de las Partes 1 y 2

<details>
<summary>📁 Estructura del Proyecto (clic para expandir)</summary>

```text
helpdesk-agent/
├── src/
│   ├── module1_simple_agent.py      # Agente básico con streaming
│   ├── module2_structured.py        # Salida estructurada Pydantic
│   ├── module3_tools.py             # Herramientas de función
│   ├── module4_ai_search.py         # Integración RAG
│   └── module5_group_chat.py        # Multi-agente con MCP
├── .env
└── requirements.txt
```

</details>

<details>
<summary>🔧 Componentes Clave (clic para expandir)</summary>

```python
# Herramienta RAG de búsqueda (módulo 4)
@function_tool
async def search_knowledge_base(query: str) -> str:
    """Busca en la base de conocimiento."""
    search_client = SearchClient(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        index_name=os.getenv("AZURE_SEARCH_INDEX"),
        credential=AzureKeyCredential(os.getenv("AZURE_SEARCH_KEY"))
    )
    results = search_client.search(query, top=3)
    return "\n".join([doc["content"] for doc in results])

# Configuración cliente MCP (módulo 5)
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
<summary>🔐 Variables de Entorno (clic para expandir)</summary>

```bash
# .env - Valores requeridos de las partes anteriores
AZURE_OPENAI_ENDPOINT=https://xxx.openai.azure.com/
AZURE_OPENAI_KEY=xxx
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Añadido en la Parte 2
AZURE_SEARCH_ENDPOINT=https://xxx.search.windows.net
AZURE_SEARCH_KEY=xxx
AZURE_SEARCH_INDEX=helpdesk-index

# Añadir para la Parte 3
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx
```

</details>

<div class="info" data-title="¿No completaste las partes anteriores?">

> Completa [Parte 1](./part1-basics.es.md) y [Parte 2](./part2-knowledge.es.md) primero para tener todos los componentes.

</div>

---

Esta parte cubre funcionalidades para producción:

| Sección | Contenido |
|---------|-----------|
| **Módulo 6** | Orquestación Handoff |
| **Módulo 7** | Observabilidad OpenTelemetry |
| **Módulo 8** | Evaluación y Pruebas |

---

## Módulo 6 — Orquestación Handoff

Implementa transferencias inteligentes entre agentes especializados.

### 📚 Concepto: Patrón Handoff

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO HANDOFF                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Usuario: "Tengo un problema con la VPN y necesito         │
│            crear un ticket"                                 │
│                    │                                        │
│                    ▼                                        │
│           ┌───────────────┐                                │
│           │ 🎯 Orquestador │                                │
│           │   (Triaje)     │                                │
│           └───────┬───────┘                                │
│                   │ Analiza → "Problema técnico + ticket"  │
│                   │                                        │
│      ┌────────────┴────────────┐                          │
│      ▼                         ▼                          │
│ ┌─────────────┐         ┌─────────────┐                   │
│ │ 🔧 Técnico  │ ──────▶ │ 📝 Tickets  │                   │
│ │  Specialist │ handoff │  Specialist │                   │
│ └─────────────┘         └─────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Componente | Rol |
|------------|-----|
| **Orquestador** | Triaje inicial, decide workflow |
| **Especialista Técnico** | Resuelve problemas técnicos |
| **Especialista Tickets** | Crea y gestiona tickets |
| **Handoff** | Transferencia controlada |

### 🧠 Pseudocódigo

```
ALGORITMO: Workflow Handoff

1. CREAR AGENTES ESPECIALISTAS:
   - tech_specialist → problemas técnicos
   - ticket_specialist → gestión tickets

2. CREAR ORQUESTADOR con HandoffBuilder:
   - Añadir especialistas disponibles
   - Definir instrucciones de triaje

3. HANDOFF CONDICIONAL:
   - Orquestador analiza solicitud
   - Decide especialista apropiado
   - Transfiere con contexto

4. FINALIZACIÓN:
   - Especialista completa tarea
   - Retorna al orquestador si necesario
```

### 🔨 Ejercicio

Crea `src/module6_orchestration.py`.

<details>
<summary>💡 Hint: Crear Especialistas</summary>

```python
tech_specialist = client.create_agent(
    name="TechSpecialist",
    instructions="""Eres un experto técnico de TI.
    Resuelves problemas de hardware, software, red y seguridad.
    Proporciona pasos claros de solución.""",
    tools=[search_knowledge_base, run_diagnostics],
)

ticket_specialist = client.create_agent(
    name="TicketSpecialist",
    instructions="""Eres un experto en gestión de tickets.
    Creas, actualizas y das seguimiento a tickets de soporte.""",
    tools=[create_ticket, update_ticket, get_ticket_status],
)
```

</details>

<details>
<summary>💡 Hint: Configurar Handoff</summary>

```python
from agent_framework.workflows import HandoffBuilder

orchestrator = (
    HandoffBuilder()
    .with_orchestrator(
        name="Orchestrator",
        instructions="""Eres el orquestador del helpdesk.
        Analiza cada solicitud y decide el especialista apropiado:
        - Problemas técnicos → TechSpecialist
        - Crear/gestionar tickets → TicketSpecialist
        """
    )
    .add_specialist(tech_specialist)
    .add_specialist(ticket_specialist)
    .build()
)
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 6</summary>

```python
"""Módulo 6: Orquestación Avanzada - Workflow Handoff."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.workflows import HandoffBuilder


# Herramientas para especialistas
@ai_function
def search_knowledge_base(query: str) -> list[dict]:
    """Busca soluciones en la base de conocimiento."""
    return [
        {"title": "Solución VPN", "content": "Reinicia el cliente VPN..."},
        {"title": "Resetear conexión", "content": "Flush DNS con ipconfig /flushdns..."},
    ]


@ai_function
def run_diagnostics(system: str) -> dict:
    """Ejecuta diagnósticos remotos."""
    return {
        "system": system,
        "status": "healthy",
        "checks": {"network": "ok", "disk": "ok", "memory": "ok"},
    }


@ai_function
def create_ticket(title: str, priority: str, description: str) -> dict:
    """Crea un nuevo ticket de soporte."""
    return {
        "ticket_id": "TK-2024-001",
        "title": title,
        "priority": priority,
        "status": "open",
    }


async def main() -> None:
    """Demuestra orquestación con Handoff."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Crear especialistas
    tech_specialist = client.create_agent(
        name="TechSpecialist",
        instructions="""Eres un experto técnico de TI.
        Diagnosticas y resuelves problemas técnicos.
        Usa las herramientas para buscar soluciones y ejecutar diagnósticos.""",
        tools=[search_knowledge_base, run_diagnostics],
    )
    
    ticket_specialist = client.create_agent(
        name="TicketSpecialist",
        instructions="""Eres un experto en gestión de tickets.
        Creas tickets con la información proporcionada.
        Asegúrate de incluir todos los detalles relevantes.""",
        tools=[create_ticket],
    )
    
    # Construir orquestador con Handoff
    orchestrator = (
        HandoffBuilder()
        .with_orchestrator(
            client=client,
            name="HelpdeskOrchestrator",
            instructions="""Eres el orquestador del helpdesk.
            
            ANALIZA cada solicitud y TRANSFIERE al especialista apropiado:
            - Problemas técnicos (VPN, red, software) → TechSpecialist
            - Crear o gestionar tickets → TicketSpecialist
            
            Puedes transferir a múltiples especialistas secuencialmente.
            Cuando todos los especialistas hayan terminado, resume el resultado.
            """,
        )
        .add_specialist(tech_specialist, "Problemas técnicos de TI")
        .add_specialist(ticket_specialist, "Gestión de tickets de soporte")
        .with_max_handoffs(3)
        .build()
    )
    
    # Escenarios de prueba
    escenarios = [
        "Mi VPN no conecta desde esta mañana, necesito ayuda urgente",
        "Crea un ticket para reportar que la impresora del piso 3 no funciona",
        "Tengo problemas de red y necesito que quede registrado en un ticket",
    ]
    
    for escenario in escenarios:
        print(f"\n{'='*60}")
        print(f"👤 Usuario: {escenario}")
        print("-" * 60)
        
        async for event in orchestrator.run_stream(escenario):
            if hasattr(event, 'handoff_to'):
                print(f"\n🔄 Handoff a: {event.handoff_to}")
            if hasattr(event, 'text'):
                print(event.text, end="", flush=True)
        
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module6_orchestration.py
```

---

## Módulo 7 — Observabilidad OpenTelemetry

Implementa trazabilidad completa con OpenTelemetry y Azure Monitor.

### 📚 Concepto: ¿Por qué Observabilidad?

```
┌─────────────────────────────────────────────────────────────┐
│                  STACK DE OBSERVABILIDAD                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  TRACES (Trazas)                                           │
│  ├── request_span                                          │
│  │   ├── orchestrator_span (200ms)                         │
│  │   │   └── llm_call_span (150ms)                         │
│  │   ├── tool_call_span (50ms)                             │
│  │   └── specialist_span (300ms)                           │
│                                                             │
│  MÉTRICAS                                                  │
│  • Latencia promedio: 450ms                                │
│  • Tokens consumidos: 1,234                                │
│  • Tasa de éxito: 98.5%                                    │
│                                                             │
│  LOGS                                                       │
│  • [INFO] Agente iniciado                                  │
│  • [DEBUG] Tool call: search_kb                            │
│  • [ERROR] Timeout en llamada LLM                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Señal | Propósito |
|-------|-----------|
| **Traces** | Seguir flujo de ejecución |
| **Métricas** | Medir rendimiento |
| **Logs** | Depurar problemas |

### 🧠 Pseudocódigo

```
ALGORITMO: Agente con Observabilidad

1. CONFIGURAR OPENTELEMETRY:
   - TracerProvider con Azure exporter
   - Instrumentar framework de agentes

2. CREAR SPANS PERSONALIZADOS:
   - Envolver operaciones críticas
   - Añadir atributos relevantes

3. ENVIAR A AZURE MONITOR:
   - Connection string de App Insights
   - Traces y métricas automáticos
```

### 🔨 Ejercicio

Crea `src/module7_observability.py`.

<details>
<summary>💡 Hint: Configurar OpenTelemetry</summary>

```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter

# Configurar proveedor de trazas
provider = TracerProvider()
exporter = AzureMonitorTraceExporter(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
)
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

tracer = trace.get_tracer(__name__)
```

</details>

<details>
<summary>💡 Hint: Spans Personalizados</summary>

```python
with tracer.start_as_current_span("process_request") as span:
    span.set_attribute("user_id", user_id)
    span.set_attribute("request_type", "helpdesk")
    
    with tracer.start_as_current_span("agent_run") as agent_span:
        result = await agent.run(query)
        agent_span.set_attribute("tokens_used", result.usage.total_tokens)
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 7</summary>

```python
"""Módulo 7: Observabilidad con OpenTelemetry."""
import asyncio
import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework import ai_function


def setup_telemetry() -> trace.Tracer:
    """Configura OpenTelemetry con Azure Monitor."""
    
    resource = Resource.create({
        "service.name": "helpdesk-agent",
        "service.version": "1.0.0",
        "deployment.environment": "development",
    })
    
    provider = TracerProvider(resource=resource)
    
    exporter = AzureMonitorTraceExporter(
        connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    )
    provider.add_span_processor(BatchSpanProcessor(exporter))
    
    trace.set_tracer_provider(provider)
    
    return trace.get_tracer(__name__)


@ai_function
def get_system_status(system_name: str) -> dict:
    """Obtiene el estado de un sistema."""
    return {"system": system_name, "status": "healthy", "uptime": "99.9%"}


async def main() -> None:
    """Demuestra observabilidad con trazas."""
    
    tracer = setup_telemetry()
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="ObservableAgent",
        instructions="Eres un asistente de TI con observabilidad.",
        tools=[get_system_status],
    )
    
    consultas = [
        "¿Cuál es el estado del servidor de correo?",
        "Verifica el sistema de autenticación",
    ]
    
    for consulta in consultas:
        # Crear span padre para toda la solicitud
        with tracer.start_as_current_span("helpdesk_request") as request_span:
            request_span.set_attribute("query", consulta)
            request_span.set_attribute("user_id", "user_123")
            
            print(f"\n👤 Usuario: {consulta}")
            
            # Span para ejecución del agente
            with tracer.start_as_current_span("agent_execution") as agent_span:
                result = await agent.run(consulta)
                
                agent_span.set_attribute("agent_name", "ObservableAgent")
                agent_span.set_attribute("response_length", len(result.text))
                
                if hasattr(result, 'usage'):
                    agent_span.set_attribute("tokens_prompt", result.usage.prompt_tokens)
                    agent_span.set_attribute("tokens_completion", result.usage.completion_tokens)
            
            print(f"🤖 Agente: {result.text}")
            request_span.set_attribute("status", "success")
    
    print("\n📊 Trazas enviadas a Azure Monitor")
    print("   Ver en: Portal Azure → Application Insights → Búsqueda de transacciones")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
pip install azure-monitor-opentelemetry-exporter
python src/module7_observability.py
```

---

## Módulo 8 — Evaluación y Pruebas

Implementa un pipeline de evaluación para medir la calidad de tu agente.

### 📚 Concepto: ¿Por qué Evaluar?

| Sin Evaluación | Con Evaluación |
|----------------|----------------|
| "Parece que funciona bien" | "Precisión: 94.2%" |
| Cambios rompen funcionalidad | Regresiones detectadas |
| Calidad subjetiva | Métricas objetivas |

```
┌─────────────────────────────────────────────────────────────┐
│                   PIPELINE EVALUACIÓN                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. DATASET          2. EJECUCIÓN        3. MÉTRICAS        │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Preguntas   │───▶│   Agente    │───▶│ Comparar    │     │
│  │ Esperado    │    │   Responde  │    │ Evaluar     │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                              │              │
│                                              ▼              │
│                                        ┌─────────────┐     │
│                                        │ • Precisión │     │
│                                        │ • Relevancia│     │
│                                        │ • Coherencia│     │
│                                        └─────────────┘     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 🧠 Pseudocódigo

```
ALGORITMO: Evaluación de Agente

1. CREAR DATASET DE PRUEBAS:
   - Lista de (pregunta, respuesta_esperada)
   - Cubrir casos normales y edge cases

2. EJECUTAR AGENTE EN DATASET:
   - Para cada pregunta, obtener respuesta
   - Guardar resultado

3. EVALUAR CON MÉTRICAS:
   - Relevancia: ¿responde a la pregunta?
   - Coherencia: ¿es lógica la respuesta?
   - Fundamentación: ¿usa fuentes correctas?

4. GENERAR REPORTE:
   - Puntuaciones por métrica
   - Ejemplos de fallos
```

### 🔨 Ejercicio

Crea `src/module8_evaluation.py`.

<details>
<summary>💡 Hint: Dataset de Pruebas</summary>

```python
test_cases = [
    {
        "query": "¿Cómo reinicio mi contraseña?",
        "expected_topics": ["contraseña", "portal", "autoservicio"],
        "expected_type": "procedural",
    },
    {
        "query": "¿Cuál es la política de contraseñas?",
        "expected_topics": ["caracteres", "expiración", "complejidad"],
        "expected_type": "informational",
    },
]
```

</details>

<details>
<summary>💡 Hint: Función de Evaluación</summary>

```python
async def evaluate_response(
    query: str,
    response: str,
    expected_topics: list[str],
) -> dict:
    """Evalúa una respuesta del agente."""
    
    # Verificar cobertura de temas
    topics_found = sum(1 for t in expected_topics if t.lower() in response.lower())
    topic_coverage = topics_found / len(expected_topics)
    
    # Evaluar con LLM
    evaluator_prompt = f"""
    Evalúa esta respuesta del 1 al 5:
    Pregunta: {query}
    Respuesta: {response}
    
    Criterios:
    - Relevancia: ¿responde a la pregunta?
    - Claridad: ¿es fácil de entender?
    - Completitud: ¿cubre todos los aspectos?
    """
    
    return {
        "topic_coverage": topic_coverage,
        "relevance_score": ...,  # Del evaluador LLM
    }
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 8</summary>

```python
"""Módulo 8: Evaluación y Pruebas de Agentes."""
import asyncio
import os
from dataclasses import dataclass
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


@dataclass
class TestCase:
    """Caso de prueba para evaluación."""
    query: str
    expected_topics: list[str]
    category: str


@dataclass
class EvaluationResult:
    """Resultado de evaluación de un caso."""
    query: str
    response: str
    topic_coverage: float
    relevance_score: float
    passed: bool


# Dataset de pruebas
TEST_CASES = [
    TestCase(
        query="¿Cómo reinicio mi contraseña de correo?",
        expected_topics=["contraseña", "portal", "restablecer", "pasos"],
        category="password",
    ),
    TestCase(
        query="No puedo conectar a la VPN",
        expected_topics=["VPN", "conexión", "verificar", "credenciales"],
        category="network",
    ),
    TestCase(
        query="¿Cuál es el horario del soporte técnico?",
        expected_topics=["horario", "soporte", "disponible"],
        category="general",
    ),
]


async def evaluate_single(
    agent,
    evaluator_agent,
    test_case: TestCase,
) -> EvaluationResult:
    """Evalúa un solo caso de prueba."""
    
    # Obtener respuesta del agente
    result = await agent.run(test_case.query)
    response = result.text
    
    # Calcular cobertura de temas
    topics_found = sum(
        1 for topic in test_case.expected_topics
        if topic.lower() in response.lower()
    )
    topic_coverage = topics_found / len(test_case.expected_topics)
    
    # Evaluar relevancia con LLM
    eval_prompt = f"""
    Evalúa la relevancia de esta respuesta (0.0 a 1.0):
    
    Pregunta: {test_case.query}
    Respuesta: {response}
    
    Responde SOLO con un número entre 0.0 y 1.0.
    """
    
    eval_result = await evaluator_agent.run(eval_prompt)
    try:
        relevance_score = float(eval_result.text.strip())
    except ValueError:
        relevance_score = 0.5
    
    passed = topic_coverage >= 0.5 and relevance_score >= 0.6
    
    return EvaluationResult(
        query=test_case.query,
        response=response[:200] + "...",
        topic_coverage=topic_coverage,
        relevance_score=relevance_score,
        passed=passed,
    )


async def main() -> None:
    """Ejecuta pipeline de evaluación."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Agente a evaluar
    agent = client.create_agent(
        name="HelpdeskAgent",
        instructions="""Eres un asistente de TI.
        Proporciona respuestas útiles y detalladas.""",
    )
    
    # Agente evaluador
    evaluator = client.create_agent(
        name="Evaluator",
        instructions="Evalúa respuestas de IA. Responde solo con números.",
    )
    
    print("🧪 Iniciando evaluación...\n")
    print("=" * 60)
    
    results: list[EvaluationResult] = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n📋 Caso {i}/{len(TEST_CASES)}: {test_case.category}")
        print(f"   Pregunta: {test_case.query[:50]}...")
        
        result = await evaluate_single(agent, evaluator, test_case)
        results.append(result)
        
        status = "✅" if result.passed else "❌"
        print(f"   {status} Cobertura: {result.topic_coverage:.0%}, Relevancia: {result.relevance_score:.0%}")
    
    # Resumen
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE EVALUACIÓN")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.passed)
    total = len(results)
    avg_coverage = sum(r.topic_coverage for r in results) / total
    avg_relevance = sum(r.relevance_score for r in results) / total
    
    print(f"   Casos pasados: {passed}/{total} ({passed/total:.0%})")
    print(f"   Cobertura promedio: {avg_coverage:.0%}")
    print(f"   Relevancia promedio: {avg_relevance:.0%}")
    
    if passed == total:
        print("\n🎉 ¡Todos los casos pasaron!")
    else:
        print("\n⚠️ Algunos casos fallaron. Revisa las respuestas.")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module8_evaluation.py
```

<div class="task" data-title="🎯 Desafío">

> Añade métricas adicionales: tiempo de respuesta, tokens usados, y genera un reporte JSON.

</div>

---

> 🌍 **[← Parte 2: Conocimiento](./part2-knowledge.es.md)** | **[Parte 4: Avanzado y Recursos →](./part4-advanced.es.md)**
