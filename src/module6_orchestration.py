"""Module 6: Advanced Orchestration - Handoff workflow.

This module demonstrates how to build sophisticated orchestration
with the Handoff pattern for routing between specialist agents.
"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from agent_framework import ChatAgent
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.workflows import HandoffBuilder


def create_agents(client: AzureOpenAIChatClient) -> dict:
    """Create all specialist agents."""
    
    complexity_analyst = ChatAgent(
        chat_client=client,
        name="ComplexityAnalyst",
        instructions="""Analyze ticket complexity and recommend routing.
        
        Output format:
        - Complexity: simple | medium | complex
        - Recommended Handler: direct_response | create_ticket | escalate
        - Reasoning: brief explanation
        """,
    )
    
    quick_resolver = ChatAgent(
        chat_client=client,
        name="QuickResolver",
        instructions="""Handle simple IT issues directly.
        
        Provide step-by-step solutions for common problems like:
        - Password resets
        - Browser cache clearing
        - Basic network troubleshooting
        """,
    )
    
    ticket_creator = ChatAgent(
        chat_client=client,
        name="TicketCreator",
        instructions="""Create detailed support tickets.
        
        Format:
        - Title: Clear, concise issue title
        - Priority: Low | Medium | High | Critical
        - Category: Network | Hardware | Software | Access
        - Description: Detailed problem description
        - Steps to Reproduce: If applicable
        """,
    )
    
    escalation_agent = ChatAgent(
        chat_client=client,
        name="EscalationAgent",
        instructions="""Handle complex escalations.
        
        For escalated issues:
        1. Document all gathered information
        2. Identify the appropriate specialist team
        3. Create escalation report with full context
        4. Set up follow-up reminders
        """,
    )
    
    return {
        "analyst": complexity_analyst,
        "resolver": quick_resolver,
        "creator": ticket_creator,
        "escalation": escalation_agent,
    }


async def main() -> None:
    """Run the orchestrated helpdesk workflow."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agents = create_agents(client)
    
    # Create Orchestrator with Handoff pattern
    orchestrator = ChatAgent(
        chat_client=client,
        name="Orchestrator",
        instructions="""You are the main helpdesk orchestrator.
        
        Workflow:
        1. Receive incoming requests
        2. Route to ComplexityAnalyst for initial assessment
        3. Based on analysis:
           - Simple issues → QuickResolver
           - Medium issues → TicketCreator
           - Complex issues → EscalationAgent
        4. Compile final response for user
        
        Always provide status updates during the process.""",
    )
    
    # Build Handoff workflow
    workflow = (
        HandoffBuilder()
        .set_coordinator(orchestrator)
        .add_specialist(agents["analyst"])
        .add_specialist(agents["resolver"])
        .add_specialist(agents["creator"])
        .add_specialist(agents["escalation"])
        # Configure handoff routes
        .add_handoff(orchestrator, [agents["analyst"]])
        .add_handoff(agents["analyst"], [
            agents["resolver"],
            agents["creator"],
            agents["escalation"]
        ])
        # Enable return to coordinator after specialist completes
        .enable_return_to_previous()
        .build()
    )
    
    # Test with different ticket types
    tickets = [
        "I forgot my password and need to reset it",
        "The VPN keeps disconnecting every 5 minutes since the update",
        "Our entire department can't access the CRM and we have client calls in 1 hour",
    ]
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n{'='*60}")
        print(f"Processing Ticket {i}")
        print(f"{'='*60}")
        print(f"User: {ticket}\n")
        
        async for event in workflow.run_stream(ticket):
            if hasattr(event, 'text') and event.text:
                agent_name = getattr(event, 'agent_name', 'System')
                print(f"[{agent_name}]: {event.text}")


async def main_with_conditional_routing() -> None:
    """Advanced example with conditional routing logic."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Create router function
    async def route_ticket(analysis_result: str) -> str:
        """Route based on analysis result."""
        analysis_lower = analysis_result.lower()
        
        if "simple" in analysis_lower or "quick_fix" in analysis_lower:
            return "QuickResolver"
        elif "complex" in analysis_lower or "escalate" in analysis_lower:
            return "EscalationAgent"
        else:
            return "TicketCreator"
    
    agents = create_agents(client)
    
    # Manual orchestration with conditional routing
    orchestrator = ChatAgent(
        chat_client=client,
        name="Orchestrator",
        instructions="You coordinate the helpdesk workflow.",
    )
    
    ticket = "My laptop screen is flickering intermittently"
    
    # Step 1: Analyze
    print("Step 1: Analyzing ticket...")
    analysis = await agents["analyst"].run(f"Analyze this ticket: {ticket}")
    print(f"Analysis: {analysis.text}\n")
    
    # Step 2: Route based on analysis
    target_agent = await route_ticket(analysis.text)
    print(f"Step 2: Routing to {target_agent}...")
    
    # Step 3: Execute with target agent
    result = await agents[target_agent.lower().replace("agent", "").strip()].run(
        f"Handle this ticket based on analysis:\nTicket: {ticket}\nAnalysis: {analysis.text}"
    )
    print(f"\nResult: {result.text}")


if __name__ == "__main__":
    # Run main handoff workflow
    asyncio.run(main())
    
    # Uncomment to run conditional routing example:
    # asyncio.run(main_with_conditional_routing())
