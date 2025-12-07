---
published: true
type: workshop
title: "Parte 2: Integración de Conocimiento"
short_title: "Conocimiento"
description: RAG con Azure AI Search y workflows multi-agente
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 55
tags: rag, ai-search, group-chat, mcp, multi-agente
banner_url: ../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - Introducción
  - 🏠 Navegación
  - Código de la Parte 1
  - Módulo 4 - Azure AI Search
  - Módulo 5 - Group Chat
  - Parte 2 Completa
---

# Parte 2: Integración de Conocimiento

![Banner del Taller](../../assets/banner.jpg)

> 🌍 **[← Parte 1: Los Fundamentos](./part1-basics.es.md)** | **[Parte 3 →](./part3-production.es.md)**

---

## 🏠 Navegación

<div class="tip" data-title="Navegación del Taller">

> **📚 Todas las partes:**
> - [🏠 Inicio del Taller](./index.es.md)
> - [Parte 1: Los Fundamentos](./part1-basics.es.md)
> - [Parte 2: Integración de Conocimiento](./part2-knowledge.es.md) *(actual)*
> - [Parte 3: Listo para Producción](./part3-production.es.md)
> - [Parte 4: Avanzado y Recursos](./part4-advanced.es.md)
>
> **🌍 Esta página en otros idiomas:**
> - [🇬🇧 English](/workshop/part2-knowledge.md)
> - [🇫🇷 Français](/workshop/translations/fr/part2-knowledge.fr.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part2-knowledge.hi.md)

</div>

---

## 📦 Código de la Parte 1

<details>
<summary>📁 Estructura del Proyecto (clic para expandir)</summary>

```text
helpdesk-agent/
├── src/
│   ├── module1_simple_agent.py      # Agente básico con streaming
│   ├── module2_structured.py        # Salida estructurada Pydantic
│   └── module3_tools.py             # Herramientas de función
├── .env                             # Variables de entorno
└── requirements.txt                 # Dependencias
```

</details>

<details>
<summary>🔧 Componentes Clave (clic para expandir)</summary>

```python
# Configuración base del cliente (todos los módulos)
from agents import Agent, Runner
from openai import AsyncAzureOpenAI

client = AsyncAzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version="2024-10-21"
)

# Modelo Pydantic para salida estructurada (módulo 2)
class TicketExtraction(BaseModel):
    ticket_id: str
    customer_name: str
    issue_type: str
    priority: str
    summary: str

# Herramientas de función (módulo 3)
@function_tool
def get_ticket_status(ticket_id: str) -> str:
    """Obtiene el estado actual de un ticket."""
    # Lógica de búsqueda del ticket
    return f"Ticket {ticket_id}: En Progreso"
```

</details>

<div class="info" data-title="¿No completaste la Parte 1?">

> Completa [Parte 1: Los Fundamentos](./part1-basics.es.md) primero para tener la configuración base.

</div>

---

Esta parte cubre la integración de conocimiento:

| Sección | Contenido |
|---------|-----------|
| **Módulo 4** | RAG con Azure AI Search |
| **Módulo 5** | Group Chat Multi-Agente con MCP |

---

## Módulo 4 — Integración Azure AI Search

Conecta tu agente a una base de conocimiento empresarial.

### 📚 Concepto: RAG (Retrieval-Augmented Generation)

```
┌─────────────────────────────────────────────────────────────┐
│                     FLUJO RAG                               │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. CONSULTA        2. BÚSQUEDA         3. GENERACIÓN       │
│  ┌─────────┐       ┌─────────────┐      ┌─────────────┐    │
│  │ Usuario │──────▶│ AI Search   │─────▶│ LLM + Docs  │    │
│  │ Pregunta│       │ (Vectores)  │      │ = Respuesta │    │
│  └─────────┘       └─────────────┘      └─────────────┘    │
│                                                             │
│  "¿Cómo configuro    Busca docs        Genera respuesta     │
│   el VPN?"           relevantes        CON contexto         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

| Componente | Rol |
|------------|-----|
| **Azure AI Search** | Almacena e indexa documentos |
| **Embeddings** | Convierte texto a vectores |
| **Búsqueda Híbrida** | Keyword + Semántica |
| **LLM** | Genera respuesta con contexto |

### 🧠 Pseudocódigo

```
ALGORITMO: Agente con Conocimiento RAG

1. CONFIGURAR AI SEARCH:
   - Endpoint y nombre del índice
   - Credenciales Azure

2. CREAR BÚSQUEDA:
   - Función que consulta AI Search
   - Retorna documentos relevantes

3. INTEGRAR CON AGENTE:
   - Añadir como herramienta
   - O usar context_providers

