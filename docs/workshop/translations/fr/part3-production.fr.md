---
published: true
type: workshop
title: "Partie 3 : Prêt pour la production"
short_title: "Production"
description: Orchestration, supervision et évaluation pour un déploiement en production
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 60
tags: orchestration, observabilité, opentelemetry, évaluation, production, handoff
banner_url: ../../assets/banner.jpg
navigation_levels: 1
sections_title:
  - Introduction
  - 🏠 Navigation
  - Code des Parties 1-2
  - Module 6 - Orchestration
  - Module 7 - Supervision
  - Module 8 - Évaluation
  - Résumé
---

# Partie 3 : Prêt pour la production

![Banner Workshop](../../assets/banner.jpg)

> 🌍 **[← Partie 2 : Gestion des connaissances](./part2-knowledge.fr.md)** | **[Partie 4 : Pour aller plus loin →](./part4-advanced.fr.md)**

---

## 🏠 Navigation

<div class="tip" data-title="Navigation de l'atelier">

> **📚 Toutes les parties :**
> - [🏠 Accueil de l'atelier](./index.fr.md)
> - [Partie 1 : Les fondamentaux](./part1-basics.fr.md)
> - [Partie 2 : Gestion des connaissances](./part2-knowledge.fr.md)
> - [Partie 3 : Prêt pour la production](./part3-production.fr.md) *(actuel)*
> - [Partie 4 : Pour aller plus loin](./part4-advanced.fr.md)
>
> **🌍 Cette page en d'autres langues :**
> - [🇬🇧 English](/workshop/part3-production.md)
> - [🇪🇸 Español](/workshop/translations/es/part3-production.es.md)
> - [🇮🇳 हिन्दी](/workshop/translations/hi/part3-production.hi.md)

</div>

---

## 📦 Code des Parties 1 et 2

Avant de commencer, assurez-vous de disposer du code des parties précédentes :

<details>
<summary>📁 Structure du projet (cliquez pour afficher)</summary>

```text
helpdesk-agent/
├── .env
├── requirements.txt
└── src/
    ├── module1_simple_agent.py    # Partie 1: Agent simple
    ├── module2_structured.py      # Partie 1: Sortie structurée
    ├── module3_tools.py           # Partie 1: Outils fonction
    ├── module4_rag.py             # Partie 2: AI Search RAG
    └── module5_group_chat.py      # Partie 2: Group Chat + MCP
```

</details>

<details>
<summary>🔧 Composants Clés de la Partie 2 (cliquez pour développer)</summary>

```python
# Outil de recherche RAG du Module 4
from azure.search.documents import SearchClient
from azure.identity import DefaultAzureCredential

search_client = SearchClient(
    endpoint=os.getenv("AZURE_SEARCH_ENDPOINT"),
    index_name="helpdesk-faq",
    credential=DefaultAzureCredential(),
)

@ai_function
def search_knowledge_base(query: str) -> list[dict]:
    """Recherche dans la base de connaissances FAQ."""
    results = search_client.search(
        search_text=query,
        query_type="semantic",
        top=5,
    )
    return [{"title": r["title"], "content": r["content"]} for r in results]

# Configuration client MCP du Module 5
from agent_framework.mcp import MCPStdioClient

async def get_mcp_tools() -> list:
    """Récupère les outils des serveurs MCP."""
    mslearn_client = await MCPStdioClient.create(
        command="npx",
        args=["-y", "@anthropic/mcp-mslearn"],
    )
    return mslearn_client.tools
```

</details>

<details>
<summary>📋 Variables d'Environnement Nécessaires (cliquez pour développer)</summary>

```bash
# Fichier .env - assurez-vous que tout est configuré
AZURE_OPENAI_ENDPOINT=https://votre-ressource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
AZURE_SEARCH_ENDPOINT=https://votre-search.search.windows.net
AZURE_SEARCH_INDEX_NAME=helpdesk-faq
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Nouveau pour Partie 3:
APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey=xxx;...
```

</details>

<div class="info" data-title="Parties 1-2 non complétées ?">

> Complétez d'abord [Partie 1](part1-basics.fr.md) et [Partie 2](part2-knowledge.fr.md), ou utilisez le code ci-dessus.

</div>

---

| Module | Sujet | Ce que vous construisez |
|--------|-------|-------------------------|
| 6 | **Orchestration** | Workflow Handoff avec spécialistes |
| 7 | **Observabilité** | Tracing OpenTelemetry + Azure Monitor |
| 8 | **Évaluation** | Pipeline de tests qualité |

---

## Module 6 — Orchestration Avancée

Construisez un orchestrateur qui coordonne plusieurs agents spécialisés.

### 📚 Concept : Pattern Handoff

Imaginez un appel au helpdesk : une **standardiste** (Orchestrateur) répond, comprend votre problème, puis vous **transfère** au bon spécialiste.

```text
                                           ┌──────────────────────┐
                                     ┌────▶│ ⚡ Résolveur Rapide   │
                                     │     └──────────────────────┘
                                     │
👤 User ───▶ 🎯 Orchestrateur ───▶ 🔍 Analyste ──┼────▶ 📝 Créateur Ticket
                                     │
                                     │     ┌──────────────────────┐
                                     └────▶│ 🚨 Escalade          │
                                           └──────────────────────┘
             
       requête       analyse         route par complexité:
                                        • simple  → Résolveur Rapide
                                        • moyen   → Créateur Ticket
                                        • complexe → Escalade
```

| Concept | Description |
|---------|-------------|
| **Coordinateur** | L'agent "chef" qui route les requêtes |
| **Spécialiste** | Agents experts pour des tâches spécifiques |
| **Handoff** | Transfert de conversation entre agents |
| **Retour** | Le spécialiste rend le contrôle au coordinateur |

### 🧠 Pseudo-code

```
ALGORITHME : Orchestration Helpdesk

1. CRÉER SPÉCIALISTES :
   - ComplexityAnalyst → détermine la difficulté
   - QuickResolver → résout les problèmes simples
   - TicketCreator → crée des tickets formels
   - EscalationAgent → escalade les cas critiques

2. CRÉER ORCHESTRATEUR comme coordinateur

3. CONFIGURER ROUTES HANDOFF :
   - Orchestrateur → [Analyste]
   - Analyste → [Résolveur, Créateur, Escalade]
   - Tous les spécialistes retournent à l'Orchestrateur

4. TRAITEMENT : User → Orchestrateur → Analyste → Spécialiste → Réponse
```

### 🔨 Exercice

Créez `src/module6_orchestration.py`.

<details>
<summary>💡 Indice : Création Agent Spécialiste</summary>

```python
quick_resolver = ChatAgent(
    chat_client=client,
    name="QuickResolver",
    instructions="""Résous les problèmes IT simples directement.
    Fournis des solutions étape par étape pour :
    - Réinitialisation mot de passe
    - Vidage cache navigateur
    - Dépannage réseau basique""",
)
```

</details>

<details>
<summary>💡 Indice : Pattern HandoffBuilder</summary>

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
<summary>💡 Indice : Streaming Événements</summary>

```python
async for event in workflow.run_stream(ticket):
    if hasattr(event, 'text') and event.text:
        agent_name = getattr(event, 'agent_name', 'System')
        print(f"[{agent_name}]: {event.text}")
```

</details>

### ✅ Solution

<details>
<summary>📄 Code Complet Module 6</summary>

```python
"""Module 6 : Orchestration Avancée - Workflow Handoff."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.workflows import HandoffBuilder


async def create_agents(client: AzureOpenAIChatClient) -> dict:
    """Crée tous les agents spécialistes."""
    
    complexity_analyst = ChatAgent(
        chat_client=client,
        name="ComplexityAnalyst",
        instructions="""Analyse la complexité du ticket.
        Output : Complexité (simple|moyen|complexe), Handler, Raisonnement""",
    )
    
    quick_resolver = ChatAgent(
        chat_client=client,
        name="QuickResolver",
        instructions="""Résous les problèmes IT simples.
        Fournis des solutions étape par étape.""",
    )
    
    ticket_creator = ChatAgent(
        chat_client=client,
        name="TicketCreator",
        instructions="""Crée des tickets de support détaillés.
        Format : Titre, Priorité, Catégorie, Description""",
    )
    
    escalation_agent = ChatAgent(
        chat_client=client,
        name="EscalationAgent",
        instructions="""Gère les escalades complexes.
        Documente, identifie l'équipe, crée un rapport.""",
    )
    
    return {
        "analyst": complexity_analyst,
        "resolver": quick_resolver,
        "creator": ticket_creator,
        "escalation": escalation_agent,
    }


async def main() -> None:
    """Exécute le workflow orchestré."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agents = await create_agents(client)
    
    orchestrator = ChatAgent(
        chat_client=client,
        name="Orchestrator",
        instructions="""Tu es l'orchestrateur helpdesk principal.
        Route vers ComplexityAnalyst d'abord, puis selon l'analyse :
        - Simple → QuickResolver
        - Moyen → TicketCreator
        - Complexe → EscalationAgent""",
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
        "J'ai oublié mon mot de passe",
        "Le VPN se déconnecte toutes les 5 minutes",
        "Tout le département ne peut pas accéder au CRM - appels clients dans 1h",
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

<div class="task" data-title="🎯 Défi">

> Ajoutez un 5ème spécialiste : `FeedbackAgent` qui demande une évaluation de satisfaction. Modifiez les routes pour que les spécialistes puissent transférer vers FeedbackAgent.

</div>

---

## Module 7 — Observabilité

Activez le tracing et monitoring avec OpenTelemetry et Microsoft Foundry.

### 📚 Concept : Tracing Distribué

| Sans Observabilité | Avec Observabilité |
|--------------------|-------------------|
| "L'agent est lent" | "L'appel outil a pris 3.2s à 14:32:05" |
| "La réponse était fausse" | "Le modèle a reçu 4500 tokens, pas de contexte" |
| Des heures à chercher dans les logs | Un clic pour voir la trace exacte |

**Concepts OpenTelemetry :**

| Terme | Description |
|-------|-------------|
| **Trace** | Voyage complet d'une requête |
| **Span** | Opération unique (hiérarchie imbriquée) |
| **Attributs** | Métadonnées clé-valeur sur les spans |
| **Exporter** | Envoie les données vers Azure Monitor |

### 🧠 Pseudo-code

```
ALGORITHME : Ajouter l'Observabilité

1. CONFIGURER EXPORTER au démarrage :
   - configure_azure_monitor(connection_string)

2. SETUP OBSERVABILITÉ FRAMEWORK :
   - setup_observability(service_name, enable_tracing=True)

3. OBTENIR TRACER :
   - tracer = trace.get_tracer(__name__)

4. ENCAPSULER OPÉRATIONS DANS SPANS :
   - with tracer.start_as_current_span("operation"):
   -     span.set_attribute("key", value)
   -     # Code automatiquement chronométré
```

### 🔨 Exercice

Créez `src/module7_observability.py`.

<details>
<summary>💡 Indice : Configuration Azure Monitor</summary>

```python
from azure.monitor.opentelemetry import configure_azure_monitor

configure_azure_monitor(
    connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"),
)
```

</details>

<details>
<summary>💡 Indice : Observabilité Framework</summary>

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
<summary>💡 Indice : Création Spans</summary>

```python
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

with tracer.start_as_current_span("helpdesk_session") as span:
    span.set_attribute("user.id", "demo_user")
    # Les spans enfants sont automatiquement imbriqués
    with tracer.start_as_current_span("agent_query") as query_span:
        query_span.set_attribute("query.text", query)
        result = await agent.run(query)
        query_span.set_attribute("response.length", len(result.text))
```

</details>

### ✅ Solution

<details>
<summary>📄 Code Complet Module 7</summary>

```python
"""Module 7 : Observabilité - Tracing avec OpenTelemetry."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework import ChatAgent, ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.observability import setup_observability
from opentelemetry import trace

# Configurer AVANT de créer les agents
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
    """Vérifie le statut d'un système."""
    return {"system": system_name, "status": "operational"}


async def main() -> None:
    """Exécute l'agent avec observabilité complète."""
    
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
            instructions="Tu es un assistant avec monitoring.",
            tools=[check_system_status],
        )
        
        queries = ["Vérifie le système email", "Vérifie le VPN"]
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

