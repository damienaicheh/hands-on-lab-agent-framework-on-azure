"""Module 9: Redis Integration - Persistent conversations.

This module demonstrates how to add conversation persistence
with Azure Managed Redis.
"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework_redis import RedisProvider, RedisChatMessageStore


async def main() -> None:
    """Create agent with Redis-backed memory."""
    
    redis_url = os.getenv("REDIS_CONNECTION_STRING")
    if not redis_url:
        print("⚠️ REDIS_CONNECTION_STRING not set. Using in-memory fallback.")
        await main_without_redis()
        return
    
    user_id = "user_12345"
    thread_id = "helpdesk_session_001"
    
    # Create Redis provider for semantic memory
    redis_provider = RedisProvider(
        redis_url=redis_url,
        index_name="helpdesk_memory",
        prefix="helpdesk",
        application_id="helpdesk_assistant",
        agent_id="support_agent",
        user_id=user_id,
        thread_id=thread_id,
    )
    
    # Create chat message store for conversation history
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
        instructions="""You are a helpful IT assistant with memory.
        
        You can remember:
        - User preferences
        - Previous issues and solutions
        - Common problems for this user
        
        Use this context to provide personalized support.
        Reference previous conversations when relevant.""",
        context_providers=redis_provider,
        chat_message_store_factory=create_message_store,
    )
    
    # Simulate a multi-turn conversation
    conversations = [
        "Hi, I'm having VPN issues again",
        "It's the same problem as last week - keeps disconnecting",
        "Yes, I tried the steps you suggested before",
        "What else can I try?",
    ]
    
    thread = agent.get_new_thread()
    
    print("💬 Starting persistent conversation\n")
    print("=" * 50)
    
    for message in conversations:
        print(f"\n👤 User: {message}")
        result = await agent.run(message, thread=thread)
        print(f"🤖 Agent: {result.text}")
    
    # Save thread for later resume
    serialized = await thread.serialize()
    print(f"\n📦 Thread saved: {len(serialized)} bytes")
    
    # Simulate resuming later
    print("\n" + "=" * 50)
    print("--- Session resumed after some time ---")
    print("=" * 50)
    
    resumed_thread = await agent.deserialize_thread(serialized)
    
    resume_message = "Can you remind me what we discussed and what I should try next?"
    print(f"\n👤 User: {resume_message}")
    result = await agent.run(resume_message, thread=resumed_thread)
    print(f"🤖 Agent: {result.text}")


async def main_without_redis() -> None:
    """Fallback example without Redis (in-memory only)."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="MemorylessAssistant",
        instructions="""You are a helpful IT assistant.
        
        Note: This session does not persist across restarts.
        Each conversation is independent.""",
    )
    
    thread = agent.get_new_thread()
    
    conversations = [
        "Hi, I'm having printer issues",
        "It says 'offline' but it's turned on",
        "I already tried restarting it",
    ]
    
    print("💬 In-memory conversation (no persistence)\n")
    print("=" * 50)
    
    for message in conversations:
        print(f"\n👤 User: {message}")
        result = await agent.run(message, thread=thread)
        print(f"🤖 Agent: {result.text}")


async def main_with_semantic_search() -> None:
    """Example using Redis for semantic memory search."""
    
    redis_url = os.getenv("REDIS_CONNECTION_STRING")
    if not redis_url:
        print("⚠️ REDIS_CONNECTION_STRING required for semantic search")
        return
    
    # Create provider with semantic capabilities
    provider = RedisProvider(
        redis_url=redis_url,
        index_name="semantic_memory",
        prefix="support",
        application_id="helpdesk",
        agent_id="support_agent",
        user_id="user_123",
        thread_id="session_abc",
        # Enable semantic search
        enable_semantic_search=True,
        embedding_model="text-embedding-ada-002",
    )
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="SemanticMemoryAgent",
        instructions="""You have semantic memory capabilities.
        
        You can search through past conversations to find:
        - Similar issues that were resolved
        - User preferences and history
        - Solutions that worked before
        
        Use this knowledge to provide better support.""",
        context_providers=provider,
    )
    
    # Store some facts
    await provider.store_fact(
        "user_123",
        "User prefers detailed step-by-step instructions"
    )
    await provider.store_fact(
        "user_123",
        "User had VPN issues resolved by reinstalling the client"
    )
    
    # Query using semantic search
    result = await agent.run(
        "I'm having connection problems, what should I try?",
    )
    print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
