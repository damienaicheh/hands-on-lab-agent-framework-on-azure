---
published: true
type: workshop
title: Product Hands-on Lab - Agent Framework on Azure
short_title: Agent Framework on Azure
description: This workshop will cover how to build agentic applications using the Agent Framework on Azure, leveraging various Azure services to create scalable and efficient solutions.
level: beginner # Required. Can be 'beginner', 'intermediate' or 'advanced'
navigation_numbering: false
authors: # Required. You can add as many authors as needed
  - Olivier Mertens
  - David Rei
  - Damien Aicheh
contacts: # Required. Must match the number of authors
  - "@olmertens"
  - "@reidav"
  - "@damienaicheh"
duration_minutes: 300
tags: microsoft foundry, agent framework, ai search, ag-ui, dev-ui, csu, codespace, devcontainer
navigation_levels: 3
banner_url: assets/banner.jpg
audience: developers, architects, AI engineers

---

# Product Hands-on Lab - Agent Framework on Azure

Welcome to this hands-on lab! In this workshop, you will learn how to build agentic applications using the Agent Framework on Azure.



Scénario : “Helpdesk Ops Assistant”
Tu construis un mini‑helpdesk piloté par agents qui traite des tickets internes avec des FAQ d’entreprise (AI Search), un carnet d’actions IT (MCP server) et des outils natifs.


Agent 1 – Orchestrator : route les requêtes et choisit le bon flux (Solo vs. Group Chat). 
Agent 2 – Complexity Analyst (solo) : analyse le ticket, produit un output structuré (data contract) et propose la stratégie (réponse directe, création de ticket, escalade, docs Learn à citer). 
Agent 3 – Learn Agent (MCP mslearn) : interroge la connaissance via Foundry IQ (et/ou un serveur MCP “mslearn”) pour fournir des citations Learn pertinentes. 
Agent 4 – GitHub Agent (MCP github) : exécute les actions de ticketing GitHub (issue, labels, commentaires), en s’appuyant sur les éléments fournis par les 2 autres agents.


---

## Prerequisites

Before starting this lab, be sure to set your Azure environment :

- An Azure Subscription with the **Contributor** role to create and manage the labs' resources and deploy the infrastructure as code
- Register the Azure providers on your Azure Subscription if not done yet: `Microsoft.CognitiveServices`.

To retrieve the lab content :

- A Github account (Free, Team or Enterprise)
- Create a [fork][repo-fork] of the repository from the **main** branch to help you keep track of your changes

3 development options are available:
  - 🥇 *Preferred method* : Pre-configured GitHub Codespace 
  - 🥈 Local Devcontainer
  - 🥉 Local Dev Environment with all the prerequisites detailed below

<div class="tip" data-title="Tips">

> To focus on the main purpose of the lab, we encourage the usage of devcontainers/codespace as they abstract the dev environment configuration, and avoid potential local dependencies conflict.
> 
> You could decide to run everything without relying on a devcontainer : To do so, make sure you install all the prerequisites detailed below.

</div>

### 🥇 : Pre-configured GitHub Codespace

To use a Github Codespace, you will need :
- [A GitHub Account][github-account]

Github Codespace offers the ability to run a complete dev environment (Visual Studio Code, Extensions, Tools, Secure port forwarding etc.) on a dedicated virtual machine. 
The configuration for the environment is defined in the `.devcontainer` folder, making sure everyone gets to develop and practice on identical environments : No more conflict on dependencies or missing tools ! 

Every Github account (even the free ones) grants access to 120 vcpu hours per month, _**for free**_. A 2 vcpu dedicated environment is enough for the purpose of the lab, meaning you could run such environment for 60 hours a month at no cost!

To get your codespace ready for the labs, here are a few steps to execute : 
- After you forked the repo, click on `<> Code`, `Codespaces` tab and then click on the `+` button:

![codespace-new](./assets/codespace-new.png)

- You can also provision a beefier configuration by defining creation options and select the **Machine Type** you like : 

