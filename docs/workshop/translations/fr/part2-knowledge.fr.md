---
published: true
type: workshop
title: "Partie 2 : Gestion des connaissances"
short_title: "Connaissances"
description: RAG avec Azure AI Search et collaboration multi-agents avec MCP
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 55
tags: rag, azure-ai-search, group-chat, mcp, multi-agent
banner_url: ../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - Introduction
  - 🏠 Navigation
  - Code de la Partie 1
  - Module 4 - Azure AI Search
  - Module 5 - Discussion de groupe
  - Partie 2 terminée
---

# Partie 2 : Gestion des connaissances

![Banner Workshop](../../assets/banner.jpg)

> 🌍 **[← Partie 1 : Les fondamentaux](./part1-basics.fr.md)** | **[Partie 3 : Prêt pour la production →](./part3-production.fr.md)**

---

## 🏠 Navigation

<div class="tip" data-title="Navigation de l'atelier">

> **📚 Toutes les parties :**
> - [🏠 Accueil de l'atelier](./index.fr.md)
> - [Partie 1 : Les fondamentaux](./part1-basics.fr.md)
> - [Partie 2 : Gestion des connaissances](./part2-knowledge.fr.md) *(actuel)*
> - [Partie 3 : Prêt pour la production](./part3-production.fr.md)
> - [Partie 4 : Pour aller plus loin](./part4-advanced.fr.md)
>
> **🌍 Cette page en d'autres langues :**
> - [🇬🇧 English](/workshop/part2-knowledge.md)
> - [🇪🇸 Español](/workshop/translations/es/part2-knowledge.es.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part2-knowledge.hi.md)

</div>

---

## 📦 Code de la Partie 1

Avant de commencer, assurez-vous de disposer du code de la Partie 1 :

<details>
<summary>📁 Structure du projet (cliquez pour afficher)</summary>

```text
helpdesk-agent/
├── .env                          # Variables d'environnement
├── requirements.txt              # Dépendances Python
└── src/
    ├── module1_simple_agent.py   # Agent simple avec streaming
    ├── module2_structured.py     # Sortie structurée Pydantic
    └── module3_tools.py          # Outils fonction avec @ai_function
```

</details>

<details>
<summary>🔧 Composants à Réutiliser (cliquez pour développer)</summary>

```python
# Configuration client de base (réutilisez dans tous les modules)
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient

client = AzureOpenAIChatClient(
    credential=DefaultAzureCredential(),
    endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    deployment_name="gpt-4o",
)

# Modèle Pydantic du Module 2
from pydantic import BaseModel, Field
from typing import Literal

class TicketAnalysis(BaseModel):
    category: Literal["network", "hardware", "software", "access"]
    severity: Literal["low", "medium", "high", "critical"]
    summary: str = Field(max_length=200)
    suggested_actions: list[str]

# Outils fonction du Module 3
from agent_framework import ai_function

@ai_function
def create_ticket(title: str, description: str, priority: str = "medium") -> str:
    """Crée un nouveau ticket helpdesk."""
    ticket_id = f"TKT-{hash(title) % 10000:04d}"
    return f"✅ Ticket {ticket_id} créé : {title} (Priorité: {priority})"
```

</details>

<div class="info" data-title="Partie 1 non complétée ?">

> Complétez d'abord [Partie 1 : Les Bases](part1-basics.fr.md), ou copiez le code ci-dessus.

</div>

| Module | Sujet | Ce que vous construisez |
|--------|-------|-------------------------|
| 4 | **Azure AI Search** | Agent avec RAG (documentation IT) |
| 5 | **Group Chat** | Multi-agents collaboratifs avec MCP |

---

## Module 4 — Intégration Azure AI Search

Ajoutez une base de connaissances à votre agent avec RAG.

### 📚 Concept : RAG (Retrieval-Augmented Generation)

```text
┌──────────┐    ┌───────────┐    ┌──────────┐    ┌───────────┐    ┌──────────┐    ┌──────────┐
│ Question │───▶│🔍Recherche│───▶│ 📚 Index │───▶│📄 Contexte│───▶│ 🤖 LLM   │───▶│ Réponse  │
└──────────┘    └───────────┘    └──────────┘    └───────────┘    └──────────┘    └──────────┘
```

| Sans RAG | Avec RAG |
|----------|----------|
| Répond depuis le training | Répond depuis VOS documents |
| Connaissances gelées | Connaissances actualisées |
| Pas de sources | Réponses sourcées |

**Composants Azure AI Search :**

| Composant | Rôle |
|-----------|------|
| **Index** | Collection de documents recherchables |
| **Embeddings** | Vecteurs pour recherche sémantique |
| **AzureAISearchProvider** | Connecteur Agent Framework |

### 🧠 Pseudo-code

```
ALGORITHME : Agent avec RAG

1. CRÉER PROVIDER AI Search
   - Connexion à l'index
   - Même embedding que l'indexation

2. CRÉER AGENT avec context_providers=[provider]

3. AUTOMATIQUEMENT :
   - Question utilisateur → Recherche dans l'index
   - Documents pertinents → Ajoutés au contexte
   - LLM répond avec ces informations
```

### 🔨 Exercice

Créez `src/module4_knowledge_agent.py`.

<details>
<summary>💡 Indice : Configuration Provider</summary>

```python
from agent_framework.azure_ai_search import AzureAISearchProvider

search_provider = AzureAISearchProvider(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    credential=DefaultAzureCredential(),
    index_name="it-documentation",
    embedding_client=embedding_client,
    top_k=5,  # Nombre de documents à récupérer
)
```

</details>

<details>
<summary>💡 Indice : Agent avec Provider</summary>

```python
agent = client.create_agent(
    name="KnowledgeAgent",
    instructions="""Tu es un expert IT.
    Utilise le contexte fourni pour répondre.
    Cite tes sources quand possible.""",
    context_providers=[search_provider],
)
```

</details>

### ✅ Solution

<details>
<summary>📄 Code Complet Module 4</summary>

```python
"""Module 4 : Intégration Azure AI Search."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.azure_ai_search import AzureAISearchProvider


async def main():
    credential = DefaultAzureCredential()
    
    client = AzureOpenAIChatClient(
        credential=credential,
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Client pour embeddings
    embedding_client = AzureOpenAIChatClient(
        credential=credential,
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="text-embedding-ada-002",
    )
    
    # Provider Azure AI Search
    search_provider = AzureAISearchProvider(
        endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
        credential=credential,
        index_name="it-documentation",
        embedding_client=embedding_client,
        top_k=5,
    )
    
    agent = client.create_agent(
        name="ITExpert",
        instructions="""Tu es un expert IT avec accès à la documentation.
        Réponds en te basant sur le contexte fourni.
        Cite les sources quand applicable.""",
        context_providers=[search_provider],
    )
    
    questions = [
        "Comment configurer le VPN sur Windows ?",
        "Quelle est la procédure de reset mot de passe ?",
        "Comment accéder au SharePoint depuis l'extérieur ?",
    ]
    
    thread = agent.get_new_thread()
    
    for question in questions:
        print(f"\n❓ {question}")
        result = await agent.run(question, thread=thread)
        print(f"💡 {result.text[:300]}...")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module4_knowledge_agent.py
```

<div class="task" data-title="🎯 Défi">

> Modifiez `top_k` et observez l'impact sur la qualité des réponses. Ajoutez un filtre par catégorie de document.

</div>

---

## Module 5 — Group Chat Multi-Agent

Créez un workflow collaboratif avec plusieurs agents spécialisés.

### 📚 Concept : Group Chat avec MCP

```text
                    👤 Utilisateur
                          │
                          ▼
              ┌───────────────────────┐
              │    💬 Group Chat      │
              └───────────┬───────────┘
                          │
         ┌────────────────┼────────────────┐
         │                │                │
         ▼                ▼                ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐
│ 📚 LearnAgent   │ │ 🐙 GitHubAgent  │ │ 🔍 Analyste │
│ MCP: MS Learn   │ │ MCP: GitHub     │ │             │
└────────┬────────┘ └────────┬────────┘ └──────┬──────┘
         │                   │                 │
         └────────────────┬──┴─────────────────┘
                          │
                          ▼
              ┌───────────────────────┐
              │ 📋 Réponse Consolidée │
              └───────────────────────┘
```

**Model Context Protocol (MCP) :**

| Concept | Description |
|---------|-------------|
| **MCP** | Protocole standard pour connecter IA ↔ données |
| **MCP Server** | Service exposant des outils (GitHub, Slack, etc.) |
| **MCP Tool** | Outil utilisable par l'agent |

### 🧠 Pseudo-code

```
ALGORITHME : Group Chat avec MCP

1. CRÉER AGENTS SPÉCIALISÉS
   - LearnAgent (MCP: mcp-server-fetch)
   - GitHubAgent (MCP: github-mcp-server)
   - AnalystAgent (analyse et synthèse)

2. CONSTRUIRE GROUP CHAT
   - GroupChatBuilder
   - Ajouter tous les agents
   - Configurer rounds max

3. EXÉCUTER
   - Chaque agent contribue
   - Résultats consolidés
```

### 🔨 Exercice

Créez `src/module5_group_chat.py`.

<details>
<summary>💡 Indice : Agent avec MCP Tool</summary>

```python
from agent_framework.mcp import MCPTool

async with MCPTool("npx", ["-y", "@anthropic/mcp-server-fetch"]) as fetch_tool:
    learn_agent = ChatAgent(
        chat_client=client,
        name="LearnAgent",
        instructions="Tu recherches dans Microsoft Learn...",
        tools=[fetch_tool],
    )
```

</details>

<details>
<summary>💡 Indice : GroupChatBuilder</summary>

```python
from agent_framework.workflows import GroupChatBuilder

group_chat = (
    GroupChatBuilder()
    .add_agent(analyst)
    .add_agent(learn_agent)
    .add_agent(github_agent)
    .set_max_rounds(3)
    .build()
)
```

</details>

<details>
<summary>💡 Indice : Streaming Événements</summary>

```python
async for event in group_chat.run_stream(query):
    if hasattr(event, 'text') and event.text:
        agent_name = getattr(event, 'agent_name', 'System')
        print(f"[{agent_name}]: {event.text}")
```

</details>

### ✅ Solution

<details>
<summary>📄 Code Complet Module 5</summary>

```python
"""Module 5 : Group Chat Multi-Agent avec MCP."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.mcp import MCPTool
from agent_framework.workflows import GroupChatBuilder


async def main():
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Agent Analyste (sans MCP)
    analyst = ChatAgent(
        chat_client=client,
        name="Analyst",
        instructions="""Tu analyses les problèmes IT et coordonnes.
        Synthétise les contributions des autres agents.""",
    )
    
    # Agents avec MCP
    async with MCPTool("npx", ["-y", "@anthropic/mcp-server-fetch"]) as fetch_tool:
        learn_agent = ChatAgent(
            chat_client=client,
            name="LearnAgent",
            instructions="""Tu recherches dans Microsoft Learn.
            Fournis documentation et bonnes pratiques.""",
            tools=[fetch_tool],
        )
        
        async with MCPTool("npx", ["-y", "@anthropic/github-mcp-server"]) as gh_tool:
            github_agent = ChatAgent(
                chat_client=client,
                name="GitHubAgent",
                instructions="""Tu recherches dans GitHub.
                Trouve exemples de code et issues similaires.""",
                tools=[gh_tool],
            )
            
            # Construire le Group Chat
            group_chat = (
                GroupChatBuilder()
                .add_agent(analyst)
                .add_agent(learn_agent)
                .add_agent(github_agent)
                .set_max_rounds(3)
                .build()
            )
            
            query = "Comment implémenter l'authentification Azure AD dans une app Python ?"
            
            print(f"❓ {query}\n")
            print("=" * 50)
            
            async for event in group_chat.run_stream(query):
                if hasattr(event, 'text') and event.text:
                    agent_name = getattr(event, 'agent_name', 'System')
                    print(f"\n[{agent_name}]:\n{event.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module5_group_chat.py
```

<div class="warning" data-title="⚠️ MCP Servers">

> Les serveurs MCP nécessitent Node.js installé. Si `npx` échoue, installez Node.js depuis [nodejs.org](https://nodejs.org).

</div>

<div class="task" data-title="🎯 Défi">

> Ajoutez un quatrième agent `SecurityAgent` qui vérifie les implications sécurité. Configurez-le pour intervenir en dernier.

</div>

---

## Résumé Partie 2

Vous avez appris :

| Module | Compétence |
|--------|------------|
| **4** | ✅ RAG avec Azure AI Search |
| **5** | ✅ Group Chat multi-agent avec MCP |

**Patterns clés :**

```python
# RAG avec context_providers
agent = client.create_agent(
    context_providers=[search_provider],
    ...
)

# Multi-agent avec GroupChatBuilder
group_chat = (
    GroupChatBuilder()
    .add_agent(agent1)
    .add_agent(agent2)
    .build()
)
```

**Architecture construite :**

```
┌─────────────────────────────────────┐
│         GROUP CHAT                  │
├─────────────────────────────────────┤
│  📚 LearnAgent ──→ MCP: Fetch       │
│  🐙 GitHubAgent ──→ MCP: GitHub     │
│  🔍 Analyste ──→ Synthèse           │
├─────────────────────────────────────┤
│  Tous connectés à AI Search (RAG)   │
└─────────────────────────────────────┘
```

> 🌍 **[← Partie 1 : Les Bases](part1-basics.fr.md)** | **[Partie 3 : Production Ready →](part3-production.fr.md)**
