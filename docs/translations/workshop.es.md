---
published: true
type: workshop
title: Laboratorio Práctico - Agent Framework en Azure
short_title: Agent Framework en Azure
description: Construya un Asistente Helpdesk completo con Microsoft Agent Framework en Azure - desde un agente simple hasta orquestación multi-agentes con servidores MCP, AI Search y Redis.
level: intermediate
navigation_numbering: false
authors:
  - Olivier Mertens
  - Damien Aicheh
contacts:
  - "@olmertens"
  - "@damienaicheh"
duration_minutes: 300
tags: microsoft foundry, agent framework, ai search, managed redis, mcp, group chat, orquestación, observabilidad, evaluación
navigation_levels: 3
banner_url: ../assets/banner.jpg
audience: desarrolladores, arquitectos, ingenieros IA
sections_title:
  - Introducción
  - Prerrequisitos
  - Desplegar Infraestructura
  - Módulo 1 - Agente Simple
  - Módulo 2 - Analizador de Complejidad
  - Módulo 3 - Herramientas Funcionales
  - Módulo 4 - Integración de Conocimientos
  - Módulo 5 - Workflow Group Chat
  - Módulo 6 - Orquestación
  - Módulo 7 - Observabilidad
  - Módulo 8 - Evaluación
  - Módulo 9 - Integración Redis
  - Conclusión
---

# Asistente Helpdesk Ops - Agent Framework en Azure

¡Bienvenido a este laboratorio práctico! Construirás un **mini-helpdesk potenciado por agentes IA** que procesa tickets internos usando:

- 🔍 **Azure AI Search** para conocimientos FAQ de la empresa
- 🔧 **Servidores MCP** para gestión de tickets GitHub y documentación Microsoft Learn
- 🤖 **Orquestación multi-agentes** con Microsoft Agent Framework
- 📊 **Observabilidad** con OpenTelemetry y Azure AI Foundry

## 🎯 Escenario: Asistente Helpdesk Ops

Construirás un sistema helpdesk completo con varios agentes especializados:

| Agente | Rol | Herramientas/Integraciones |
|--------|-----|---------------------------|
| **Orquestador** | Enruta consultas, elige workflow (Solo vs Group Chat) | Control de workflow |
| **Analizador de Complejidad** | Analiza tickets, produce salida estructurada, sugiere estrategia | Herramientas funcionales |
| **Agente Learn** | Consulta documentación Microsoft Learn | Servidor MCP mslearn |
| **Agente GitHub** | Crea/gestiona issues GitHub, labels, comentarios | Servidor MCP github |

## 📚 Módulos del Laboratorio

| Módulo | Tema | Duración |
|--------|------|----------|
| 1 | Crear un Agente Simple | 20 min |
| 2 | Agente Analizador de Complejidad | 25 min |
| 3 | Herramientas Funcionales | 30 min |
| 4 | Integración de Conocimientos (Foundry IQ) | 30 min |
| 5 | Workflow Group Chat | 35 min |
| 6 | Orquestación Avanzada | 30 min |
| 7 | Observabilidad | 25 min |
| 8 | Evaluación | 30 min |
| 9 | Integración Redis | 25 min |

---

## Prerrequisitos

### 🖥️ Entorno de Desarrollo Local

Antes de comenzar este laboratorio, asegúrate de tener las siguientes herramientas instaladas en tu máquina:

#### Herramientas Requeridas