![codespace-configure](./assets/codespace-configure.png)

### 🥈 : Using a local Devcontainer

This repo comes with a Devcontainer configuration that will let you open a fully configured dev environment from your local Visual Studio Code, while still being completely isolated from the rest of your local machine configuration : No more dependancy conflict.
Here are the required tools to do so : 

- [Git client][git-client] 
- [Docker Desktop][docker-desktop] running
- [Visual Studio Code][vs-code] installed on your machine

Start by cloning the repository you just forked on your local Machine and open the local folder in Visual Studio Code.
Once you have cloned the repository locally, make sure Docker Desktop is up and running and open the cloned repository in Visual Studio Code.  

You will be prompted to open the project in a Dev Container. Click on `Reopen in Container`. 

If you are not prompted by Visual Studio Code, you can open the command palette (`Ctrl + Shift + P`) and search for `Reopen in Container` and select it: 

![devcontainer-reopen](./assets/devcontainer-reopen.png)

### 🥉 : Using your own local environment

The following tools and access will be necessary to run the lab on a local environment :  

- [Git client][git-client] 
- [Visual Studio Code][vs-code] installed
- [Azure CLI][az-cli-install] installed on your machine
- [Python 3.13][download-python] installed on your machine
- [UV package manager][download-uv] installed on your machine
- [Terraform][download-terraform] installed on your machine

Once you have set up your local environment, you can clone the repository you just forked on your machine, and open the local folder in Visual Studio Code and head to the next step. 

### Sign in to Azure

> - Log into your Azure subscription in your environment using Azure CLI and on the [Azure Portal][az-portal] using your credentials.
> - Instructions and solutions will be given for the Azure CLI, but you can also use the Azure Portal if you prefer.
> - Register the Azure providers on your Azure Subscription if not done yet: `Microsoft.CognitiveServices`

```bash
# Login to Azure : 
# --tenant : Optional | In case your Azure account has access to multiple tenants

# Option 1 : Local Environment 
az login --tenant <yourtenantid or domain.com>
# Option 2 : Github Codespace : you might need to specify --use-device-code parameter to ease the az cli authentication process
az login --use-device-code --tenant <yourtenantid or domain.com>

# Display your account details
az account show
# Select your Azure subscription
az account set --subscription <subscription-id>

# Register the following Azure providers if they are not already

# Azure Cognitive Services
az provider register --namespace 'Microsoft.CognitiveServices'
```

### Deploy the infrastructure

First, you need to initialize the terraform infrastructure by running the following command:

```bash
# Set the subscription ID as an environment variable
export ARM_SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Initialize terraform
cd infra && terraform init
```

Then run the following command to deploy the infrastructure:

```bash
# Apply the deployment directly
terraform apply -auto-approve
```

The deployment should take around 5 minutes to complete.

[az-cli-install]: https://learn.microsoft.com/en-us/cli/azure/install-azure-cli
[az-portal]: https://portal.azure.com
[vs-code]: https://code.visualstudio.com/
[azure-function-vs-code-extension]: https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions
[docker-desktop]: https://www.docker.com/products/docker-desktop/
[repo-fork]: https://github.com/microsoft/hands-on-lab-agent-framework-on-azure/fork
[git-client]: https://git-scm.com/downloads
[github-account]: https://github.com/join
[download-python]: https://www.python.org/downloads/
[download-uv]: https://docs.astral.sh/uv/
[download-terraform]: https://developer.hashicorp.com/terraform/install

---

## Create your first agent

Let's create a first simple agent using the Agent Framework and a Foundry model to respond to basic queries.

Inside the `src` folder, you will find a `pyproject.toml` file that defines the dependencies for your Python project. Make sure to install them using `uv` and activate the virtual environment:

```bash
# Install dependencies
uv sync
# Activate the virtual environment
source .venv/bin/activate
```

Then, rename the `.env.template` file to `.env` and update the environment variables with the values from your deployed infrastructure.

