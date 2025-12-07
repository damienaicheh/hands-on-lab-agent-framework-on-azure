"""Module 1: Simple Agent - Basic helpdesk greeting agent.

This module demonstrates how to create a basic AI agent using the
Microsoft Agent Framework with Azure OpenAI.
"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


async def main() -> None:
    """Create and run a simple helpdesk agent."""
    
    # Create Azure OpenAI client with Azure Identity
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Create the agent with instructions
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="""You are a friendly IT helpdesk assistant.
        
        Your role is to:
        - Greet users warmly
        - Understand their IT issues
        - Provide initial guidance
        - Escalate complex issues appropriately
        
        Always be professional and empathetic.""",
    )
    
    # Run the agent with a simple query
    query = "Hi, my laptop won't connect to the VPN and I have an important meeting in 30 minutes!"
    print(f"User: {query}")
    
    result = await agent.run(query)
    print(f"Agent: {result.text}")


async def main_streaming() -> None:
    """Run agent with streaming response for better UX."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="HelpdeskGreeter",
        instructions="You are a friendly IT helpdesk assistant.",
    )
    
    query = "My email is not syncing on my phone"
    print(f"User: {query}")
    print("Agent: ", end="")
    
    async for update in agent.run_stream(query):
        if update.text:
            print(update.text, end="", flush=True)
    print()  # New line at end


if __name__ == "__main__":
    # Run basic example
    asyncio.run(main())
    
    # Uncomment to run streaming example:
    # asyncio.run(main_streaming())