| Herramienta | Descripción | Enlace de Instalación |
|-------------|-------------|----------------------|
| **Azure CLI** | Interfaz de línea de comandos para Azure | [Instalar Azure CLI](https://learn.microsoft.com/es-es/cli/azure/install-azure-cli) |
| **Terraform** | Herramienta de Infraestructura como Código | [Instalar Terraform en Azure](https://learn.microsoft.com/es-es/azure/developer/terraform/quickstart-configure) |
| **Git** | Sistema de control de versiones | [Instalar Git](https://learn.microsoft.com/es-es/devops/develop/git/install-and-set-up-git) |
| **Visual Studio Code** | Editor de código | [Descargar VS Code](https://code.visualstudio.com/download) |
| **Python 3.11+** | Runtime de Python | [Descargar Python](https://www.python.org/downloads/) |

<div class="tip" data-title="Instalación Windows">

> Puedes instalar estas herramientas con `winget` en PowerShell:
> ```powershell
> winget install -e --id Microsoft.AzureCLI
> winget install -e --id Hashicorp.Terraform
> winget install -e --id Git.Git
> winget install -e --id Microsoft.VisualStudioCode
> winget install -e --id Python.Python.3.11
> ```

</div>

### 🧩 Extensiones de Visual Studio Code

Instala las siguientes extensiones en Visual Studio Code:

#### Extensiones Requeridas

| Extensión | ID | Propósito |
|-----------|-----|----------|
| **GitHub Copilot** | `GitHub.copilot` | Codificación asistida por IA |
| **GitHub Copilot Chat** | `GitHub.copilot-chat` | Chat IA interactivo |
| **HashiCorp Terraform** | `HashiCorp.terraform` | Sintaxis Terraform & IntelliSense |
| **Azure Account** | `ms-vscode.azure-account` | Integración de inicio de sesión Azure |
| **Azure Tools** | `ms-vscode.vscode-node-azure-pack` | Herramientas de desarrollo Azure |

#### Extensiones Recomendadas para Desarrollo IA

| Extensión | ID | Propósito |
|-----------|-----|----------|
| **AI Toolkit** | `ms-windows-ai-studio.windows-ai-studio` | Desarrollo y pruebas de modelos IA |
| **Azure MCP Server** | `ms-azuretools.azure-mcp` | Servidor Azure Model Context Protocol |
| **Azure Learn MCP** | `ms-azuretools.vscode-azure-github-copilot` | Documentación Azure y mejores prácticas |
| **Python** | `ms-python.python` | Soporte del lenguaje Python |
| **Jupyter** | `ms-toolsai.jupyter` | Soporte de notebooks Jupyter |
| **Pylance** | `ms-python.vscode-pylance` | IntelliSense Python |

<div class="hint" data-title="🤖 Maximiza Copilot para Este Laboratorio">

> **Configura Copilot para desarrollo Agent Framework:**
>
> 1. **Crea instrucciones de workspace** - Añade `.github/copilot-instructions.md`:
>    ```markdown
>    Este proyecto usa Microsoft Agent Framework para agentes IA.
>    - Usar Azure OpenAI con DefaultAzureCredential
>    - Usar patrones async/await para todas las operaciones de agente
>    - Usar Pydantic para salida estructurada
>    - Usar el decorador @ai_function para herramientas
>    - Seguir patrones OpenTelemetry para observabilidad
>    ```
>
> 2. **Usa el modo Copilot correcto para cada tarea**:
>    - **Ask**: Preguntas sobre conceptos de Agent Framework
>    - **Edit**: Modificar código de agente existente
>    - **Agent**: Construir nuevos agentes autónomamente
>    - **Plan**: Diseñar arquitecturas multi-agentes
>
> 3. **Usa servidores MCP**: Instala las extensiones Azure MCP y GitHub MCP para capacidades mejoradas

</div>

<div class="task" data-title="Instalar Extensiones">

> Instala las extensiones mediante línea de comandos:
> ```powershell
> # Extensiones Requeridas
> code --install-extension GitHub.copilot
> code --install-extension GitHub.copilot-chat
> code --install-extension HashiCorp.terraform
> code --install-extension ms-vscode.azure-account
> code --install-extension ms-vscode.vscode-node-azure-pack
> 
> # Extensiones IA Recomendadas
> code --install-extension ms-windows-ai-studio.windows-ai-studio
> code --install-extension ms-azuretools.azure-mcp
> code --install-extension ms-azuretools.vscode-azure-github-copilot
> code --install-extension ms-python.python
> code --install-extension ms-toolsai.jupyter
> code --install-extension ms-python.vscode-pylance
> ```

</div>

### 🐍 Configuración del Entorno Python

Crea y activa un entorno virtual Python:

```bash
# Crear entorno virtual
python -m venv .venv

# Activar (Windows)
.venv\Scripts\activate

# Activar (Linux/Mac)
source .venv/bin/activate

# Instalar Agent Framework con todos los extras
pip install agent-framework[azure,redis,viz] --pre
```

<div class="hint" data-title="¿Problemas con el Entorno Virtual?">

> **Problemas comunes y soluciones:**
>
> 1. **"python" no reconocido**: Usa `python3` en lugar de `python` en Linux/Mac
> 2. **La activación falla en Windows PowerShell**: Ejecuta primero `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
> 3. **pip install falla**: Prueba `python -m pip install --upgrade pip` y luego reintenta
> 4. **Versión Python incorrecta**: Verifica con `python --version` (necesita 3.11+)
>
> Para verificar que la activación funcionó, tu prompt de terminal debería mostrar el prefijo `(.venv)`.

</div>

<div class="hint" data-title="☁️ Usa Azure MCP para Verificar Variables de Entorno">

> **Pide a Copilot con Azure MCP que verifique tu configuración Azure:**
>
> 1. **Verificar conexión Azure CLI**:
>    ```
>    ¿En qué cuenta Azure estoy actualmente conectado?
>    Muestra el ID del tenant y nombre de la suscripción.
>    ```
>
> 2. **Verificar variables de entorno requeridas**:
>    ```
>    Verifica si AZURE_OPENAI_ENDPOINT y AZURE_AI_SEARCH_ENDPOINT 
>    están definidos en mi entorno y apuntan a recursos Azure válidos
>    ```
>
> 3. **Validar acceso Azure OpenAI**:
>    ```
>    ¿Mi identidad Azure actual puede acceder al recurso Azure OpenAI 
>    en mi AZURE_OPENAI_ENDPOINT? ¿Qué roles tengo asignados?
>    ```
>
> ¡Esto detecta problemas de configuración antes de ejecutar código!

</div>

### ☁️ Prerrequisitos Azure

- Una suscripción Azure activa con rol **Owner** o **Contributor**
- Cuota suficiente para los siguientes servicios:
  - Azure AI Foundry
  - Azure AI Search
  - Azure Managed Redis
  - Modelos Azure OpenAI (GPT-4o recomendado)

### ✅ Verificación

Después de la instalación, verifica tu configuración ejecutando estos comandos:

```powershell
# Verificar Azure CLI
az --version

# Verificar Terraform
terraform --version

# Verificar Python
python --version

# Verificar Agent Framework
pip show agent-framework

# Iniciar sesión en Azure (reemplaza con tu tenant)
az login --tenant <tu-tenant-id-o-dominio.com>

# Mostrar detalles de tu cuenta
az account show
```

<div class="warning" data-title="Importante">

> Asegúrate de estar conectado a la suscripción Azure correcta antes de proceder con el despliegue de infraestructura.

</div>

<div class="warning" data-title="🆘 ¿Necesitas Ayuda?">

> **¿Atascado durante la configuración? Así es como obtener ayuda:**
>
> - 📖 Consulta la [Guía de Solución de Problemas](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/wiki/Troubleshooting)
> - 🐛 [Reportar un problema de configuración](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[SETUP]%20&labels=setup,help-wanted)
> - 💬 [Hacer una pregunta en Discusiones](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions/categories/q-a)
>
> Al reportar problemas, por favor incluye:
> - Tu OS y versión de Python
> - El mensaje de error exacto
> - En qué paso estabas

</div>

---

## Desplegar Infraestructura

Primero, necesitas inicializar la infraestructura Terraform ejecutando los siguientes comandos.

### Opción 1: Entorno Local

Inicia sesión en tu cuenta Azure:

```bash
az login --tenant <tu-tenant-id o dominio.com>
```

### Opción 2: GitHub Codespace

Puede que necesites especificar el parámetro `--use-device-code` para facilitar el proceso de autenticación Azure CLI:

```bash
az login --use-device-code --tenant <tu-tenant-id o dominio.com>

# Mostrar detalles de tu cuenta
az account show
```

### Definir Variables de Entorno

Define la variable de entorno `ARM_SUBSCRIPTION_ID` con tu ID de suscripción Azure:

```bash
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

### Desplegar con Terraform

Navega al directorio `infra` e inicializa Terraform:

```bash
cd infra && terraform init
```

Luego ejecuta el siguiente comando para desplegar la infraestructura:

```bash
# Aplicar el despliegue directamente
terraform apply -auto-approve
```

<div class="hint" data-title="¿Problemas de Despliegue Terraform?">

> **Problemas de despliegue comunes:**
>
> 1. **"Provider not found"**: Ejecuta `terraform init -upgrade` para refrescar providers
> 2. **Cuota excedida**: Verifica Portal Azure → Suscripciones → Uso + cuotas
> 3. **Región no disponible**: Intenta cambiar la variable `location` en `variables.tf`
> 4. **Error de autenticación**: Asegúrate de que `az login` tuvo éxito y ejecuta `az account show` para verificar
> 5. **Error de bloqueo de estado**: Si el despliegue fue interrumpido, ejecuta `terraform force-unlock <LOCK_ID>`
>
> **Para ver logs detallados:**
> ```bash
> export TF_LOG=DEBUG
> terraform apply
> ```

</div>

<div class="info" data-title="Tiempo de Despliegue">

> El despliegue de infraestructura puede tomar 15-30 minutos dependiendo de la región Azure y disponibilidad de recursos.

</div>

---

## Módulo 1 — Crear un Agente Simple

En este módulo, descubrirás Microsoft Agent Framework y crearás tu primer agente.

### 🎯 Objetivos de Aprendizaje

- Entender los conceptos fundamentales de Agent Framework
- Crear un agente básico con Azure AI Foundry
- Ejecutar el agente y manejar respuestas

### 📖 Conceptos Clave

**Agent Framework** es el framework unificado de Microsoft para construir agentes IA que soporta:

- Múltiples proveedores LLM (Azure OpenAI, OpenAI, Anthropic, etc.)
- Llamada de herramientas y ejecución de funciones
- Orquestación multi-agentes
- Observabilidad con OpenTelemetry

<div class="hint" data-title="🤖 ¡Usa GitHub Copilot para Ayudarte!">

> **Copilot puede ayudarte a entender Agent Framework:**
>
> 1. **Pregunta a Copilot Chat** (`Ctrl+Shift+I`): `@workspace Explica qué hace AzureOpenAIChatClient y cómo configurarlo`
> 2. **Sugerencias inline**: Empieza a escribir `client = Azure` y deja que Copilot complete
> 3. **Obtener documentación**: Selecciona código y pregunta `/explain` para entender cada parámetro
>
> **Consejo**: Crea un archivo de instrucciones personalizado `.github/copilot-instructions.md`:
> ```markdown
> Usamos Microsoft Agent Framework con Azure OpenAI.
> Siempre usar DefaultAzureCredential para autenticación.
> Usar patrones async/await para todas las operaciones de agente.
> ```

</div>

### 💻 Crea Tu Primer Agente

Crea un nuevo archivo `src/module1_simple_agent.py`:

```python
"""Módulo 1: Agente Simple - Agente básico de bienvenida helpdesk."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Crear y ejecutar un agente helpdesk simple."""
    
    # Crear cliente Azure OpenAI con Azure Identity
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Crear el agente con instrucciones
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="""Eres un asistente de helpdesk IT amigable.
        
        Tu rol es:
        - Dar la bienvenida a los usuarios cordialmente
        - Entender sus problemas IT
        - Proporcionar orientación inicial
        - Escalar problemas complejos apropiadamente
        
        Sé siempre profesional y empático.""",
    )
    
    # Ejecutar el agente con una consulta simple
    query = "¡Hola, mi laptop no se conecta al VPN y tengo una reunión importante en 30 minutos!"
    print(f"Usuario: {query}")
    
    result = await agent.run(query)
    print(f"Agente: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 🚀 Ejecuta Tu Agente

```bash
python src/module1_simple_agent.py
```

<div class="hint" data-title="¿Errores de Autenticación?">

> **Solución de problemas Azure Identity:**
>
> 1. **DefaultAzureCredential falla**: Asegúrate de estar conectado con `az login`
> 2. **Endpoint no encontrado**: Verifica que `AZURE_OPENAI_ENDPOINT` esté correctamente definido (debe empezar con `https://`)
> 3. **Deployment no encontrado**: Verifica que el nombre del deployment coincida exactamente en Azure AI Foundry
> 4. **403 Forbidden**: Tu cuenta Azure podría no tener acceso al recurso OpenAI
>
> **Depurar la cadena de credenciales:**
> ```python
> from azure.identity import DefaultAzureCredential
> credential = DefaultAzureCredential(logging_enable=True)
> token = credential.get_token("https://cognitiveservices.azure.com/.default")
> print(f"Token adquirido: {token.token[:20]}...")
> ```

</div>

<div class="task" data-title="Ejercicio">

> Intenta modificar las instrucciones del agente para ser más específico sobre los pasos de solución de problemas VPN. ¿Qué cambia en la respuesta?

</div>

---

## Conclusión

¡Felicitaciones! 🎉 Has construido un **Asistente Helpdesk Ops** completo con:

### ✅ Lo Que Aprendiste

| Módulo | Habilidad |
|--------|-----------|
| 1 | Crear agentes básicos con Agent Framework |
| 2 | Salida estructurada con modelos Pydantic |
| 3 | Herramientas funcionales y llamada de herramientas |
| 4 | Integración de conocimientos con Azure AI Search |
| 5 | Workflows Group Chat multi-agentes |
| 6 | Orquestación avanzada con Handoff |
| 7 | Observabilidad con OpenTelemetry |
| 8 | Evaluación y pruebas de agentes |
| 9 | Memoria persistente con Redis |

### 📚 Recursos Adicionales

#### Agent Framework & Aprendizaje

- [Microsoft Agent Framework - GitHub](https://github.com/microsoft/agent-framework)
- [Agentes IA para Principiantes - Módulo Microsoft Agent Framework](https://microsoft.github.io/ai-agents-for-beginners/14-microsoft-agent-framework/)
- [Ejemplos de Workflows Agent Framework](https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/README.md)
- [Visión General de Orquestaciones](https://learn.microsoft.com/es-es/agent-framework/user-guide/workflows/orchestrations/overview)

#### Azure AI & Observabilidad

- [Azure AI Foundry](https://learn.microsoft.com/es-es/azure/ai-studio/)
- [Trazar Agentes con Azure AI SDK](https://learn.microsoft.com/es-es/azure/ai-foundry/how-to/develop/trace-agents-sdk?view=foundry-classic)
- [Model Context Protocol](https://modelcontextprotocol.io/)

#### Inspiración Workshop

- [GitHub Copilot Hands-on Lab (Ejemplo MOAW)](https://moaw.dev/workshop/gh:Philess/GHCopilotHoL/main/docs/?step=0)

### 🐛 ¿Encontraste un Problema? ¿Solicitud de Característica?

¡Queremos mejorar este laboratorio! Tu feedback es valioso.

<div class="task" data-title="Ayúdanos a Mejorar">

> **Reporta problemas o sugiere mejoras:**
>
> - 🐛 **Bug o Error**: [Abrir Issue](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=bug_report.md&title=[BUG]%20)
> - 💡 **Solicitud de Característica**: [Solicitar Característica](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=feature_request.md&title=[FEATURE]%20)
> - 📝 **Documentación**: [Sugerir Mejora de Doc](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[DOCS]%20)
> - 💬 **Preguntas**: [Iniciar una Discusión](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions)

</div>

<div class="info" data-title="Feedback">

> ¡Nos encantaría recibir tus comentarios! Por favor abre un issue o discusión en el repositorio del laboratorio.

</div>