To connect to the AI chat model you need, you will use the Microsoft Foundry project resource to connect to the deployed models.

Go to Azure, inside your resource group, select the Microsoft Foundry project: 

![resource-group-foundry-project](./assets/resource-group-foundry-project.png)

Then select `Go to Foundry portal`: 

![open-foundry-project](./assets/open-foundry-project.png)

You will be redirected to the home page of Microsoft Foundry Portal where you will have to copy paste the endpoint

![foundry-project-endpoint](./assets/foundry-project-endpoint.png)

Then assign it's value inside the `.env` file in the `AZURE_AI_PROJECT_ENDPOINT` environment variable. 

When it's done, due to the role assigned to you on this cloud resource, you can have access to the models with your code. 

Now let's create your first agent! 

Inside `main.py` first, define the structure of the file and load the `.env` file and add the imports:

```python
import os
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv
from agent_framework.devui import serve
import logging

load_dotenv()

def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    
    ## Create the agent here

if __name__ == "__main__":
    main()
```

Then, let's create the first agent: IssueAnalyzerAgent, using the Agent Framework to analyze an ask.

```python
settings = {
    "project_endpoint": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    "model_deployment_name": os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
    "async_credential": AzureCliCredential(),
}
issue_analyzer_agent = AzureAIAgentClient(**settings).create_agent(
    instructions="""
                    You are analyzing issues. 
                    If the ask is a feature request the complexity should be 'NA'.
                    If the issue is a bug, analyze the stack trace and provide the likely cause and complexity level
                """,
    name="IssueAnalyzerAgent",
) 
```

For the purpose of this lab, we voluntarily use a `settings` dictionary to pass the parameters to create the agent to be able to reuse it later when creating other agents but you can also pass the parameters directly inside the `AzureAIAgentClient` constructor.

The `AzureAIAgentClient` class allows you to create agents that leverage Azure AI models deployed in your Microsoft Foundry project.

To help you build and test your agent more easily, instead of relying only on the console output, let's introduce Dev UI integration.

Let's modify the `main.py` file to add Dev UI integration just after the agent creation.

```python
serve(entities=[issue_analyzer_agent], port=8090, auto_open=True, tracing_enabled=True)
```

Now if you run your agent again:

```bash
uv run python main.py
```

Let's run the agent with a simple prompt to analyze a first ask:

```txt
There is an issue with the Azure App Services is causing intermittent 500 errors. 
                        Traceback (most recent call last):
                                    File "<string>", line 38, in <module>
                                        main_application()                    ← Entry point
                                    File "<string>", line 30, in main_application
                                        results = process_data_batch(test_data)  ← Calls processor
                                    File "<string>", line 13, in process_data_batch
                                        avg = calculate_average(batch)        ← Calls calculator
                                    File "<string>", line 5, in calculate_average
                                        return total / count                  ← ERROR HERE
                                            ~~~~~~^~~~~~~
                                    ZeroDivisionError: division by zero
```

or you can also ask a feature request:

```txt
Please add a dark mode to the application to improve user experience during night time usage.
```

Open your browser and go to `http://localhost:8090` to access the Dev UI. You should see your agent listed there. Click on it to open the chat interface.

![issue_agent_tool_devui_start.png](./assets/issue_agent_tool_devui_start.png)

If you try to run the agent multiple times, you might hit the rate limit of tokens per minute. If that happens, you will see a 429 error. Just wait a minute and try again.

Also, if you look at the output, the response is always different because the model is generative and non-deterministic by default, but you ask the model to structure the output in a specific format. That's what you will do in the next step.

> The final `main.py` file can be found in `solutions/lab_1.py`.

---

## Add response format

Let's structure the output of your agent to make it more useful.

To make sure the IssueAnalyzerAgent provide the same structure every time, let's define a response format using a basic python class.

Inside the `src` folder, create a new folder called `models` and inside this folder create a new file called `issue_analyzer.py`.

