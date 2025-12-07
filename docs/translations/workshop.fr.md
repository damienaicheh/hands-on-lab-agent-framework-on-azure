---
published: true
type: workshop
title: Atelier Pratique - Agent Framework sur Azure
short_title: Agent Framework sur Azure
description: Construisez un Assistant Helpdesk complet avec Microsoft Agent Framework sur Azure - de l'agent simple à l'orchestration multi-agents avec serveurs MCP, AI Search et Redis.
level: intermediate
navigation_numbering: false
authors:
  - Olivier Mertens
  - Damien Aicheh
contacts:
  - "@olmertens"
  - "@damienaicheh"
duration_minutes: 300
tags: microsoft foundry, agent framework, ai search, managed redis, mcp, group chat, orchestration, observabilité, évaluation
navigation_levels: 3
banner_url: ../assets/banner.jpg
audience: développeurs, architectes, ingénieurs IA
sections_title:
  - Introduction
  - Prérequis
  - Déployer l'Infrastructure
  - Module 1 - Agent Simple
  - Module 2 - Analyste de Complexité
  - Module 3 - Outils Fonctionnels
  - Module 4 - Intégration de Connaissances
  - Module 5 - Workflow Group Chat
  - Module 6 - Orchestration
  - Module 7 - Observabilité
  - Module 8 - Évaluation
  - Module 9 - Intégration Redis
  - Conclusion
---

# Assistant Helpdesk Ops - Agent Framework sur Azure

Bienvenue dans cet atelier pratique ! Vous allez construire un **mini-helpdesk propulsé par des agents IA** qui traite les tickets internes en utilisant :

- 🔍 **Azure AI Search** pour les connaissances FAQ de l'entreprise
- 🔧 **Serveurs MCP** pour la gestion des tickets GitHub et la documentation Microsoft Learn
- 🤖 **Orchestration multi-agents** avec Microsoft Agent Framework
- 📊 **Observabilité** avec OpenTelemetry et Azure AI Foundry

## 🎯 Scénario : Assistant Helpdesk Ops

Vous allez construire un système helpdesk complet avec plusieurs agents spécialisés :

| Agent | Rôle | Outils/Intégrations |
|-------|------|---------------------|
| **Orchestrateur** | Route les requêtes, choisit le workflow (Solo vs Group Chat) | Contrôle du workflow |
| **Analyste de Complexité** | Analyse les tickets, produit une sortie structurée, suggère une stratégie | Outils fonctionnels |
| **Agent Learn** | Interroge la documentation Microsoft Learn | Serveur MCP mslearn |
| **Agent GitHub** | Crée/gère les issues GitHub, labels, commentaires | Serveur MCP github |

## 📚 Modules de l'Atelier

| Module | Sujet | Durée |
|--------|-------|-------|
| 1 | Créer un Agent Simple | 20 min |
| 2 | Agent Analyste de Complexité | 25 min |
| 3 | Outils Fonctionnels | 30 min |
| 4 | Intégration de Connaissances (Foundry IQ) | 30 min |
| 5 | Workflow Group Chat | 35 min |
| 6 | Orchestration Avancée | 30 min |
| 7 | Observabilité | 25 min |
| 8 | Évaluation | 30 min |
| 9 | Intégration Redis | 25 min |

---

## Prérequis

### 🖥️ Environnement de Développement Local

Avant de commencer cet atelier, assurez-vous d'avoir les outils suivants installés sur votre machine :

#### Outils Requis

