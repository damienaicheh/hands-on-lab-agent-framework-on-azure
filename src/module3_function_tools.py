"""Module 3: Function Tools - Extending agents with custom tools.

This module demonstrates how to create function tools using the
@ai_function decorator and integrate them with agents.
"""
import asyncio
import os
import re
from typing import Annotated
from pydantic import Field
from azure.identity import DefaultAzureCredential
from agent_framework import ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient


# Define tools using @ai_function decorator
@ai_function
def extract_ticket_id(
    text: Annotated[str, Field(description="Text containing a ticket ID")]
) -> str:
    """Extract ticket ID from text (format: TICKET-YYYY-NNNN)."""
    pattern = r"TICKET-\d{4}-\d{4}"
    match = re.search(pattern, text)
    if match:
        return f"Found ticket ID: {match.group()}"
    return "No ticket ID found in the provided text."


@ai_function
def extract_user_email(
    text: Annotated[str, Field(description="Text containing an email address")]
) -> str:
    """Extract user email from text."""
    pattern = r"[\w\.-]+@[\w\.-]+\.\w+"
    match = re.search(pattern, text)
    if match:
        return f"Found email: {match.group()}"
    return "No email address found in the provided text."


@ai_function
def classify_urgency(
    description: Annotated[str, Field(description="Ticket description to classify")],
    keywords: Annotated[list[str], Field(description="Urgency keywords to look for")]
) -> dict:
    """Classify ticket urgency based on keywords."""
    urgency_keywords = {
        "critical": ["urgent", "critical", "emergency", "immediately", "asap", "down"],
        "high": ["important", "soon", "deadline", "client", "presentation"],
        "medium": ["issue", "problem", "not working", "help"],
        "low": ["question", "wondering", "when", "how to"]
    }
    
    description_lower = description.lower()
    found_level = "low"
    found_keywords = []
    
    for level, kws in urgency_keywords.items():
        for kw in kws:
            if kw in description_lower:
                found_keywords.append(kw)
                if level in ["critical", "high"]:
                    found_level = level
                    break
    
    return {
        "urgency_level": found_level,
        "matched_keywords": found_keywords,
        "analysis": f"Classified as {found_level} based on: {', '.join(found_keywords) or 'no specific keywords'}"
    }


@ai_function
def lookup_user_info(
    email: Annotated[str, Field(description="User email to look up")]
) -> dict:
    """Look up user information from the directory (simulated)."""
    # Simulated user directory
    users = {
        "john.doe@company.com": {
            "name": "John Doe",
            "department": "Sales",
            "manager": "jane.smith@company.com",
            "vip": True,
            "phone": "+1-555-0101"
        },
        "alice.jones@company.com": {
            "name": "Alice Jones", 
            "department": "Engineering",
            "manager": "bob.wilson@company.com",
            "vip": False,
            "phone": "+1-555-0102"
        }
    }
    
    if email.lower() in users:
        return users[email.lower()]
    return {"error": f"User {email} not found in directory"}


@ai_function
def create_ticket_summary(
    ticket_id: Annotated[str, Field(description="Ticket ID")],
    user_name: Annotated[str, Field(description="User's full name")],
    issue_summary: Annotated[str, Field(description="Brief issue summary")],
    urgency: Annotated[str, Field(description="Urgency level")],
) -> str:
    """Create a formatted ticket summary."""
    return f"""
╔══════════════════════════════════════════════════════════════╗
║ TICKET SUMMARY                                                ║
╠══════════════════════════════════════════════════════════════╣
║ ID: {ticket_id:<55} ║
║ User: {user_name:<53} ║
║ Urgency: {urgency.upper():<50} ║
║ Issue: {issue_summary[:52]:<52} ║
╚══════════════════════════════════════════════════════════════╝
"""


async def main() -> None:
    """Run agent with function tools."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    # Create agent with tools
    agent = client.create_agent(
        name="TicketProcessor",
        instructions="""You are a ticket processing assistant.
        
        When given a ticket:
        1. Extract the ticket ID
        2. Extract the user email
        3. Look up user information
        4. Classify the urgency
        5. Create a ticket summary with all gathered information
        
        Use the available tools to gather information.""",
        tools=[
            extract_ticket_id,
            extract_user_email,
            classify_urgency,
            lookup_user_info,
            create_ticket_summary,
        ],
    )
    
    ticket = """
    TICKET-2024-1234
    From: john.doe@company.com
    
    URGENT: Production server is down and clients cannot access 
    the application. This is affecting our biggest client's demo 
    scheduled for today at 3 PM.
    """
    
    print("Processing ticket with tools...")
    result = await agent.run(f"Process this ticket:\n{ticket}")
    print(f"\n{result.text}")


if __name__ == "__main__":
    asyncio.run(main())
