---
published: true
type: workshop
title: "Partie 4 : Pour aller plus loin"
short_title: "Pour aller plus loin"
description: Persistance Redis, structure projet complète, ressources pour la production
level: advanced
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 45
tags: redis, persistance, architecture, production, ressources, conclusion
banner_url: ../../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - 🏠 Navigation
  - Code des Parties 1-3
  - Module 9 - Redis
  - Conclusion
  - Ressources
---

# Partie 4 : Pour aller plus loin

![Banner Workshop](../../../assets/banner.jpg)

> 🌍 **[← Partie 3 : Prêt pour la production](./part3-production.fr.md)** | **[🏠 Accueil Atelier](./index.fr.md)**

---

## 🏠 Navigation

<div class="tip" data-title="Navigation de l'atelier">

> **📚 Toutes les parties :**
> - [🏠 Accueil de l'atelier](./index.fr.md)
> - [Partie 1 : Les fondamentaux](./part1-basics.fr.md)
> - [Partie 2 : Gestion des connaissances](./part2-knowledge.fr.md)
> - [Partie 3 : Prêt pour la production](./part3-production.fr.md)
> - [Partie 4 : Pour aller plus loin](./part4-advanced.fr.md) *(actuel)*
>
> **🌍 Cette page en d'autres langues :**
> - [🇬🇧 English](/workshop/part4-advanced.md)
> - [🇪🇸 Español](/workshop/translations/es/part4-advanced.es.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part4-advanced.hi.md)

</div>

---

Dernière partie de l'atelier.

---

## 📦 Code des Parties 1-3

Avant de continuer, assurez-vous d'avoir le code complet des parties précédentes :

<details>
<summary>📁 Structure complète du projet (cliquez pour afficher)</summary>

```text
helpdesk-agent/
├── .env                            # Toutes les variables d'environnement
├── requirements.txt                # Dépendances
├── pyproject.toml                  # Configuration projet
└── src/
    ├── module1_simple_agent.py     # Partie 1: Agent simple
    ├── module2_structured.py       # Partie 1: Sortie structurée
    ├── module3_tools.py            # Partie 1: Outils fonction
    ├── module4_rag.py              # Partie 2: AI Search RAG
    ├── module5_group_chat.py       # Partie 2: Group Chat + MCP
    ├── module6_orchestration.py    # Partie 3: Orchestration Handoff
    ├── module7_observability.py    # Partie 3: Tracing OpenTelemetry
    └── module8_evaluation.py       # Partie 3: Évaluation qualité
```

</details>

<details>
<summary>🔧 Composants Clés de la Partie 3 (cliquez pour développer)</summary>

```python
# Pattern d'orchestration du Module 6
from agent_framework import HandoffOrchestrator

orchestrator = HandoffOrchestrator(
    agents=[analyst, resolver, escalator],
    default_agent=analyst,
)

# Configuration observabilité du Module 7
from azure.monitor.opentelemetry import configure_azure_monitor
from opentelemetry import trace

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
)
tracer = trace.get_tracer(__name__)

# Pattern d'évaluation du Module 8
async def evaluate_agent() -> dict:
    """Evaluate l'agent sur des cas de test."""
    test_cases = [
        {"input": "VPN ne fonctionne pas", "expected_category": "network"},
        {"input": "Laptop ne démarre pas", "expected_category": "hardware"},
    ]
    # Exécuter les tests et calculer les métriques...
```

</details>

<details>
<summary>📋 Toutes les Variables d'Environnement (cliquez pour développer)</summary>

```bash
# Fichier .env - liste complète pour Partie 4
# Azure OpenAI
AZURE_OPENAI_ENDPOINT=https://votre-ressource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Azure AI Search
AZURE_SEARCH_ENDPOINT=https://votre-search.search.windows.net
AZURE_SEARCH_INDEX_NAME=helpdesk-faq

# MCP & GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Observabilité
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...

# Nouveau pour Partie 4 - Redis
REDIS_CONNECTION_STRING=rediss://votre-redis.redis.cache.windows.net:6380?password=xxx
```

</details>

<div class="info" data-title="Parties 1-3 non complétées ?">

> Complétez d'abord toutes les parties précédentes :
>
> - [Partie 1 : Les Bases](part1-basics.fr.md)
> - [Partie 2 : Intégration Connaissances](part2-knowledge.fr.md)
> - [Partie 3 : Production Ready](part3-production.fr.md)
>
> Ou utilisez les extraits de code ci-dessus.

</div>

---

| Section | Contenu |
|---------|---------|
| **Module 9** | Persistance Redis pour la mémoire |
| **Conclusion** | Résumé architecture |
| **Ressources** | Aller plus loin + liens |

---

## Module 9 — Intégration Redis

Ajoutez la persistance des conversations avec Azure Managed Redis.

### 📚 Concept : Pourquoi la Persistance ?

| Sans Persistance | Avec Redis |
|------------------|------------|
| "Quel était mon dernier problème ?" → "Je ne sais pas" | "Vous avez signalé un problème VPN lundi" |
| Répéter le dépannage à chaque fois | Construire sur les solutions précédentes |
| État perdu au redémarrage | Reprendre les conversations à tout moment |

**Architecture :**

```
SESSION 1 (Lundi)
┌────────────────────────────────────┐
│ User: "Le VPN se déconnecte"       │
│ Agent: "Essayez de réinitialiser...│
│           ↓                        │
│     ┌──────────────┐               │
│     │ REDIS STORE  │               │
│     │ • Historique │               │
│     │ • Contexte   │               │
│     └──────────────┘               │
└────────────────────────────────────┘
            ↓
SESSION 2 (Mercredi)  
┌────────────────────────────────────┐
│ User: "Encore le problème VPN"     │
│ Agent: "Je vois que vous aviez ce  │
│         problème lundi. Essayons   │
│         les étapes suivantes..."   │
└────────────────────────────────────┘
```

| Composant | Rôle |
|-----------|------|
| **RedisProvider** | Mémoire sémantique (faits, préférences) |
| **RedisChatMessageStore** | Historique des conversations |
| **thread_id** | Lie les sessions pour une même conversation |
| **user_id** | Groupe les données pour un utilisateur |

### 🧠 Pseudo-code

```
ALGORITHME : Agent avec Mémoire Redis

1. CONFIGURER CONNEXION REDIS :
   - Connection string depuis environnement
   - Définir user_id, thread_id

2. CRÉER REDIS PROVIDER :
   - Pour la mémoire sémantique
   - Définir index_name et prefix

3. CRÉER FACTORY MESSAGE STORE :
   - Retourne RedisChatMessageStore
   - Définir limite max_messages

4. CRÉER AGENT AVEC PROVIDERS :
   - context_providers=redis_provider
   - chat_message_store_factory=factory

5. SÉRIALISER/DÉSÉRIALISER :
   - thread.serialize() → Sauvegarder
   - agent.deserialize_thread() → Reprendre
```

### 🔨 Exercice

Créez `src/module9_redis_agent.py`.

<details>
<summary>💡 Indice : Configuration RedisProvider</summary>

```python
from agent_framework_redis import RedisProvider

redis_provider = RedisProvider(
    redis_url=os.getenv("REDIS_CONNECTION_STRING"),
    index_name="helpdesk_memory",
    prefix="helpdesk",
    application_id="helpdesk_assistant",
    agent_id="support_agent",
    user_id=user_id,
    thread_id=thread_id,
)
```

</details>

<details>
<summary>💡 Indice : Factory Message Store</summary>

```python
from agent_framework_redis import RedisChatMessageStore

def create_message_store():
    return RedisChatMessageStore(
        redis_url=redis_url,
        thread_id=thread_id,
        key_prefix="chat_messages",
        max_messages=100,
    )
```

</details>

<details>
<summary>💡 Indice : Agent avec Persistance</summary>

```python
agent = client.create_agent(
    name="PersistentAssistant",
    instructions="Tu es un assistant IT avec mémoire...",
    context_providers=redis_provider,
    chat_message_store_factory=create_message_store,
)
```

</details>

<details>
<summary>💡 Indice : Sérialisation Thread</summary>

```python
# Sauvegarder en fin de session
serialized = await thread.serialize()

# Reprendre plus tard
resumed_thread = await agent.deserialize_thread(serialized)
result = await agent.run("Continuons notre conversation", thread=resumed_thread)
```

</details>

### ✅ Solution

<details>
<summary>📄 Code Complet Module 9</summary>

```python
"""Module 9 : Intégration Redis - Conversations persistantes."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework_redis import RedisProvider, RedisChatMessageStore


async def main() -> None:
    """Crée un agent avec mémoire Redis."""
    
    redis_url = os.getenv("REDIS_CONNECTION_STRING")
    user_id = "user_12345"
    thread_id = "helpdesk_session_001"
    
    redis_provider = RedisProvider(
        redis_url=redis_url,
        index_name="helpdesk_memory",
        prefix="helpdesk",
        application_id="helpdesk_assistant",
        agent_id="support_agent",
        user_id=user_id,
        thread_id=thread_id,
    )
    
    def create_message_store():
        return RedisChatMessageStore(
            redis_url=redis_url,
            thread_id=thread_id,
            key_prefix="chat_messages",
            max_messages=100,
        )
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="PersistentAssistant",
        instructions="""Tu es un assistant IT avec mémoire.
        Souviens-toi des préférences, problèmes précédents et solutions.""",
        context_providers=redis_provider,
        chat_message_store_factory=create_message_store,
    )
    
    conversations = [
        "Salut, j'ai encore des problèmes VPN",
        "C'est le même problème que la semaine dernière",
        "Qu'est-ce que je peux essayer d'autre ?",
    ]
    
    thread = agent.get_new_thread()
    print("💬 Démarrage conversation persistante\n")
    
    for message in conversations:
        print(f"User: {message}")
        result = await agent.run(message, thread=thread)
        print(f"Agent: {result.text}\n")
    
    # Sauvegarder pour plus tard
    serialized = await thread.serialize()
    print(f"📦 Thread sauvegardé: {len(serialized)} bytes")
    
    # Reprendre plus tard
    print("\n--- Session reprise ---\n")
    resumed_thread = await agent.deserialize_thread(serialized)
    result = await agent.run("De quoi on parlait ?", thread=resumed_thread)
    print(f"Agent: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

</details>

```bash
python src/module9_redis_agent.py
```

<div class="hint" data-title="Problèmes Connexion Redis ?">

> - Utilisez `rediss://` (SSL) et non `redis://` pour Azure
> - Format : `rediss://<name>.redis.cache.windows.net:6380?password=<key>`
> - Test : `redis.from_url(url).ping()` → doit retourner `True`

</div>

<div class="task" data-title="🎯 Défi">

> Ajoutez un TTL pour expirer les anciennes conversations après 7 jours. Créez un helper pour lister tous les threads d'un utilisateur.

</div>

---

## Conclusion

🎉 **Félicitations !** Vous avez construit un **Helpdesk Ops Assistant** complet !

### ✅ Ce que Vous Avez Appris

| Module | Compétence |
|--------|------------|
| 1 | Agents basiques avec Agent Framework |
| 2 | Sortie structurée avec Pydantic |
| 3 | Outils fonction et tool calling |
| 4 | Intégration connaissances avec AI Search |
| 5 | Group Chat multi-agent avec MCP |
| 6 | Orchestration avancée avec Handoff |
| 7 | Observabilité avec OpenTelemetry |
| 8 | Évaluation et tests agents |
| 9 | Mémoire persistante avec Redis |

### 📁 Structure Projet

```
helpdesk-ops-assistant/
├── 📁 .github/
│   ├── 📁 agents/                      # Agents Copilot personnalisés
│   │   └── AgentArchitect.agent.md
│   ├── 📁 prompts/                     # Prompts réutilisables
│   │   └── evaluate-agent.prompt.md
│   └── copilot-instructions.md         # Instructions projet
│
├── 📁 infra/                           # Terraform IaC
│   ├── aai.tf                          # Microsoft Foundry
│   ├── ai_search.tf                    # AI Search
│   ├── foundry.tf                      # AI Foundry workspace
│   ├── foundry_models.tf               # Déploiements modèles
│   ├── managed_redis.tf                # Redis
│   ├── log.tf                          # App Insights
│   └── variables.tf
│
├── 📁 src/                             # Modules Python
│   ├── module1_simple_agent.py
│   ├── module2_complexity_analyst.py
│   ├── module3_function_tools.py
│   ├── module4_knowledge_agent.py
│   ├── module5_group_chat.py
│   ├── module6_orchestration.py
│   ├── module7_observability.py
│   ├── module8_evaluation.py
│   └── module9_redis_agent.py
│
├── 📁 docs/                            # Documentation atelier
│   ├── workshop.md
│   └── 📁 assets/
│       └── banner.jpg
│
├── .env.example
├── requirements.txt
└── README.md
```

### 🏗️ Résumé Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                           📥 ENTRÉE                                 │
│                       👤 Utilisateur                                │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      🎯 ORCHESTRATION                               │
│                       🧠 Orchestrateur                              │
└───────────┬──────────────────┼──────────────────┬───────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
       ┌─────────┐       ┌───────────┐      ┌────────────┐
       │⚡ Simple │       │👥 Group   │      │🚨 Escalade │
       │         │       │   Chat    │      │            │
       └────┬────┘       └─────┬─────┘      └────────────┘
            │                  │                   
            │           ┌──────┴──────┐            
            │           │  🤖 AGENTS  │            
            │           │ ┌──────────┐│            
            │           │ │📚 Learn  ││            
            │           │ │   Agent  ││            
            │           │ ├──────────┤│            
            │           │ │🐙 GitHub ││            
            │           │ │   Agent  ││            
            │           │ └────┬─────┘│            
            │           └──────┼──────┘            
            │                  │                   
            │                  ▼                   
            │         ┌───────────────┐            
            │         │🔍 AI Search   │            
            │         └───────────────┘            
            │                                      
            └───────────────┬──────────────────────
                            ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      ☁️ SERVICES AZURE                              │
│       💾 Redis Cache         📊 Application Insights                │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Ressources

### 📚 Documentation Principale

| Ressource | Lien |
|-----------|------|
| **Agent Framework GitHub** | [🔗 microsoft/agent-framework](https://github.com/microsoft/agent-framework){target="_blank"} |
| **Agent Framework Docs** | [🔗 learn.microsoft.com](https://learn.microsoft.com/fr-fr/agent-framework/){target="_blank"} |
| **AI Agents for Beginners** | [🔗 Module 14: Agent Framework](https://microsoft.github.io/ai-agents-for-beginners/14-microsoft-agent-framework/){target="_blank"} |
| **Exemples Workflows** | [🔗 Workflows README](https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/README.md){target="_blank"} |

### 🚀 Fonctionnalités Avancées

| Fonctionnalité | Description | Lien |
|----------------|-------------|------|
| **Shared State** | Partager l'état entre agents | [🔗 Guide](https://learn.microsoft.com/fr-fr/agent-framework/user-guide/workflows/shared-states){target="_blank"} |
| **Checkpoints** | Sauvegarder/restaurer l'état workflow | [🔗 Guide](https://learn.microsoft.com/fr-fr/agent-framework/user-guide/workflows/checkpoints){target="_blank"} |
| **AG-UI** | Construire des UIs agents avec streaming | [🔗 Intégration AG-UI](https://learn.microsoft.com/fr-fr/agent-framework/integrations/ag-ui/){target="_blank"} |

### 🔐 Production & Sécurité

| Sujet | Description | Lien |
|-------|-------------|------|
| **Azure APIM** | Sécuriser et scaler les APIs agent | [🔗 Docs APIM](https://learn.microsoft.com/fr-fr/azure/api-management/){target="_blank"} |
| **GenAI Gateway** | Rate limiting basé tokens | [🔗 Intégration OpenAI](https://learn.microsoft.com/fr-fr/azure/api-management/api-management-howto-integrate-openai){target="_blank"} |
| **Identités Managées** | Éliminer les secrets | [🔗 Docs MI](https://learn.microsoft.com/fr-fr/azure/active-directory/managed-identities-azure-resources/){target="_blank"} |

### 🔌 MCP (Model Context Protocol)

| Sujet | Description | Lien |
|-------|-------------|------|
| **Spécification MCP** | Protocole ouvert pour connexions IA-données | [🔗 modelcontextprotocol.io](https://modelcontextprotocol.io/){target="_blank"} |
| **Serveurs MCP** | Serveurs pré-construits (GitHub, Slack, etc.) | [🔗 Registre Serveurs](https://github.com/modelcontextprotocol/servers){target="_blank"} |
| **Azure MCP** | Serveur MCP Azure officiel | [🔗 Azure MCP](https://github.com/Azure/azure-mcp){target="_blank"} |

### 🏛️ Gouvernance IA

| Sujet | Description | Lien |
|-------|-------------|------|
| **Content Safety** | Filtrer le contenu nuisible | [🔗 Content Safety](https://learn.microsoft.com/fr-fr/azure/ai-services/content-safety/){target="_blank"} |
| **Prompt Shields** | Bloquer l'injection de prompt | [🔗 Prompt Shields](https://learn.microsoft.com/fr-fr/azure/ai-services/content-safety/concepts/prompt-shields){target="_blank"} |
| **Tableau RAI** | Surveiller équité & fiabilité | [🔗 Tableau RAI](https://learn.microsoft.com/fr-fr/azure/machine-learning/concept-responsible-ai-dashboard){target="_blank"} |

### ☁️ Patterns Architecture

| Sujet | Description | Lien |
|-------|-------------|------|
| **IA sur Azure** | Architectures de référence | [🔗 Architecture IA](https://learn.microsoft.com/fr-fr/azure/architecture/ai-ml/){target="_blank"} |
| **Pattern RAG** | Bonnes pratiques RAG | [🔗 Guide RAG](https://learn.microsoft.com/fr-fr/azure/architecture/ai-ml/guide/rag/rag-solution-design-and-evaluation-guide){target="_blank"} |
| **Chat E2E** | Baseline chat entreprise | [🔗 Baseline Chat](https://learn.microsoft.com/fr-fr/azure/architecture/ai-ml/architecture/baseline-openai-e2e-chat){target="_blank"} |

---

### 📜 Instructions Personnalisées Copilot

Créez `.github/copilot-instructions.md` :

```markdown
# Helpdesk Ops Assistant - Instructions Copilot

## Contexte Projet
Projet Microsoft Agent Framework pour helpdesk IT avec orchestration multi-agent.

## Stack Technique
- Framework : Microsoft Agent Framework (package agent-framework)
- LLM : Azure OpenAI GPT-4o via AzureOpenAIChatClient
- Auth : DefaultAzureCredential (jamais de clés en dur)
- Async : Toutes les opérations utilisent async/await

## Patterns Code
- Utiliser @ai_function pour les outils
- Utiliser Pydantic avec response_format= pour sortie structurée
- Encapsuler les opérations dans des spans OpenTelemetry

## Patterns Workflow
- Simple : agent.run() direct
- Group Chat : GroupChatBuilder pour collaboration
- Handoff : HandoffBuilder pour routage
```

---

### 🐛 Trouvé un Problème ?

<div class="task" data-title="Aidez-nous à Améliorer">

> - 🐛 **Bug** : [Ouvrir une Issue](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[BUG]%20)
> - 💡 **Fonctionnalité** : [Demander Feature](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[FEATURE]%20)
> - 💬 **Questions** : [Discussions](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions)

</div>

---

### 🚀 Prochaines Étapes

1. Ajouter plus d'agents spécialisés pour votre cas d'usage
2. Implémenter la gestion d'erreurs production
3. Configurer CI/CD pour le déploiement agents
4. Configurer l'autoscaling pour l'hébergement Azure Functions

---

> 🌍 **[← Partie 3 : Prêt pour la production](./part3-production.fr.md)** | **[🏠 Accueil Atelier](./index.fr.md)**

<div class="info" data-title="🎉 Atelier terminé !">

> **Merci d'avoir suivi cet atelier !**
> 
> Vous avez appris à créer des agents IA prêts pour la production avec Microsoft Agent Framework sur Azure.
> 
> Partagez votre expérience sur les réseaux sociaux ! 🚀

</div>