**Voir les traces dans :**
- **Microsoft Foundry** → Votre Projet → Tracing
- **Application Insights** → Recherche de transactions

<div class="hint" data-title="Traces Non Visibles ?">

> - Attendez 2-3 minutes pour le délai d'ingestion
> - Vérifiez que `APPLICATIONINSIGHTS_CONNECTION_STRING` est correct
> - Assurez-vous que `configure_azure_monitor()` est appelé AVANT de créer les agents

</div>

<div class="task" data-title="🎯 Défi">

> Ajoutez une métrique personnalisée pour suivre l'utilisation des tokens par requête. Créez un span de gestion d'erreur qui capture les exceptions.

</div>

---

## Module 8 — Évaluation

Implémentez l'évaluation de la qualité et performance de vos agents.

### 📚 Concept : Pourquoi Évaluer ?

| Sans Évaluation | Avec Évaluation |
|-----------------|-----------------|
| "L'agent semble bon" | "94% de précision sur la classification" |
| "Les utilisateurs se plaignent parfois" | "15% d'échec sur les tickets critiques" |
| Deviner les améliorations | Optimisation basée sur les données |

**Pipeline d'Évaluation :**

```
DATASET TEST → AGENT → MÉTRIQUES
  [entrées +    [run]   [précision,
   attendus]             taux réussite]
```

