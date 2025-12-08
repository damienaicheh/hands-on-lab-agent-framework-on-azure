---
published: true
type: workshop
title: "Parte 1: Los Fundamentos"
short_title: "Los Fundamentos"
description: Requisitos, despliegue de infraestructura y primeros agentes
level: beginner
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 70
tags: requisitos, terraform, agente-simple, salida-estructurada, herramientas
banner_url: ../assets/banner.jpg
navigation_levels: 1
sections_title:
  - Introducción
  - 🏠 Navegación
  - Requisitos Previos
  - Despliegue de Infraestructura
  - Módulo 1 - Agente Simple
  - Módulo 2 - Salida Estructurada
  - Módulo 3 - Herramientas
  - Parte 1 Completa
---

# Parte 1: Los Fundamentos

![Workshop Banner](../assets/banner.jpg)

> 🌍 **[🏠 Inicio del Taller](./index.es.md)** | **[Parte 2 →](./part2-knowledge.es.md)**

---

## 🏠 Navegación

<div class="tip" data-title="Navegación del Taller">

> **📚 Todas las partes:**
> - [🏠 Inicio del Taller](./index.es.md)
> - [Parte 1: Los Fundamentos](./part1-basics.es.md) *(actual)*
> - [Parte 2: Integración de Conocimiento](./part2-knowledge.es.md)
> - [Parte 3: Listo para Producción](./part3-production.es.md)
> - [Parte 4: Avanzado y Recursos](./part4-advanced.es.md)
>
> **🌍 Esta página en otros idiomas:**
> - [🇬🇧 English](/workshop/part1-basics.md)
> - [🇫🇷 Français](/workshop/translations/fr/part1-basics.fr.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part1-basics.hi.md)

</div>

---


## Requisitos Previos

### 🛠️ Herramientas Requeridas