4. FLUJO:
   - Usuario pregunta
   - Agente busca contexto
   - Genera respuesta fundamentada
```

### 🔨 Ejercicio

Crea `src/module4_knowledge_agent.py`.

<details>
<summary>💡 Hint: Cliente Azure AI Search</summary>

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
<summary>💡 Hint: Herramienta de Búsqueda</summary>

```python
@ai_function
def search_faq(query: str) -> list[dict]:
    """Busca en el FAQ empresarial.
    
    Args:
        query: La pregunta a buscar
    
    Returns:
        Lista de documentos relevantes
    """
    results = search_client.search(
        search_text=query,
        select=["title", "content", "category"],
        top=3,
    )
    return [dict(r) for r in results]
```

</details>

<details>
<summary>💡 Hint: Agente con Conocimiento</summary>

```python
agent = client.create_agent(
    name="KnowledgeAgent",
    instructions="""Eres un asistente de TI con acceso al FAQ.
    SIEMPRE busca en el FAQ antes de responder.
    Cita las fuentes en tus respuestas.""",
    tools=[search_faq],
)
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 4</summary>

```python
"""Módulo 4: Integración Azure AI Search - RAG."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient


# Cliente global de búsqueda
search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name=os.getenv("AZURE_SEARCH_INDEX_NAME"),
    credential=DefaultAzureCredential(),
)


@ai_function
def search_knowledge_base(query: str, top_k: int = 3) -> list[dict]:
    """Busca en la base de conocimiento empresarial.
    
    Args:
        query: La pregunta o términos de búsqueda
        top_k: Número máximo de resultados
    
    Returns:
        Lista de documentos relevantes con título, contenido y categoría
    """
    results = search_client.search(
        search_text=query,
        select=["title", "content", "category", "last_updated"],
        top=top_k,
        query_type="semantic",
        semantic_configuration_name="default",
    )
    
    documents = []
    for result in results:
        documents.append({
            "title": result["title"],
            "content": result["content"][:500],  # Limitar contenido
            "category": result.get("category", "General"),
            "relevance_score": result["@search.score"],
        })
    
    return documents


async def main() -> None:
    """Demuestra un agente con integración RAG."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="KnowledgeAgent",
        instructions="""Eres un asistente de TI con acceso al FAQ empresarial.
        
        REGLAS:
        1. SIEMPRE busca en la base de conocimiento antes de responder
        2. Basa tus respuestas en los documentos encontrados
        3. Si no encuentras información, indícalo claramente
        4. Cita las fuentes: [Fuente: título del documento]
        """,
        tools=[search_knowledge_base],
    )
    
    preguntas = [
        "¿Cómo configuro la VPN para trabajo remoto?",
        "¿Cuál es la política de contraseñas?",
        "Mi Outlook no sincroniza emails, ¿qué hago?",
    ]
    
    for pregunta in preguntas:
        print(f"\n{'='*60}")
        print(f"👤 Usuario: {pregunta}")
        print("-" * 60)
        
        result = await agent.run(pregunta)
        print(f"🤖 Agente:\n{result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module4_knowledge_agent.py
```

---

## Módulo 5 — Group Chat Multi-Agente con MCP

Orquesta múltiples agentes especializados con servidores MCP.

### 📚 Concepto: ¿Qué es MCP?

**Model Context Protocol (MCP)** es un protocolo abierto para conectar IA a fuentes de datos.

```
┌─────────────────────────────────────────────────────────────┐
│                    ARQUITECTURA MCP                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │ Learn Agent │     │GitHub Agent │     │ Más Agentes │   │
│  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘   │
│         │                   │                    │          │
│         ▼                   ▼                    ▼          │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐   │
│  │ MCP Server  │     │ MCP Server  │     │ MCP Server  │   │
│  │  MS Learn   │     │   GitHub    │     │   Otros     │   │
│  └─────────────┘     └─────────────┘     └─────────────┘   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

| Servidor MCP | Capacidades |
|--------------|-------------|
| **@anthropic/mcp-mslearn** | Buscar docs Microsoft Learn |
| **@anthropic/mcp-github** | Issues, PRs, repos |
| **@azure/azure-mcp** | Recursos Azure |

### 🧠 Pseudocódigo

```
ALGORITMO: Group Chat Multi-Agente

1. CONFIGURAR SERVIDORES MCP:
   - mslearn_server para documentación
   - github_server para issues

2. CREAR AGENTES ESPECIALIZADOS:
   - Learn Agent → usa mslearn_server
   - GitHub Agent → usa github_server