| Type Éval | Description | Cas d'Usage |
|-----------|-------------|-------------|
| **Exact Match** | La sortie correspond exactement | JSON structuré |
| **LLM-as-Judge** | Un modèle note la réponse | Texte libre |
| **Éval Humaine** | Des personnes notent la qualité | Validation production |

### 🧠 Pseudo-code

```
ALGORITHME : Évaluer la Qualité Agent

1. DÉFINIR DATASET TEST :
   - input + expected_category + expected_severity

2. BOUCLE SUR LES CAS TEST :
   POUR chaque test_case :
       - Envoyer l'input à l'agent
       - Parser la réponse JSON
       - Comparer aux valeurs attendues
       - Enregistrer pass/fail

3. CALCULER MÉTRIQUES :
   - pass_rate = réussis / total
   - category_accuracy = corrects / total
   - severity_accuracy = corrects / total

4. RAPPORTER résultats et cas échoués
```

### 🔨 Exercice

Créez `src/module8_evaluation.py`.

<details>
<summary>💡 Indice : Dataset Test</summary>

```python
TEST_CASES = [
    {
        "input": "Je ne peux pas accéder à ma boîte mail",
        "expected_category": "access",
        "expected_severity": "medium",
    },
    {
        "input": "URGENT: La base de production est down!",
        "expected_category": "software",
        "expected_severity": "critical",
    },
]
```