```python
from pydantic import BaseModel
from enum import Enum

class Complexity(Enum):
    NA = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3
        
class IssueAnalyzer(BaseModel):
    """Information about an issue."""
    title: str | None = None
    description: str | None = None
    reason: str | None = None
    complexity: Complexity | None = None
    time_estimate_hours: str | None = None
```

As you can see, the `IssueAnalyzer` class defines multiple fields that the agent will fill when answering a prompt.

Now, let's modify the `main.py` file to use this response format. Inside the creation of the agent, add the `response_format` parameter:

```python
response_format=IssueAnalyzer
```

Also, make sure to import the `IssueAnalyzer` class at the top of the file:

```python
from models.issue_analyzer import IssueAnalyzer
```

You can now run your agent again:

```bash
uv run python main.py
```

You should notice that the output is now structured according to the `IssueAnalyzer` class you defined.

As you can see in the Dev UI, the output is now in JSON format, making it easier to parse and use in other agents or systems:

![devui-structured-output](./assets/issue_agent_tool_devui_json.png)

> The final `main.py` file can be found in `solutions/lab_2.py`.

---

## Add native tools

If you looked at the output of your agent, you probably noticed that the estimated time to resolve the issue is randomly generated by the model. To make it more accurate, let's add a native tool that will help the agent estimate the time based on the complexity of the issue.

First, create a new folder called `tools` inside the `src` folder. Then, inside this folder, create a new file called `time_per_issue_tools.py`.

```python
from models.issue_analyzer import Complexity
from typing import Annotated
from pydantic import Field

class TimePerIssueTools:

    def calculate_time_based_on_complexity(
        self,
        complexity: Annotated[Complexity, Field(description="The complexity level of the issue.")],
    ) -> str:
        """Calculate the time required based on issue complexity."""
        match complexity:
            case Complexity.NA:
                return "1 hour"
            case Complexity.LOW:
                return "2 hours"
            case Complexity.MEDIUM:
                return "4 hours"
            case Complexity.HIGH:
                return "8 hours"
            case _:
                return "Unknown complexity level"
```

This class defines a single tool that calculates the estimated time to resolve an issue based on its complexity. Of course, you can implement more tools as needed, with API calls or other logic.

Now, let's modify the `main.py` file to add this tool to your agent.

First, add the imports at the top of the file:

```python
from tools.time_per_issue_tools import TimePerIssueTools
from agent_framework import ToolMode
```

Then before the agent creation, create an instance of the `TimePerIssueTools` class:

```python
timePerIssueTools = TimePerIssueTools()
```

Inside the agent creation add the tools properties:

```python
tool_choice=ToolMode.AUTO,
tools=[timePerIssueTools.calculate_time_based_on_complexity]
```

Also, let's update the instructions to give more details to the agent on how to use this tool:

```python
instructions="""
    You are analyzing issues. 
    If the ask is a feature request the complexity should be 'NA'.
    If the issue is a bug, analyze the stack trace and provide the likely cause and complexity level.

    CRITICAL: You MUST use the provided tools for ALL calculations:
    1. First determine the complexity level
    2. Use the available tools to calculate time and cost estimates based on that complexity
    3. Never provide estimates without using the tools first

    Your response should contain only values obtained from the tool calls.
""",
```

Now, run your agent again:

```bash
uv run python main.py
```

As you can see in the `Tools` tab of Dev UI, the agent used the `calculate_time_based_on_complexity` tool to estimate the time to resolve the issue based on its complexity. If you look at the **Tools** tab, you should see the tool being called with the complexity level and the estimated time being returned:

![devui-tools-tab](./assets/issue_agent_tool_devui.png)

Your IssueAnalyzerAgent is now more precise and reliable!

> The final `main.py` file can be found in `solutions/lab_3.py`.

---

## Add MCP tool

You have now a first agent to analyze issues and request of users, but to build a complete helpdesk solution, you need to add another agent responsible of adding the query as a ticket. For the purpose of this workshop, you will use your own GitHub repository as a ticketing system, using GitHub Issues.