3. CREAR GROUP CHAT:
   - Añadir agentes con add_agents()
   - Configurar límite de turnos

4. EJECUTAR:
   - Orquestador decide quién responde
   - Agentes colaboran
   - Resultado combinado
```

### 🔨 Ejercicio

Crea `src/module5_group_chat.py`.

<details>
<summary>💡 Hint: Configurar MCP Servers</summary>

```python
from agent_framework.mcp import MCPServerStdio

mslearn_server = MCPServerStdio(
    name="mslearn",
    command="npx",
    args=["-y", "@anthropic/mcp-mslearn"],
)

github_server = MCPServerStdio(
    name="github",
    command="npx",
    args=["-y", "@anthropic/mcp-github"],
    env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
)
```

</details>

<details>
<summary>💡 Hint: Crear Agentes con MCP</summary>

```python
learn_agent = client.create_agent(
    name="LearnExpert",
    instructions="Busca documentación en Microsoft Learn.",
    mcp_servers=[mslearn_server],
)

github_agent = client.create_agent(
    name="GitHubExpert",
    instructions="Gestiona issues y busca código en GitHub.",
    mcp_servers=[github_server],
)
```

</details>

<details>
<summary>💡 Hint: Construir Group Chat</summary>

```python
from agent_framework.workflows import GroupChatBuilder

group_chat = (
    GroupChatBuilder()
    .add_agents(learn_agent, github_agent)
    .with_max_turns(5)
    .build()
)

result = await group_chat.run("¿Cómo implemento RAG en Azure?")
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 5</summary>

```python
"""Módulo 5: Group Chat Multi-Agente con MCP."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.mcp import MCPServerStdio
from agent_framework.workflows import GroupChatBuilder


async def main() -> None:
    """Demuestra Group Chat con servidores MCP."""
    
    # Configurar servidores MCP
    mslearn_server = MCPServerStdio(
        name="mslearn",
        command="npx",
        args=["-y", "@anthropic/mcp-mslearn"],
    )
    
    github_server = MCPServerStdio(
        name="github",
        command="npx",
        args=["-y", "@anthropic/mcp-github"],
        env={"GITHUB_TOKEN": os.getenv("GITHUB_TOKEN")},
    )
    
    # Cliente Azure OpenAI
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Crear agentes especializados
    learn_agent = client.create_agent(
        name="LearnExpert",
        instructions="""Eres un experto en documentación Microsoft.
        Busca información en Microsoft Learn para responder preguntas técnicas.
        Proporciona enlaces a la documentación relevante.""",
        mcp_servers=[mslearn_server],
    )
    
    github_agent = client.create_agent(
        name="GitHubExpert",
        instructions="""Eres un experto en gestión de repositorios GitHub.
        Puedes buscar código, crear issues y analizar repos.
        Proporciona ejemplos de código cuando sea útil.""",
        mcp_servers=[github_server],
    )
    
    orchestrator = client.create_agent(
        name="Orchestrator",
        instructions="""Eres el orquestador del equipo.
        Analiza las preguntas y decide qué experto debe responder.
        Combina las respuestas en una solución coherente.""",
    )
    
    # Construir Group Chat
    group_chat = (
        GroupChatBuilder()
        .with_orchestrator(orchestrator)
        .add_agents(learn_agent, github_agent)
        .with_max_turns(5)
        .with_termination_condition(
            lambda msgs: any("RESUELTO" in m.content for m in msgs[-2:])
        )
        .build()
    )
    
    # Ejecutar consulta
    consulta = """
    Necesito implementar un agente IA con Azure OpenAI.
    ¿Puedes buscar documentación y ejemplos de código?
    """
    
    print(f"👤 Usuario: {consulta}\n")
    print("=" * 60)
    print("🎯 Iniciando Group Chat...\n")
    
    async for event in group_chat.run_stream(consulta):
        if hasattr(event, 'agent_name'):
            print(f"\n🤖 {event.agent_name}:")
        if hasattr(event, 'text'):
            print(event.text, end="", flush=True)
    
    print("\n\n" + "=" * 60)
    print("✅ Group Chat completado")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
# Instalar dependencias MCP primero
npm install -g @anthropic/mcp-mslearn @anthropic/mcp-github

# Ejecutar
python src/module5_group_chat.py
```

<div class="task" data-title="🎯 Desafío">

> Añade un tercer agente "AzureExpert" que use el servidor MCP de Azure (`@azure/azure-mcp`) para consultar recursos.

</div>

---

> 🌍 **[← Parte 1: Los Fundamentos](./part1-basics.es.md)** | **[Parte 3: Listo para Producción →](./part3-production.es.md)**
