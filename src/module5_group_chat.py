"""Module 5: Group Chat Workflow - Multi-agent collaboration.

This module demonstrates how to create a workflow where multiple
agents collaborate using the Group Chat pattern.
"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent, MCPStreamableHTTPTool
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.workflows import GroupChatBuilder


async def main() -> None:
    """Create a group chat with Learn and GitHub agents."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Agent 1: Learn Agent with MCP Microsoft Learn tool
    async with MCPStreamableHTTPTool(
        name="mslearn",
        description="Search Microsoft Learn documentation",
        url=os.getenv("MCP_MSLEARN_URL"),
        headers={"Authorization": f"Bearer {os.getenv('MCP_API_KEY')}"},
    ) as learn_tool:
        
        learn_agent = ChatAgent(
            chat_client=client,
            name="LearnAgent",
            instructions="""You are a documentation specialist.
            
            Your role is to:
            - Search Microsoft Learn for relevant documentation
            - Provide accurate citations with links
            - Summarize key points from documentation
            
            Always cite sources in format: [Doc: Title](URL)""",
            tools=learn_tool,
        )
        
        # Agent 2: GitHub Agent with MCP GitHub tool
        async with MCPStreamableHTTPTool(
            name="github",
            description="Manage GitHub issues and repositories",
            url=os.getenv("MCP_GITHUB_URL"),
            headers={"Authorization": f"Bearer {os.getenv('GITHUB_TOKEN')}"},
        ) as github_tool:
            
            github_agent = ChatAgent(
                chat_client=client,
                name="GitHubAgent",
                instructions="""You are a GitHub issue manager.
                
                Your role is to:
                - Create issues with proper labels
                - Add comments with context from other agents
                - Link to relevant documentation
                
                Format issues clearly with sections for:
                - Problem Description
                - Steps to Reproduce
                - Relevant Documentation
                - Recommended Actions""",
                tools=github_tool,
            )
            
            # Create Group Chat workflow
            workflow = (
                GroupChatBuilder()
                .add_participant(learn_agent)
                .add_participant(github_agent)
                .set_manager(
                    agent=ChatAgent(
                        chat_client=client,
                        name="GroupManager",
                        instructions="""You manage the discussion between agents.
                        
                        Workflow:
                        1. First, ask LearnAgent to find relevant documentation
                        2. Then, ask GitHubAgent to create an issue with the findings
                        3. Summarize the outcome
                        
                        Select the next speaker based on the current task.""",
                    )
                )
                .with_max_rounds(5)
                .build()
            )
            
            # Run the group chat
            task = """
            A user reported: "Azure Functions deployment fails with 'Out of memory' error"
            
            Please:
            1. Find relevant Azure Functions memory documentation
            2. Create a GitHub issue with the findings and recommended solutions
            """
            
            print("Starting Group Chat workflow...\n")
            print("=" * 60)
            
            async for event in workflow.run_stream(task):
                if hasattr(event, 'agent_name') and hasattr(event, 'text'):
                    print(f"\n[{event.agent_name}]:")
                    print(f"{event.text}")
                    print("-" * 40)


async def main_simple() -> None:
    """Simplified group chat without external MCP tools."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Create specialist agents
    analyst = ChatAgent(
        chat_client=client,
        name="TicketAnalyst",
        instructions="Analyze tickets and identify the core issue.",
    )
    
    researcher = ChatAgent(
        chat_client=client,
        name="Researcher",
        instructions="Research solutions and best practices for identified issues.",
    )
    
    writer = ChatAgent(
        chat_client=client,
        name="ResponseWriter",
        instructions="Write clear, helpful responses to users.",
    )
    
    # Create manager
    manager = ChatAgent(
        chat_client=client,
        name="Manager",
        instructions="""Coordinate the team to solve the ticket:
        1. Have TicketAnalyst analyze the issue
        2. Have Researcher find solutions
        3. Have ResponseWriter draft the user response""",
    )
    
    workflow = (
        GroupChatBuilder()
        .add_participant(analyst)
        .add_participant(researcher)
        .add_participant(writer)
        .set_manager(agent=manager)
        .with_max_rounds(6)
        .build()
    )
    
    task = "User ticket: My laptop is running very slow after the latest Windows update"
    
    async for event in workflow.run_stream(task):
        if hasattr(event, 'agent_name') and hasattr(event, 'text'):
            print(f"[{event.agent_name}]: {event.text}")


if __name__ == "__main__":
    # Run full example with MCP tools
    # asyncio.run(main())
    
    # Run simplified example without external tools
    asyncio.run(main_simple())
