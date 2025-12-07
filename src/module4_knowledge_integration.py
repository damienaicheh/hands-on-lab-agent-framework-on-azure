"""Module 4: Knowledge Integration - Connect to Azure AI Search.

This module demonstrates how to integrate Azure AI Search as a
knowledge source for RAG-based responses.
"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework.azure_ai import AzureAIAgentClient


async def main() -> None:
    """Create agent with Azure AI Search integration."""
    
    # Use Azure AI Agent Service with built-in search
    async with AzureAIAgentClient(
        async_credential=DefaultAzureCredential(),
        project_connection_string=os.getenv("AZURE_AI_PROJECT_CONNECTION"),
    ) as client:
        
        # Create agent with Azure AI Search tool
        agent = await client.create_agent(
            name="LearnAgent",
            instructions="""You are a documentation expert.
            
            Your role is to:
            1. Search the knowledge base for relevant articles
            2. Provide accurate answers with citations
            3. Always cite your sources with [Source: title]
            4. Suggest related documentation for further reading
            
            Be precise and always back your answers with evidence.""",
            tools=[
                {
                    "type": "azure_ai_search",
                    "azure_ai_search": {
                        "index_connection_id": os.getenv("AZURE_AI_SEARCH_CONNECTION_ID"),
                        "index_name": "helpdesk-kb",
                    }
                }
            ],
        )
        
        # Query about VPN issues
        query = "How do I troubleshoot VPN connection issues after a password reset?"
        print(f"User: {query}\n")
        
        result = await agent.run(query)
        print(f"Agent: {result.text}")
        
        # Check for citations
        if hasattr(result, 'citations') and result.citations:
            print("\n📚 Citations:")
            for citation in result.citations:
                print(f"  - {citation.title}: {citation.url}")


async def main_with_file_search() -> None:
    """Alternative using file search for uploaded documents."""
    
    async with AzureAIAgentClient(
        async_credential=DefaultAzureCredential(),
        project_connection_string=os.getenv("AZURE_AI_PROJECT_CONNECTION"),
    ) as client:
        
        # Create a vector store for documents
        vector_store = await client.create_vector_store(
            name="helpdesk-docs",
        )
        
        # Upload documents to vector store
        # await client.upload_files_to_vector_store(
        #     vector_store_id=vector_store.id,
        #     file_paths=["docs/faq.pdf", "docs/troubleshooting.pdf"]
        # )
        
        # Create agent with file search
        agent = await client.create_agent(
            name="DocSearchAgent",
            instructions="You are a helpful assistant that answers questions using the uploaded documents.",
            tools=[{"type": "file_search"}],
            tool_resources={
                "file_search": {
                    "vector_store_ids": [vector_store.id]
                }
            }
        )
        
        result = await agent.run("What are common VPN issues?")
        print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