To do that, you will use the MCP GitHub tool provided by GitHub and create a new agent called GitHubAgent.

### Get a GitHub PAT (Personal Access Token)

To authenticate to GitHub, you need to create a Personal Access Token (PAT) with the appropriate permissions. This PAT will only need to have access to your repository (result of the fork you did at the beginning of the workshop) and read/write access to issues.

To do so, go to your GitHub account settings, then to **Developer Settings** > **Personal Access Tokens** > **Fine-grained tokens** and create a new token with the following settings:

- Give it a name, e.g., `Agent Framework Workshop Token`
- Set the expiration to `30 days`
- Under **Repository access**, select `Only select repositories` and choose the repository you forked
- Under **Permissions**, set the following:
  - Issues: `Read and write`

Finally click on **Generate token**.

![github-create-pat](./assets/github-create-pat.png)

Once the token is created, make sure to copy it and paste it inside the `.env` file in the `GITHUB_PAT` environment variable. Also, set the `GITHUB_REPOSITORY` environment variable to the format `owner/repo`, e.g., `your-username/your-forked-repo`.

### Create the GitHubAgent

Now, let's create the GitHubAgent inside the `main.py` file. Just after the creation of the IssueAnalyzerAgent, add the following code:

```python
github_agent = AzureAIAgentClient(**settings).create_agent(
    name="GitHubAgent",
    instructions=f"""
        You are a helpful assistant that can create an issue on the user's GitHub repository based on the input provided.
        To create the issue, use the GitHub MCP tool.
        You work on this repository: {os.environ["GITHUB_PROJECT_REPO"]}
    """,
    tools=HostedMCPTool(
        name="GitHub MCP",
        url="https://api.githubcopilot.com/mcp",
        description="A GitHub MCP server for GitHub interactions",
        approval_mode="never_require",
        # PAT token, restricting which repos the MCP Server
        headers={
            "Authorization": f"Bearer {os.environ['GITHUB_MCP_PAT']}",
        },
    ),
)
```

Don't forget to import the `HostedMCPTool` class at the top of the file:

```python
from agent_framework import HostedMCPTool
```

As you can see, you dynamically load the MCP GitHub tool, pass the authentication parameter, and create the agent using this tool.

Finally, as you did for the IssueAnalyzerAgent, add the GitHubAgent to the Dev UI integration:

```python
serve(entities=[issue_analyzer_agent, github_agent], port=8090, auto_open=True, tracing_enabled=True)
```

Now, run your agent again:

```bash
uv run python main.py
```

Select the GitHubAgent in the Dev UI and ask your first question:

![select-menu-devui](./assets/devui_select_menu.png)

If you ask the agent to create a ticket, it should create a new issue in your GitHub repository!

> The final `main.py` file can be found in `solutions/lab_4.py`.

---

## Create a group chat workflow

You have now two agents: the IssueAnalyzerAgent to analyze issues and the GitHubAgent to create tickets in GitHub. To build a complete helpdesk solution, you need to orchestrate these two agents to work together in a group chat. 

To do that you will use a mechanism called Group Chat Workflow provided by the Agent Framework.

This will allow the agents to communicate and collaborate to handle ask in their own chat.

Let's create the chat group inside the `main.py` file. 

First import the `GroupChatBuilder` class at the top of the file:

```python
from agent_framework import GroupChatBuilder
```

Just after the creation of the GitHubAgent, add the following code:

```python
group_workflow = (
    GroupChatBuilder()
    .set_manager(
        manager=AzureAIAgentClient(**settings).create_agent(
            name="Issue Creation Group Chat Workflow",
            instructions="""
                You are a workflow manager that helps create GitHub issues based on user input.
                First, analyze the input using the Issue Analyzer Agent to determine the issue type, likely cause, and complexity.
                If an issue requires additional information from documentation, ask other specialized agents.
                Finally, create a GitHub issue using the GitHub Agent with the analyzed information.
            """,
        ),
    )
    .participants(
        github_agent=github_agent, issue_analyzer_agent=issue_analyzer_agent
    )
    .build()
)
```

