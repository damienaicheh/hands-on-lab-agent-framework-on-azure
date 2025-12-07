---
published: true
type: workshop
title: "Taller Agent Framework en Azure"
short_title: "Agent Framework Lab"
description: Construye un asistente Helpdesk con Microsoft Agent Framework en Azure
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 180
tags: agent-framework, azure, ia, multi-agente, mcp, rag
banner_url: ../../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - Inicio
  - Acerca de
  - Partes
  - Recursos
---

# 🤖 Taller Agent Framework en Azure

> **¡Bienvenido!** Construye un **Helpdesk Ops Assistant** completo con Microsoft Agent Framework.

## 📋 Acerca de este Taller

| Info | Detalles |
|------|----------|
| **Duración** | ~3 horas |
| **Nivel** | Intermedio |
| **Requisitos** | Python, nociones de Azure |
| **Lo que construirás** | Sistema multi-agente con RAG, MCP, observabilidad |

## 🏗️ Arquitectura

```text
┌─────────────────────────────────────────────────────────────────────┐
│                           📥 ENTRADA                                │
│                   👤 Solicitud del Usuario                         │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🎯 CAPA DE ORQUESTACIÓN                          │
│                       🧠 Orquestador                               │
└───────────┬──────────────────┼──────────────────┬───────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
       ┌───────────┐     ┌───────────┐      ┌───────────────┐
       │⚡ Flujo   │     │👥 Group   │      │🚨 Escalamiento │
       │  Simple  │     │   Chat    │      │               │
       └────┬──────┘     └─────┬─────┘      └───────────────┘
            │                  │                   
            │                  ▼                   
            │         ┌───────────────┐            
            │         │🔍 AI Search   │            
            │         └───────────────┘            
            │                                      
            └───────────────┬──────────────────────
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ☁️ SERVICIOS AZURE                            │
│       💾 Redis Cache         📊 Application Insights                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📚 Ruta del Taller

El taller está dividido en **4 partes** para facilitar la navegación:

### 🔷 [Parte 1: Los Fundamentos](./part1-basics.es.md)
> Requisitos, despliegue de infraestructura y módulos fundamentales

| Módulo | Tema | Duración |
|--------|------|----------|
| Setup | Requisitos y Despliegue | 20 min |
| 1 | Agente Simple con Streaming | 15 min |
| 2 | Salida Estructurada (Pydantic) | 15 min |
| 3 | Herramientas de Función | 20 min |

### 🔷 [Parte 2: Integración de Conocimiento](./part2-knowledge.es.md)
> RAG con Azure AI Search y workflows multi-agente

| Módulo | Tema | Duración |
|--------|------|----------|
| 4 | Integración Azure AI Search | 25 min |
| 5 | Group Chat Multi-Agente con MCP | 30 min |

### 🔷 [Parte 3: Listo para Producción](./part3-production.es.md)
> Orquestación avanzada, observabilidad, evaluación

| Módulo | Tema | Duración |
|--------|------|----------|
| 6 | Orquestación Handoff | 25 min |
| 7 | Observabilidad OpenTelemetry | 20 min |
| 8 | Evaluación y Pruebas | 20 min |

### 🔷 [Parte 4: Avanzado y Recursos](./part4-advanced.es.md)
> Persistencia Redis, estructura del proyecto, recursos de producción

| Módulo | Tema | Duración |
|--------|------|----------|
| 9 | Integración Redis | 25 min |
| - | Conclusión y Recursos | 10 min |

---

## 🚀 Navegación Rápida

<div class="info" data-title="Elige tu camino">

> **🚀 ¿Primera vez?** Empieza con [Parte 1: Los Fundamentos](./part1-basics.es.md)
>
> **🔍 ¿Necesitas un tema específico?** Salta directamente a:
> - [Requisitos y Configuración](./part1-basics.es.md?step=1)
> - [Módulo 1: Agente Simple](./part1-basics.es.md?step=3)
> - [Módulo 2: Salida Estructurada](./part1-basics.es.md?step=4)
> - [Módulo 3: Herramientas de Función](./part1-basics.es.md?step=5)
> - [Módulo 4: AI Search / RAG](./part2-knowledge.es.md?step=2)
> - [Módulo 5: Group Chat](./part2-knowledge.es.md?step=3)
> - [Módulo 6: Orquestación](./part3-production.es.md?step=2)
> - [Módulo 7: Observabilidad](./part3-production.es.md?step=3)
> - [Módulo 8: Evaluación](./part3-production.es.md?step=4)
> - [Módulo 9: Redis](./part4-advanced.es.md?step=2)
> - [Conclusión y Recursos](./part4-advanced.es.md?step=3)

</div>

---

## 🌍 Otros Idiomas

- 🇬🇧 [English](../../index.md)
- 🇫🇷 [Français](../fr/index.fr.md)
- 🇪🇸 Español (actual)
- 🇮🇳 [हिन्दी](../hi/index.hi.md)

---

<div class="info" data-title="💡 Consejo">

> Cada parte es autónoma. Puedes hacerlas en orden o saltar a los módulos que te interesen.
>
> **Copilot Hints** 🤖: ¡Busca las secciones desplegables con consejos para GitHub Copilot!

</div>
