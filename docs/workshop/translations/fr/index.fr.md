---
published: true
type: workshop
title: "Atelier Agent Framework sur Azure"
short_title: "Agent Framework Lab"
description: Créez un assistant Helpdesk complet avec Microsoft Agent Framework sur Azure
level: intermediate
authors:
  - Olivier Mertens
contacts:
  - "@olivMertens"
duration_minutes: 180
tags: agent-framework, azure, ia, multi-agent, mcp, rag
banner_url: ../../assets/banner.jpg
navigation_levels: 2
sections_title:
  - Accueil
  - Présentation
  - Parties
  - Ressources
---

# 🤖 Atelier Agent Framework sur Azure

> **Bienvenue !** Dans cet atelier, vous allez créer un **assistant Helpdesk** complet avec Microsoft Agent Framework.

## 📋 Présentation de l'atelier

| Info | Détails |
|------|---------|
| **Durée** | Environ 3 heures |
| **Niveau** | Intermédiaire |
| **Prérequis** | Python, notions de base sur Azure |
| **Objectif** | Créer un système multi-agents avec RAG, MCP et observabilité |

## 🏗️ Architecture

```text
┌─────────────────────────────────────────────────────────────────────┐
│                           📥 ENTRÉE                                 │
│                    👤 Requête Utilisateur                           │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    🎯 COUCHE ORCHESTRATION                          │
│                       🧠 Orchestrateur                              │
└───────────┬──────────────────┼──────────────────┬───────────────────┘
            │                  │                  │
            ▼                  ▼                  ▼
       ┌──────────┐      ┌───────────┐      ┌────────────┐
       │⚡ Flux    │      │👥 Group   │      │🚨 Escalade │
       │  Simple  │      │   Chat    │      │            │
       └────┬─────┘      └─────┬─────┘      └────────────┘
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

## 📚 Parcours de l'atelier

L'atelier se compose de **4 parties** pour faciliter la navigation :

### 🔷 [Partie 1 : Les fondamentaux](./part1-basics.fr.md)
> Prérequis, déploiement de l'infrastructure et premiers modules

| Module | Contenu | Durée |
|--------|---------|-------|
| Mise en place | Prérequis et déploiement | 20 min |
| 1 | Agent simple avec streaming | 15 min |
| 2 | Réponses structurées (Pydantic) | 15 min |
| 3 | Outils personnalisés | 20 min |

### 🔷 [Partie 2 : Gestion des connaissances](./part2-knowledge.fr.md)
> RAG avec Azure AI Search et collaboration multi-agents

| Module | Contenu | Durée |
|--------|---------|-------|
| 4 | Intégration d'Azure AI Search | 25 min |
| 5 | Discussion de groupe avec MCP | 30 min |

### 🔷 [Partie 3 : Prêt pour la production](./part3-production.fr.md)
> Orchestration avancée, supervision et évaluation

| Module | Contenu | Durée |
|--------|---------|-------|
| 6 | Orchestration par transfert | 25 min |
| 7 | Supervision avec OpenTelemetry | 20 min |
| 8 | Évaluation et tests | 20 min |

### 🔷 [Partie 4 : Pour aller plus loin](./part4-advanced.fr.md)
> Persistance Redis, structure du projet et ressources

| Module | Contenu | Durée |
|--------|---------|-------|
| 9 | Intégration de Redis | 25 min |
| - | Conclusion et ressources | 10 min |

---

## 🚀 Accès rapide

<div class="info" data-title="Choisissez votre parcours">

> **🚀 Première visite ?** Commencez par [Partie 1 : Les fondamentaux](./part1-basics.fr.md)
>
> **🔍 Besoin d'un sujet précis ?** Accédez directement à :
> - [Prérequis et configuration](./part1-basics.fr.md#prérequis)
> - [Module 1 : Agent simple](./part1-basics.fr.md#module-1--agent-simple)
> - [Module 2 : Sortie structurée](./part1-basics.fr.md#module-2--sortie-structurée)
> - [Module 3 : Outils fonction](./part1-basics.fr.md#module-3--outils-fonction)
> - [Module 4 : AI Search / RAG](./part2-knowledge.fr.md#module-4--intégration-azure-ai-search)
> - [Module 5 : Group Chat](./part2-knowledge.fr.md#module-5--group-chat-multi-agent)
> - [Module 6 : Orchestration](./part3-production.fr.md#module-6--orchestration-avancée)
> - [Module 7 : Observabilité](./part3-production.fr.md#module-7--observabilité)
> - [Module 8 : Évaluation](./part3-production.fr.md#module-8--évaluation)
> - [Module 9 : Redis](./part4-advanced.fr.md#module-9--intégration-redis)
> - [Conclusion et ressources](./part4-advanced.fr.md#conclusion)

</div>

---

## 🌍 Autres langues

- 🇬🇧 [English](../../index.md)
- 🇫🇷 Français (version actuelle)
- 🇪🇸 [Español](../es/index.es.md)
- 🇮🇳 [हिन्दी](../hi/index.hi.md)

---

<div class="info" data-title="💡 Conseil">

> Chaque partie est indépendante : vous pouvez les suivre dans l'ordre ou passer directement aux modules qui vous intéressent.
>
> **Astuces Copilot** 🤖 : Repérez les sections dépliables contenant des conseils pour GitHub Copilot !

</div>