| Herramienta | Versión | Propósito |
|-------------|---------|-----------|
| [Python](https://www.python.org/downloads/){target="_blank"} | 3.11+ | Ejecución de código |
| [VS Code](https://code.visualstudio.com/){target="_blank"} | Última | IDE |
| [Azure CLI](https://docs.microsoft.com/cli/azure/install-azure-cli){target="_blank"} | 2.50+ | Gestión Azure |
| [Terraform](https://www.terraform.io/downloads){target="_blank"} | 1.5+ | Infraestructura como código |
| [Git](https://git-scm.com/){target="_blank"} | Última | Control de versiones |

### ☁️ Cuentas Requeridas

| Cuenta | Detalles |
|--------|----------|
| **Azure** | Suscripción activa con rol Contributor |
| **GitHub** | Para el servidor MCP de GitHub |

### 📦 Extensiones VS Code Recomendadas

```bash
code --install-extension ms-python.python
code --install-extension hashicorp.terraform
code --install-extension github.copilot
```

<div class="task" data-title="✅ Verificación">

> Ejecuta esto para verificar tu configuración:
> ```bash
> python --version && az --version && terraform --version
> ```

</div>

---

## Desplegar Infraestructura

### 🏗️ Arquitectura a Desplegar

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    📦 GRUPO DE RECURSOS                            │
│                                                                     │
│  ┌───────────────┐ ┌─────────────┐ ┌──────────────┐ ┌────────────┐  │
│  │🧠 Azure AI    │ │🔍 AI Search │ │💾 Managed    │ │📊 App      │  │
│  │   Foundry    │ │             │ │   Redis      │ │ Insights   │  │
│  └───────────────┘ └─────────────┘ └──────────────┘ └────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 📁 Configurar el Proyecto

```bash
# Clonar el repositorio
git clone https://github.com/yourorg/hands-on-lab-agent-framework-on-azure.git
cd hands-on-lab-agent-framework-on-azure

# Crear entorno Python
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 🚀 Desplegar con Terraform

```bash
# Iniciar sesión en Azure
az login
az account set --subscription "<TU_SUSCRIPCION>"

# Desplegar infraestructura
cd infra
terraform init
terraform plan -out=tfplan
terraform apply tfplan
```

<details>
<summary>💡 Hint Copilot: Configuración .env</summary>

```
@workspace genera un archivo .env basado en los outputs de Terraform en /infra
```

</details>

### ⚙️ Configurar Variables de Entorno

Crea `.env` en la raíz:

```bash
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://<tu-recurso>.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://<tu-recurso>.search.windows.net
AZURE_SEARCH_INDEX_NAME=helpdesk-faq

# Redis
REDIS_CONNECTION_STRING=rediss://<tu-recurso>.redis.cache.windows.net:6380?password=<clave>

# Application Insights
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=...
```

<div class="warning" data-title="⚠️ Seguridad">

> Nunca subas `.env` a Git. Está en `.gitignore` por defecto.

</div>

---

## Módulo 1 — Agente Simple

Crea tu primer agente IA con streaming de respuestas.

### 📚 Concepto: ¿Qué es un Agente?

```
┌─────────────────────────────────────────────────┐
│                    AGENTE                       │
├─────────────────────────────────────────────────┤
│  📝 Instrucciones (System Prompt)               │
│  🧠 Modelo (GPT-4o)                             │
│  🔧 Herramientas (opcional)                     │
│  💾 Memoria (opcional)                          │
└─────────────────────────────────────────────────┘
         ↓
    Entrada Usuario → Razonamiento → Respuesta
```

### 🧠 Pseudocódigo

```
ALGORITMO: Agente Simple con Streaming

1. CONFIGURAR CLIENTE:
   - Usar DefaultAzureCredential
   - Conectar al endpoint Azure OpenAI

2. CREAR AGENTE:
   - Definir nombre y instrucciones
   - Especificar modelo (gpt-4o)

3. EJECUTAR CON STREAMING:
   - Enviar mensaje del usuario
   - Para cada chunk recibido:
     - Mostrar en tiempo real
```

### 🔨 Ejercicio

Crea `src/module1_simple_agent.py`.

<details>
<summary>💡 Hint: Configuración del Cliente</summary>

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
<summary>💡 Hint: Creación del Agente</summary>

```python
agent = client.create_agent(
    name="HelpdeskAssistant",
    instructions="Eres un asistente de TI. Sé conciso y útil.",
)
```

</details>

<details>
<summary>💡 Hint: Streaming</summary>

```python
async for chunk in agent.run_stream("¿Cómo reinicio mi contraseña?"):
    print(chunk.text, end="", flush=True)
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 1</summary>

```python
"""Módulo 1: Agente Simple con Streaming."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Crea y ejecuta un agente simple con streaming."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="HelpdeskAssistant",
        instructions="""Eres un asistente de TI amable y eficiente.
        Proporciona instrucciones claras paso a paso.
        Siempre pregunta aclaraciones si es necesario.""",
    )
    
    print("🤖 Agente Helpdesk iniciado!\n")
    
    pregunta = "¿Cómo puedo reiniciar mi contraseña de correo?"
    print(f"Usuario: {pregunta}\nAsistente: ", end="")
    
    async for chunk in agent.run_stream(pregunta):
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

## Módulo 2 — Salida Estructurada

Usa Pydantic para respuestas tipadas y validadas.

### 📚 Concepto: ¿Por qué Salida Estructurada?

| Sin Estructura | Con Pydantic |
|----------------|--------------|
| "Alta prioridad, urgente" | `{"priority": "high", "score": 9}` |
| Difícil de parsear | Tipado y validado |
| Inconsistente | Esquema garantizado |

### 🧠 Pseudocódigo

```
ALGORITMO: Analista de Complejidad

1. DEFINIR MODELO PYDANTIC:
   - TicketAnalysis con campos tipados
   - priority: Literal["low", "medium", "high"]
   - complexity_score: int (1-10)
   - summary: str

2. CREAR AGENTE CON response_format:
   - Pasar clase Pydantic
   - El framework fuerza el esquema JSON

3. EJECUTAR Y OBTENER OBJETO TIPADO:
   - result.data es instancia de TicketAnalysis
```

### 🔨 Ejercicio

Crea `src/module2_complexity_analyst.py`.

<details>
<summary>💡 Hint: Modelo Pydantic</summary>

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
<summary>💡 Hint: Agente con response_format</summary>

```python
agent = client.create_agent(
    name="ComplexityAnalyst",
    instructions="Analiza tickets de soporte...",
    response_format=TicketAnalysis,
)
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 2</summary>

```python
"""Módulo 2: Salida Estructurada con Pydantic."""
import asyncio
import os
from pydantic import BaseModel, Field
from typing import Literal
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


class TicketAnalysis(BaseModel):
    """Análisis estructurado de ticket de soporte."""
    priority: Literal["low", "medium", "high"]
    complexity_score: int = Field(ge=1, le=10, description="1=simple, 10=muy complejo")
    category: str = Field(description="Categoría del ticket")
    summary: str = Field(max_length=200)
    suggested_actions: list[str] = Field(max_items=5)
    estimated_time_minutes: int = Field(ge=5, le=480)


async def main() -> None:
    """Analiza un ticket y devuelve salida estructurada."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="ComplexityAnalyst",
        instructions="""Eres un analista experto de tickets de TI.
        Analiza cada ticket y proporciona un análisis estructurado.""",
        response_format=TicketAnalysis,
    )
    
    ticket = """
    Asunto: Pantalla azul recurrente
    Usuario: Departamento de Finanzas
    Descripción: Mi laptop muestra pantalla azul varias veces al día.
    Empezó después de la última actualización de Windows.
    Ya probé reiniciar pero el problema persiste.
    """
    
    print("📋 Analizando ticket...\n")
    result = await agent.run(f"Analiza este ticket:\n{ticket}")
    
    analysis: TicketAnalysis = result.data
    
    print(f"🎯 Prioridad: {analysis.priority.upper()}")
    print(f"📊 Complejidad: {analysis.complexity_score}/10")
    print(f"📁 Categoría: {analysis.category}")
    print(f"📝 Resumen: {analysis.summary}")
    print(f"⏱️ Tiempo estimado: {analysis.estimated_time_minutes} min")
    print("\n🔧 Acciones sugeridas:")
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

## Módulo 3 — Herramientas de Función

Añade capacidades personalizadas con el decorador `@ai_function`.

### 📚 Concepto: Tool Calling

```
Usuario: "Crea un ticket para el problema del VPN"
    ↓
Agente RAZONA → "Necesito crear ticket"
    ↓
Agente LLAMA → create_ticket(title="...", priority="high")
    ↓
Función EJECUTA → Retorna {"ticket_id": "TK-123"}
    ↓
Agente RESPONDE → "He creado el ticket TK-123"
```

### 🧠 Pseudocódigo

```
ALGORITMO: Agente con Herramientas

1. DEFINIR HERRAMIENTAS con @ai_function:
   - get_ticket_status(ticket_id) → estado
   - create_ticket(title, priority) → id
   - search_knowledge(query) → artículos

2. CREAR AGENTE con tools=[...]:
   - Lista de funciones decoradas

3. EL AGENTE DECIDE:
   - Cuándo llamar herramientas
   - Qué parámetros pasar
   - Cómo usar resultados
```

### 🔨 Ejercicio

Crea `src/module3_function_tools.py`.

<details>
<summary>💡 Hint: Definir Herramientas</summary>

```python
from agent_framework import ai_function

@ai_function
def get_ticket_status(ticket_id: str) -> dict:
    """Obtiene el estado de un ticket de soporte.
    
    Args:
        ticket_id: El ID del ticket (ej: TK-123)
    
    Returns:
        Información del estado del ticket
    """
    # Simulación
    return {
        "ticket_id": ticket_id,
        "status": "in_progress",
        "assignee": "tech_support",
    }
```

</details>

<details>
<summary>💡 Hint: Agente con Herramientas</summary>

```python
agent = client.create_agent(
    name="ToolsAgent",
    instructions="Usa las herramientas para ayudar...",
    tools=[get_ticket_status, create_ticket, search_kb],
)
```

</details>

### ✅ Solución

<details>
<summary>📄 Código Completo Módulo 3</summary>

```python
"""Módulo 3: Herramientas de Función."""
import asyncio
import os
from datetime import datetime
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient


# Almacén simulado de tickets
TICKETS_DB = {}
TICKET_COUNTER = 100


@ai_function
def get_ticket_status(ticket_id: str) -> dict:
    """Obtiene el estado actual de un ticket de soporte.
    
    Args:
        ticket_id: ID del ticket (ej: TK-101)
    
    Returns:
        Estado e información del ticket
    """
    if ticket_id in TICKETS_DB:
        return TICKETS_DB[ticket_id]
    return {"error": f"Ticket {ticket_id} no encontrado"}


@ai_function
def create_ticket(title: str, description: str, priority: str = "medium") -> dict:
    """Crea un nuevo ticket de soporte.
    
    Args:
        title: Título breve del problema
        description: Descripción detallada
        priority: low, medium, o high
    
    Returns:
        Información del ticket creado
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
    """Busca en la base de conocimiento de TI.
    
    Args:
        query: Términos de búsqueda
    
    Returns:
        Lista de artículos relevantes
    """
    # Base simulada
    kb = [
        {"id": "KB001", "title": "Reiniciar contraseña", "relevance": 0.9},
        {"id": "KB002", "title": "Configurar VPN", "relevance": 0.85},
        {"id": "KB003", "title": "Solucionar pantalla azul", "relevance": 0.8},
    ]
    return [a for a in kb if query.lower() in a["title"].lower()][:3]


async def main() -> None:
    """Demuestra un agente con herramientas de función."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="HelpdeskToolsAgent",
        instructions="""Eres un asistente de TI con acceso a herramientas.
        Usa las herramientas para crear tickets, buscar soluciones y verificar estados.""",
        tools=[get_ticket_status, create_ticket, search_knowledge_base],
    )
    
    consultas = [
        "Crea un ticket urgente: mi laptop no enciende después de una caída",
        "¿Cuál es el estado del ticket TK-101?",
        "Busca información sobre VPN en la base de conocimiento",
    ]
    
    for consulta in consultas:
        print(f"\n👤 Usuario: {consulta}")
        result = await agent.run(consulta)
        print(f"🤖 Agente: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module3_function_tools.py
```

<div class="task" data-title="🎯 Desafío">

> Añade una herramienta `update_ticket_status` que permita al agente cambiar el estado de un ticket.

</div>

---

> 🌍 **[🏠 Inicio del Taller](./index.es.md)** | **[Parte 2: Integración de Conocimiento →](./part2-knowledge.es.md)**
