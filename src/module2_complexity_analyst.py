"""Module 2: Complexity Analyst - Structured ticket analysis.

This module demonstrates how to create structured output using Pydantic
models for consistent agent responses.
"""
import asyncio
import os
from typing import Literal
from pydantic import BaseModel, Field
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


class TicketAnalysis(BaseModel):
    """Structured analysis of a helpdesk ticket."""
    
    ticket_id: str = Field(description="Unique ticket identifier")
    category: Literal["network", "hardware", "software", "access", "other"] = Field(
        description="Primary category of the issue"
    )
    severity: Literal["low", "medium", "high", "critical"] = Field(
        description="Severity level based on business impact"
    )
    estimated_effort: Literal["quick_fix", "standard", "complex", "escalation"] = Field(
        description="Estimated effort to resolve"
    )
    summary: str = Field(description="Brief summary of the issue")
    recommended_actions: list[str] = Field(
        description="List of recommended actions to resolve"
    )
    requires_escalation: bool = Field(
        description="Whether this needs escalation to senior support"
    )
    suggested_documentation: list[str] = Field(
        description="Relevant documentation or Learn articles to cite"
    )


async def main() -> None:
    """Analyze a ticket and produce structured output."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="ComplexityAnalyst",
        instructions="""You are an expert IT ticket analyst.
        
        Analyze incoming tickets and provide:
        1. Categorization (network, hardware, software, access, other)
        2. Severity assessment (low, medium, high, critical)
        3. Effort estimation
        4. Recommended actions
        5. Escalation decision
        6. Relevant documentation references
        
        Be thorough but concise in your analysis.""",
    )
    
    # Sample ticket
    ticket = """
    TICKET-2024-1234
    Subject: Cannot access SharePoint after password reset
    
    Description:
    I reset my password yesterday as prompted by IT security.
    Since then, I cannot access SharePoint or OneDrive.
    I've tried logging out and back in, clearing cache, and using 
    a different browser. Nothing works.
    
    This is urgent as I have a client presentation tomorrow and 
    all my files are on SharePoint.
    
    User: john.doe@company.com
    Department: Sales
    """
    
    print("Analyzing ticket...")
    result = await agent.run(
        f"Analyze this ticket:\n{ticket}",
        response_format=TicketAnalysis,
    )
    
    # Parse structured response
    analysis = TicketAnalysis.model_validate_json(result.text)
    
    print(f"\n📋 Ticket Analysis: {analysis.ticket_id}")
    print(f"📁 Category: {analysis.category}")
    print(f"🚨 Severity: {analysis.severity}")
    print(f"⏱️ Effort: {analysis.estimated_effort}")
    print(f"📝 Summary: {analysis.summary}")
    print(f"🔧 Actions: {', '.join(analysis.recommended_actions)}")
    print(f"⬆️ Escalation Required: {analysis.requires_escalation}")
    print(f"📚 Documentation: {', '.join(analysis.suggested_documentation)}")


if __name__ == "__main__":
    asyncio.run(main())