As you can see, you create a group chat workflow with the IssueAnalyzerAgent and the GitHubAgent. The agents are guided by a manager agent that will route the requests to the appropriate agent based on the prompt.

Now, update the Dev UI setup to add the group chat workflow instead of the individual agents:

```python
serve(entities=[issue_analyzer_agent, github_agent, group_workflow_agent], port=8090, auto_open=True, tracing_enabled=True)
```

Now, run your agent again:

```bash
uv run python main.py
```



You can now interact with the group chat workflow. The manager agent will route your requests to the appropriate agent based on the prompt.

> The final `main.py` file can be found in `solutions/lab_5.py`.

---

## Orchestrate with a sequencial workflow

Let's go a step further and add one more agent in the picture. You will add an DocsAgent that will provide relevant documentation from Microsoft Learn to help the agents answer user requests. This agent will use the MCP Learn tool.

First, create the DocsAgent inside the `main.py` file. Just after the creation of the GitHubAgent, add the following code:

```python
ms_learn_agent = AzureAIAgentClient(**settings).create_agent(
    name="DocsAgent",
    instructions="""
        You are a helpful assistant that can help with Microsoft documentation questions.
        Provide accurate and concise information based on the documentation available.
    """,
    tools=HostedMCPTool(
        name="Microsoft Learn MCP",
        url="https://learn.microsoft.com/api/mcp",
        description="A Microsoft Learn MCP server for documentation questions",
        approval_mode="never_require",
    ),
)
```

If you want to test it individually, you can update the Dev UI integration:

```python
serve(entities=[issue_analyzer_agent, github_agent, ms_learn_agent, group_workflow_agent], port=8090, auto_open=True, tracing_enabled=True)
```

As you can see, you dynamically load the MCP Learn tool, without authentication for this one, as it's totally open, and create the agent using this tool.

Then, let's create a sequential workflow that will first, call the DocsAgent and then the group of agents containing the IssueAnalyzerAgent and the GitHubAgent.

Let's first transform the workflow containing the IssueAnalyzerAgent and the GitHubAgent into an agent so it can be called inside another workflow.

```python
group_workflow_agent = group_workflow.as_agent(
    name="IssueCreationAgentGroup"
)
```

Then, create the sequential workflow:

```python
workflow = (
    SequentialBuilder()
    .participants([ms_learn_agent, group_workflow_agent])
    .build()
)
```

Update the Dev UI setup to run the sequential workflow instead of the group chat workflow:

```python
serve(entities=[issue_analyzer_agent, github_agent, ms_learn_agent, group_workflow_agent, workflow], port=8090, auto_open=True, tracing_enabled=True)
```

Finally, run your agent again:

```bash
uv run python main.py
```

> The final `main.py` file can be found in `solutions/lab_6.py`.

---

## Add your own knowledge base with RAG

You now have a complete helpdesk solution with multiple agents working together to handle user requests. However, the GitHubAgent is doing some ticketing without really knowing your company's conventions and best practices. To improve this, you will add another source of knowledge using Retrieval-Augmented Generation (RAG) with Azure AI Search.

Let's create an index of data using the provided script `docs_indexer.py` inside the `data` folder. This script will read all the files inside the `data/docs` folder and index them into your Azure AI Search service. This will be used as a knowledge base for the GitHubAgent.

First, make sure to set the `AZURE_AI_SEARCH_ENDPOINT` environment variables in your `.env` file with the values from your deployed infrastructure.

Then, run the indexer script:

```bash
python data/docs_indexer.py
```

Now, let's modify the GitHubAgent to use this knowledge base when answering user requests. Inside the creation of the GitHubAgent, add the following code to create a retriever using Azure AI Search:

```python
TODO
```

Then, pass this retriever to the GitHubAgent:

```python
TODO
```

You can run the flow again, and now the GitHubAgent will use the knowledge base to provide more accurate and relevant answers based on your company's documentation.