| Outil | Description | Lien d'Installation |
|-------|-------------|---------------------|
| **Azure CLI** | Interface en ligne de commande pour Azure | [Installer Azure CLI](https://learn.microsoft.com/fr-fr/cli/azure/install-azure-cli) |
| **Terraform** | Outil d'Infrastructure as Code | [Installer Terraform sur Azure](https://learn.microsoft.com/fr-fr/azure/developer/terraform/quickstart-configure) |
| **Git** | Système de contrôle de version | [Installer Git](https://learn.microsoft.com/fr-fr/devops/develop/git/install-and-set-up-git) |
| **Visual Studio Code** | Éditeur de code | [Télécharger VS Code](https://code.visualstudio.com/download) |
| **Python 3.11+** | Runtime Python | [Télécharger Python](https://www.python.org/downloads/) |

<div class="tip" data-title="Installation Windows">

> Vous pouvez installer ces outils avec `winget` dans PowerShell :
> ```powershell
> winget install -e --id Microsoft.AzureCLI
> winget install -e --id Hashicorp.Terraform
> winget install -e --id Git.Git
> winget install -e --id Microsoft.VisualStudioCode
> winget install -e --id Python.Python.3.11
> ```

</div>

### 🧩 Extensions Visual Studio Code

Installez les extensions suivantes dans Visual Studio Code :

#### Extensions Requises

| Extension | ID | Objectif |
|-----------|-----|----------|
| **GitHub Copilot** | `GitHub.copilot` | Codage assisté par IA |
| **GitHub Copilot Chat** | `GitHub.copilot-chat` | Chat IA interactif |
| **HashiCorp Terraform** | `HashiCorp.terraform` | Syntaxe Terraform & IntelliSense |
| **Azure Account** | `ms-vscode.azure-account` | Intégration connexion Azure |
| **Azure Tools** | `ms-vscode.vscode-node-azure-pack` | Outils de développement Azure |

#### Extensions Recommandées pour le Développement IA

| Extension | ID | Objectif |
|-----------|-----|----------|
| **AI Toolkit** | `ms-windows-ai-studio.windows-ai-studio` | Développement & test de modèles IA |
| **Azure MCP Server** | `ms-azuretools.azure-mcp` | Serveur Azure Model Context Protocol |
| **Azure Learn MCP** | `ms-azuretools.vscode-azure-github-copilot` | Documentation Azure & bonnes pratiques |
| **Python** | `ms-python.python` | Support du langage Python |
| **Jupyter** | `ms-toolsai.jupyter` | Support des notebooks Jupyter |
| **Pylance** | `ms-python.vscode-pylance` | IntelliSense Python |

<div class="hint" data-title="🤖 Maximisez Copilot pour cet Atelier">

> **Configurez Copilot pour le développement Agent Framework :**
>
> 1. **Créez des instructions workspace** - Ajoutez `.github/copilot-instructions.md` :
>    ```markdown
>    Ce projet utilise Microsoft Agent Framework pour les agents IA.
>    - Utilisez Azure OpenAI avec DefaultAzureCredential
>    - Utilisez les patterns async/await pour toutes les opérations d'agent
>    - Utilisez Pydantic pour la sortie structurée
>    - Utilisez le décorateur @ai_function pour les outils
>    - Suivez les patterns OpenTelemetry pour l'observabilité
>    ```
>
> 2. **Utilisez le bon mode Copilot pour chaque tâche** :
>    - **Ask** : Questions sur les concepts Agent Framework
>    - **Edit** : Modifier le code d'agent existant
>    - **Agent** : Construire de nouveaux agents de manière autonome
>    - **Plan** : Concevoir des architectures multi-agents
>
> 3. **Utilisez les serveurs MCP** : Installez les extensions Azure MCP et GitHub MCP pour des capacités améliorées

</div>

<div class="task" data-title="Installer les Extensions">

> Installez les extensions via la ligne de commande :
> ```powershell
> # Extensions Requises
> code --install-extension GitHub.copilot
> code --install-extension GitHub.copilot-chat
> code --install-extension HashiCorp.terraform
> code --install-extension ms-vscode.azure-account
> code --install-extension ms-vscode.vscode-node-azure-pack
> 
> # Extensions IA Recommandées
> code --install-extension ms-windows-ai-studio.windows-ai-studio
> code --install-extension ms-azuretools.azure-mcp
> code --install-extension ms-azuretools.vscode-azure-github-copilot
> code --install-extension ms-python.python
> code --install-extension ms-toolsai.jupyter
> code --install-extension ms-python.vscode-pylance
> ```

</div>

### 🐍 Configuration de l'Environnement Python

Créez et activez un environnement virtuel Python :

```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer (Windows)
.venv\Scripts\activate

# Activer (Linux/Mac)
source .venv/bin/activate

# Installer Agent Framework avec tous les extras
pip install agent-framework[azure,redis,viz] --pre
```

<div class="hint" data-title="Problèmes d'Environnement Virtuel ?">

> **Problèmes courants et solutions :**
>
> 1. **"python" non reconnu** : Utilisez `python3` au lieu de `python` sur Linux/Mac
> 2. **L'activation échoue sur Windows PowerShell** : Exécutez d'abord `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`
> 3. **pip install échoue** : Essayez `python -m pip install --upgrade pip` puis réessayez
> 4. **Mauvaise version Python** : Vérifiez avec `python --version` (besoin de 3.11+)
>
> Pour vérifier que l'activation a fonctionné, votre prompt terminal devrait afficher le préfixe `(.venv)`.

</div>

<div class="hint" data-title="☁️ Utilisez Azure MCP pour Vérifier les Variables d'Environnement">

> **Demandez à Copilot avec Azure MCP de vérifier votre configuration Azure :**
>
> 1. **Vérifiez la connexion Azure CLI** :
>    ```
>    Sur quel compte Azure suis-je actuellement connecté ?
>    Montrez l'ID du tenant et le nom de l'abonnement.
>    ```
>
> 2. **Vérifiez les variables d'environnement requises** :
>    ```
>    Vérifiez si AZURE_OPENAI_ENDPOINT et AZURE_AI_SEARCH_ENDPOINT 
>    sont définis dans mon environnement et s'ils pointent vers des ressources Azure valides
>    ```
>
> 3. **Validez l'accès Azure OpenAI** :
>    ```
>    Mon identité Azure actuelle peut-elle accéder à la ressource Azure OpenAI 
>    à mon AZURE_OPENAI_ENDPOINT ? Quels rôles ai-je assignés ?
>    ```
>
> Cela détecte les problèmes de configuration avant d'exécuter du code !

</div>

### ☁️ Prérequis Azure

- Un abonnement Azure actif avec le rôle **Owner** ou **Contributor**
- Quota suffisant pour les services suivants :
  - Azure AI Foundry
  - Azure AI Search
  - Azure Managed Redis
  - Modèles Azure OpenAI (GPT-4o recommandé)

### ✅ Vérification

Après l'installation, vérifiez votre configuration en exécutant ces commandes :

```powershell
# Vérifier Azure CLI
az --version

# Vérifier Terraform
terraform --version

# Vérifier Python
python --version

# Vérifier Agent Framework
pip show agent-framework

# Se connecter à Azure (remplacez avec votre tenant)
az login --tenant <votre-tenant-id-ou-domaine.com>

# Afficher les détails de votre compte
az account show
```

<div class="warning" data-title="Important">

> Assurez-vous d'être connecté au bon abonnement Azure avant de procéder au déploiement de l'infrastructure.

</div>

<div class="warning" data-title="🆘 Besoin d'Aide ?">

> **Bloqué pendant la configuration ? Voici comment obtenir de l'aide :**
>
> - 📖 Consultez le [Guide de Dépannage](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/wiki/Troubleshooting)
> - 🐛 [Signaler un problème de configuration](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[SETUP]%20&labels=setup,help-wanted)
> - 💬 [Poser une question dans les Discussions](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions/categories/q-a)
>
> Lors du signalement de problèmes, veuillez inclure :
> - Votre OS et version Python
> - Le message d'erreur exact
> - À quelle étape vous étiez

</div>

---

## Déployer l'Infrastructure

D'abord, vous devez initialiser l'infrastructure Terraform en exécutant les commandes suivantes.

### Option 1 : Environnement Local

Connectez-vous à votre compte Azure :

```bash
az login --tenant <votre-tenant-id ou domaine.com>
```

### Option 2 : GitHub Codespace

Vous devrez peut-être spécifier le paramètre `--use-device-code` pour faciliter le processus d'authentification Azure CLI :

```bash
az login --use-device-code --tenant <votre-tenant-id ou domaine.com>

# Afficher les détails de votre compte
az account show
```

### Définir les Variables d'Environnement

Définissez la variable d'environnement `ARM_SUBSCRIPTION_ID` avec votre ID d'abonnement Azure :

```bash
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)
```

### Déployer avec Terraform

Naviguez vers le répertoire `infra` et initialisez Terraform :

```bash
cd infra && terraform init
```

Puis exécutez la commande suivante pour déployer l'infrastructure :

```bash
# Appliquer le déploiement directement
terraform apply -auto-approve
```

<div class="hint" data-title="Problèmes de Déploiement Terraform ?">

> **Problèmes de déploiement courants :**
>
> 1. **"Provider not found"** : Exécutez `terraform init -upgrade` pour rafraîchir les providers
> 2. **Quota dépassé** : Vérifiez Portail Azure → Abonnements → Usage + quotas
> 3. **Région non disponible** : Essayez de changer la variable `location` dans `variables.tf`
> 4. **Erreur d'authentification** : Assurez-vous que `az login` a réussi et exécutez `az account show` pour vérifier
> 5. **Erreur de verrouillage d'état** : Si le déploiement a été interrompu, exécutez `terraform force-unlock <LOCK_ID>`
>
> **Pour voir les logs détaillés :**
> ```bash
> export TF_LOG=DEBUG
> terraform apply
> ```

</div>

<div class="info" data-title="Temps de Déploiement">

> Le déploiement de l'infrastructure peut prendre 15-30 minutes selon la région Azure et la disponibilité des ressources.

</div>

---

## Module 1 — Créer un Agent Simple

Dans ce module, vous allez découvrir Microsoft Agent Framework et créer votre premier agent.

### 🎯 Objectifs d'Apprentissage

- Comprendre les concepts fondamentaux d'Agent Framework
- Créer un agent basique avec Azure AI Foundry
- Exécuter l'agent et gérer les réponses

### 📖 Concepts Clés

**Agent Framework** est le framework unifié de Microsoft pour construire des agents IA qui supporte :

- Plusieurs fournisseurs LLM (Azure OpenAI, OpenAI, Anthropic, etc.)
- Appel d'outils et exécution de fonctions
- Orchestration multi-agents
- Observabilité avec OpenTelemetry

<div class="hint" data-title="🤖 Utilisez GitHub Copilot pour Vous Aider !">

> **Copilot peut vous aider à comprendre Agent Framework :**
>
> 1. **Demandez à Copilot Chat** (`Ctrl+Shift+I`) : `@workspace Expliquez ce que fait AzureOpenAIChatClient et comment le configurer`
> 2. **Suggestions inline** : Commencez à taper `client = Azure` et laissez Copilot compléter
> 3. **Obtenir la documentation** : Sélectionnez du code et demandez `/explain` pour comprendre chaque paramètre
>
> **Astuce** : Créez un fichier d'instructions personnalisées `.github/copilot-instructions.md` :
> ```markdown
> Nous utilisons Microsoft Agent Framework avec Azure OpenAI.
> Toujours utiliser DefaultAzureCredential pour l'authentification.
> Utiliser les patterns async/await pour toutes les opérations d'agent.
> ```

</div>

### 💻 Créez Votre Premier Agent

Créez un nouveau fichier `src/module1_simple_agent.py` :

```python
"""Module 1: Agent Simple - Agent de bienvenue helpdesk basique."""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Créer et exécuter un agent helpdesk simple."""
    
    # Créer le client Azure OpenAI avec Azure Identity
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Créer l'agent avec des instructions
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="""Vous êtes un assistant helpdesk IT sympathique.
        
        Votre rôle est de :
        - Accueillir chaleureusement les utilisateurs
        - Comprendre leurs problèmes IT
        - Fournir des conseils initiaux
        - Escalader les problèmes complexes de manière appropriée
        
        Soyez toujours professionnel et empathique.""",
    )
    
    # Exécuter l'agent avec une requête simple
    query = "Bonjour, mon laptop ne se connecte pas au VPN et j'ai une réunion importante dans 30 minutes !"
    print(f"Utilisateur : {query}")
    
    result = await agent.run(query)
    print(f"Agent : {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 🚀 Exécutez Votre Agent

```bash
python src/module1_simple_agent.py
```

<div class="hint" data-title="Erreurs d'Authentification ?">

> **Dépannage Azure Identity :**
>
> 1. **DefaultAzureCredential échoue** : Assurez-vous d'être connecté avec `az login`
> 2. **Endpoint non trouvé** : Vérifiez que `AZURE_OPENAI_ENDPOINT` est correctement défini (doit commencer par `https://`)
> 3. **Déploiement non trouvé** : Vérifiez que le nom du déploiement correspond exactement dans Azure AI Foundry
> 4. **403 Forbidden** : Votre compte Azure n'a peut-être pas accès à la ressource OpenAI
>
> **Déboguer la chaîne de credentials :**
> ```python
> from azure.identity import DefaultAzureCredential
> credential = DefaultAzureCredential(logging_enable=True)
> token = credential.get_token("https://cognitiveservices.azure.com/.default")
> print(f"Token acquis : {token.token[:20]}...")
> ```

</div>

<div class="task" data-title="Exercice">

> Essayez de modifier les instructions de l'agent pour être plus spécifique sur les étapes de dépannage VPN. Qu'est-ce qui change dans la réponse ?

</div>

---

## Conclusion

Félicitations ! 🎉 Vous avez construit un **Assistant Helpdesk Ops** complet avec :

### ✅ Ce Que Vous Avez Appris

| Module | Compétence |
|--------|------------|
| 1 | Créer des agents basiques avec Agent Framework |
| 2 | Sortie structurée avec les modèles Pydantic |
| 3 | Outils fonctionnels et appel d'outils |
| 4 | Intégration de connaissances avec Azure AI Search |
| 5 | Workflows Group Chat multi-agents |
| 6 | Orchestration avancée avec Handoff |
| 7 | Observabilité avec OpenTelemetry |
| 8 | Évaluation et test d'agents |
| 9 | Mémoire persistante avec Redis |

### 📚 Ressources Supplémentaires

#### Agent Framework & Apprentissage

- [Microsoft Agent Framework - GitHub](https://github.com/microsoft/agent-framework)
- [Agents IA pour Débutants - Module Microsoft Agent Framework](https://microsoft.github.io/ai-agents-for-beginners/14-microsoft-agent-framework/)
- [Exemples de Workflows Agent Framework](https://github.com/microsoft/agent-framework/blob/main/python/samples/getting_started/workflows/README.md)
- [Vue d'ensemble des Orchestrations](https://learn.microsoft.com/fr-fr/agent-framework/user-guide/workflows/orchestrations/overview)

#### Azure AI & Observabilité

- [Azure AI Foundry](https://learn.microsoft.com/fr-fr/azure/ai-studio/)
- [Tracer les Agents avec Azure AI SDK](https://learn.microsoft.com/fr-fr/azure/ai-foundry/how-to/develop/trace-agents-sdk?view=foundry-classic)
- [Model Context Protocol](https://modelcontextprotocol.io/)

#### Inspiration Workshop

- [GitHub Copilot Hands-on Lab (Exemple MOAW)](https://moaw.dev/workshop/gh:Philess/GHCopilotHoL/main/docs/?step=0)

### 🐛 Trouvé un Problème ? Une Demande de Fonctionnalité ?

Nous voulons améliorer cet atelier ! Vos retours sont précieux.

<div class="task" data-title="Aidez-Nous à Améliorer">

> **Signalez des problèmes ou suggérez des améliorations :**
>
> - 🐛 **Bug ou Erreur** : [Ouvrir un Issue](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=bug_report.md&title=[BUG]%20)
> - 💡 **Demande de Fonctionnalité** : [Demander une Fonctionnalité](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?template=feature_request.md&title=[FEATURE]%20)
> - 📝 **Documentation** : [Suggérer une Amélioration Doc](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/issues/new?title=[DOCS]%20)
> - 💬 **Questions** : [Démarrer une Discussion](https://github.com/yourorg/hands-on-lab-agent-framework-on-azure/discussions)

</div>

<div class="info" data-title="Feedback">

> Nous aimerions avoir vos retours ! Veuillez ouvrir un issue ou une discussion sur le dépôt de l'atelier.

</div>
