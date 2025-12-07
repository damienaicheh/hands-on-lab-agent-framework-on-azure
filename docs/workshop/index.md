---
published: true
type: workshop
title: Product Hands-on Lab - Agent Framework on Azure
short_title: Agent Framework on Azure
description: Build a complete Helpdesk Ops Assistant with Microsoft Agent Framework on Azure - from single agent to multi-agent orchestration with MCP servers, AI Search, and Redis.
level: intermediate
navigation_numbering: false
authors:
  - Olivier Mertens
  - Damien Aicheh
contacts:
  - "@olmertens"
  - "@damienaicheh"
duration_minutes: 300
tags: microsoft foundry, agent framework, ai search, managed redis, mcp, group chat, orchestration, observability, evaluation
navigation_levels: 2
banner_url: ../assets/banner.jpg
audience: developers, architects, AI engineers
sections_title:
  - Introduction
  - Scenario
  - Workshop Parts
  - Architecture
  - Start
---

# Helpdesk Ops Assistant - Agent Framework on Azure

> 🌍 **Languages:** [Français](./translations/fr/index.fr.md) | [Español](./translations/es/index.es.md) | [हिन्दी](./translations/hi/index.hi.md)

> 💻 **Language Support:** This workshop uses **Python**, but Microsoft Agent Framework is also available in **C#/.NET**. See the [official documentation](https://learn.microsoft.com/en-us/agent-framework/overview/agent-framework-overview){target="_blank"} for .NET examples.

Welcome to this hands-on lab! You will build a **mini-helpdesk powered by AI agents** that processes internal tickets using:

- 🔍 **Azure AI Search** for enterprise FAQ knowledge
- 🔧 **MCP Servers** for GitHub ticketing and Microsoft Learn documentation
- 🤖 **Multi-agent orchestration** with Microsoft Agent Framework
- 📊 **Observability** with OpenTelemetry and Microsoft Foundry

## 🎯 Scenario: Helpdesk Ops Assistant

You will build a complete helpdesk system with multiple specialized agents:

| Agent | Role | Tools/Integrations |
|-------|------|-------------------|
| **Orchestrator** | Routes requests, chooses workflow | Workflow control |
| **Complexity Analyst** | Analyzes tickets, structured output | Function tools |
| **Learn Agent** | Queries Microsoft Learn docs | MCP mslearn server |
| **GitHub Agent** | Creates/manages GitHub issues | MCP github server |

---

## 📚 Workshop Parts

This workshop is divided into **4 parts** for easier navigation:

| Part | Modules | Duration | Description |
|------|---------|----------|-------------|
| [**Part 1: Getting Started**](./part1-basics.md) | Setup + Modules 1-3 | 75 min | Prerequisites, infrastructure, simple agents, tools |
| [**Part 2: Knowledge & Collaboration**](./part2-knowledge.md) | Modules 4-5 | 65 min | AI Search integration, multi-agent Group Chat |
| [**Part 3: Production Ready**](./part3-production.md) | Modules 6-8 | 85 min | Orchestration, observability, evaluation |
| [**Part 4: Advanced & Conclusion**](./part4-advanced.md) | Module 9 + Resources | 40 min | Redis persistence, go further resources |

---

## 🗺️ Quick Navigation

<div class="info" data-title="Choose Your Path">

> **🚀 First time?** Start with [Part 1: Getting Started](./part1-basics.md)
>
> **🔍 Need a specific topic?** Jump directly to:
> - [Prerequisites & Setup](./part1-basics.md?step=1)
> - [Module 1: Simple Agent](./part1-basics.md?step=3)
> - [Module 2: Structured Output](./part1-basics.md?step=4)
> - [Module 3: Function Tools](./part1-basics.md?step=5)
> - [Module 4: AI Search / RAG](./part2-knowledge.md?step=2)
> - [Module 5: Group Chat](./part2-knowledge.md?step=3)
> - [Module 6: Orchestration](./part3-production.md?step=2)
> - [Module 7: Observability](./part3-production.md?step=3)
> - [Module 8: Evaluation](./part3-production.md?step=4)
> - [Module 9: Redis](./part4-advanced.md?step=2)
> - [Conclusion & Resources](./part4-advanced.md?step=3)

</div>

---

## 🏗️ Architecture Overview

```text
┌─────────────────────────────────────────────────────────────────────┐
│                           📥 INPUT                                  │
│                      👤 User Request                                │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🎯 ORCHESTRATION LAYER                           │
│                       🧠 Orchestrator                               │
└───────────┬──────────────────┼──────────────────┬───────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
       ┌─────────┐       ┌───────────┐      ┌────────────┐
       │⚡ Simple │       │👥 Group   │      │🚨 Escalation│
       │         │       │   Chat    │      │            │
       └────┬────┘       └─────┬─────┘      └──────┬─────┘
            │                  │                   │
            │           ┌──────┴──────┐            │
            │           │  🤖 AGENTS  │            │
            │           │ ┌─────────┐ │            │
            │           │ │📚 Learn │ │            │
            │           │ │🐙 GitHub│ │            │
            │           │ └────┬────┘ │            │
            │           └──────┼──────┘            │
            │                  │                   │
            │                  ▼                   │
            │         ┌───────────────┐            │
            │         │🔍 AI Search   │            │
            │         └───────────────┘            │
            │                                      │
            └───────────────┬──────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        ☁️ AZURE SERVICES                            │
│     💾 Redis Cache          📊 Application Insights                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## ▶️ Start the Workshop

<div class="task" data-title="Let's Begin!">

> Click below to start with Part 1:
>
> **[🚀 Start Part 1: Getting Started →](./part1-basics.md)**

</div>