</details>

<details>
<summary>💡 Indice : Logique de Comparaison</summary>

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
    results.append({"error": "JSON invalide", "overall_pass": False})
```

</details>

<details>
<summary>💡 Indice : Calcul Métriques</summary>

```python
total = len(results)
passed = sum(1 for r in results if r.get("overall_pass", False))
category_accuracy = sum(1 for r in results if r.get("category_correct", False)) / total
print(f"Taux Réussite: {passed / total:.1%}")
print(f"Précision Catégorie: {category_accuracy:.1%}")
```

</details>

### ✅ Solution

<details>
<summary>📄 Code Complet Module 8</summary>

```python
"""Module 8 : Évaluation - Tests qualité agent."""
import asyncio
import os
import json
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


TEST_CASES = [
    {"input": "Je ne peux pas accéder à ma boîte mail", "expected_category": "access", "expected_severity": "medium"},
    {"input": "URGENT: La base de production est down!", "expected_category": "software", "expected_severity": "critical"},
    {"input": "Comment configurer le transfert d'email?", "expected_category": "software", "expected_severity": "low"},
]


async def evaluate_agent() -> dict:
    """Exécute l'évaluation sur l'agent analyseur de tickets."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="TicketAnalyst",
        instructions="""Analyse les tickets IT et réponds en JSON :
        {"category": "network|hardware|software|access|other",
         "severity": "low|medium|high|critical",
         "summary": "description brève"}""",
    )
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"Test {i}/{len(TEST_CASES)}...")
        result = await agent.run(f"Analyse : {test_case['input']}")
        
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
            results.append({"input": test_case["input"], "error": "JSON invalide", "overall_pass": False})
    
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
    """Exécute l'évaluation et affiche les résultats."""
    print("🧪 Évaluation Agent en cours\n")
    metrics = await evaluate_agent()
    
    print(f"\n📊 Résultats")
    print(f"{'='*40}")
    print(f"Taux Réussite: {metrics['pass_rate']:.1%}")
    print(f"Précision Catégorie: {metrics['category_accuracy']:.1%}")
    print(f"Précision Sévérité: {metrics['severity_accuracy']:.1%}")
    
    print("\n📋 Détails:")
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

<div class="hint" data-title="Scores Faibles ?">

> - **Faible précision catégorie** : Ajoutez des exemples dans les instructions
> - **JSON incohérent** : Utilisez `response_format=VotreModèle`
> - **Debug tests échoués** : Affichez la réponse brute pour voir les problèmes

</div>

<div class="task" data-title="🎯 Défi">

> Ajoutez des métriques de timing pour suivre la latence des réponses. Implémentez LLM-as-judge pour évaluer la qualité au-delà du match exact.

</div>

---

## Résumé Partie 3

Vous avez construit des systèmes **production-ready** :

| Module | Réalisation |
|--------|-------------|
| **6** | ✅ Orchestration Handoff avec spécialistes |
| **7** | ✅ Tracing OpenTelemetry + Azure Monitor |
| **8** | ✅ Pipeline d'évaluation qualité |

**Patterns Clés Appris :**

```
┌─────────────────────────────────────────────┐
│       SYSTÈME AGENT PRODUCTION              │
├─────────────────────────────────────────────┤
│  📨 Requête → 🎯 Orchestrateur              │
│                    ↓                        │
│             [Route par complexité]          │
│                    ↓                        │
│  ⚡ Rapide │ 📝 Ticket │ 🚨 Escalade         │
│                    ↓                        │
│  📊 Traces → Azure Monitor                  │
│  🧪 Éval → Métriques Qualité                │
└─────────────────────────────────────────────┘
```

> 🌍 **[← Partie 2 : Intégration Connaissances](part2-knowledge.fr.md)** | **[Partie 4 : Avancé & Ressources →](part4-advanced.fr.md)**
