"""Module 7: Observability - Tracing with OpenTelemetry.

This module demonstrates how to enable tracing and monitoring
with OpenTelemetry and Microsoft Foundry.
"""
import asyncio
import os
from azure.identity import DefaultAzureCredential
from azure.monitor.opentelemetry import configure_azure_monitor
from agent_framework import ChatAgent, ai_function
from agent_framework.azure_openai import AzureOpenAIChatClient
from agent_framework.observability import setup_observability
from opentelemetry import trace, metrics
from typing import Annotated
from pydantic import Field


# Configure Azure Monitor (Application Insights)
def configure_monitoring():
    """Configure Azure Monitor for telemetry export."""
    connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
    if connection_string:
        configure_azure_monitor(connection_string=connection_string)
        print("✓ Azure Monitor configured")
    else:
        print("⚠ APPLICATIONINSIGHTS_CONNECTION_STRING not set, using console exporter")


# Setup Agent Framework observability
def setup_agent_observability():
    """Setup observability for the agent framework."""
    setup_observability(
        service_name="helpdesk-agents",
        enable_tracing=True,
        enable_metrics=True,
    )
    print("✓ Agent Framework observability configured")


# Get tracer and meter
tracer = trace.get_tracer(__name__)
meter = metrics.get_meter(__name__)

# Create custom metrics
ticket_counter = meter.create_counter(
    name="tickets_processed",
    description="Number of tickets processed",
    unit="1",
)

response_time_histogram = meter.create_histogram(
    name="agent_response_time",
    description="Time taken by agent to respond",
    unit="ms",
)


@ai_function
def check_system_status(
    system_name: Annotated[str, Field(description="Name of the system to check")]
) -> dict:
    """Check the status of a system."""
    # Record a span for this tool call
    with tracer.start_as_current_span("check_system_status") as span:
        span.set_attribute("system.name", system_name)
        
        # Simulated status check
        statuses = {
            "email": {"status": "operational", "latency_ms": 45},
            "vpn": {"status": "degraded", "latency_ms": 250},
            "auth": {"status": "operational", "latency_ms": 30},
            "crm": {"status": "operational", "latency_ms": 120},
        }
        
        result = statuses.get(system_name.lower(), {
            "status": "unknown",
            "latency_ms": -1
        })
        
        span.set_attribute("system.status", result["status"])
        span.set_attribute("system.latency_ms", result["latency_ms"])
        
        return {
            "system": system_name,
            "status": result["status"],
            "latency_ms": result["latency_ms"],
            "last_check": "2024-01-15T10:30:00Z",
        }


async def process_ticket_with_telemetry(
    agent: ChatAgent,
    ticket: str,
    ticket_id: str
) -> str:
    """Process a ticket with full telemetry."""
    
    with tracer.start_as_current_span("process_ticket") as span:
        span.set_attribute("ticket.id", ticket_id)
        span.set_attribute("ticket.length", len(ticket))
        
        import time
        start_time = time.time()
        
        try:
            result = await agent.run(ticket)
            
            # Record success
            span.set_attribute("ticket.status", "completed")
            ticket_counter.add(1, {"status": "success"})
            
            return result.text
            
        except Exception as e:
            # Record failure
            span.set_attribute("ticket.status", "failed")
            span.set_attribute("error.message", str(e))
            ticket_counter.add(1, {"status": "error"})
            raise
            
        finally:
            # Record response time
            elapsed_ms = (time.time() - start_time) * 1000
            response_time_histogram.record(elapsed_ms, {"agent": "helpdesk"})


async def main() -> None:
    """Run agent with full observability."""
    
    # Setup monitoring
    configure_monitoring()
    setup_agent_observability()
    
    with tracer.start_as_current_span("helpdesk_session") as session_span:
        session_span.set_attribute("user.id", "demo_user")
        session_span.set_attribute("session.type", "support_request")
        
        client = AzureOpenAIChatClient(
            credential=DefaultAzureCredential(),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name="gpt-4o",
        )
        
        agent = client.create_agent(
            name="ObservableAgent",
            instructions="""You are a helpful assistant with system monitoring capabilities.
            
            When asked about systems, use the check_system_status tool to get current status.
            Provide clear status updates with any relevant details.""",
            tools=[check_system_status],
        )
        
        queries = [
            ("TKT-001", "Check the status of the email system"),
            ("TKT-002", "What about the VPN gateway?"),
            ("TKT-003", "Is the authentication service working?"),
        ]
        
        thread = agent.get_new_thread()
        
        for ticket_id, query in queries:
            with tracer.start_as_current_span("agent_query") as query_span:
                query_span.set_attribute("query.text", query)
                query_span.set_attribute("ticket.id", ticket_id)
                
                print(f"\n[{ticket_id}] User: {query}")
                
                result = await process_ticket_with_telemetry(
                    agent=agent,
                    ticket=query,
                    ticket_id=ticket_id,
                )
                
                print(f"Agent: {result}")
                
                query_span.set_attribute("response.length", len(result))
        
        session_span.set_attribute("tickets.processed", len(queries))


async def main_with_custom_context() -> None:
    """Example showing custom context propagation."""
    
    configure_monitoring()
    setup_agent_observability()
    
    # Create a custom context for correlation
    with tracer.start_as_current_span("parent_operation") as parent:
        parent.set_attribute("correlation.id", "abc-123-xyz")
        
        client = AzureOpenAIChatClient(
            credential=DefaultAzureCredential(),
            endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            deployment_name="gpt-4o",
        )
        
        agent = client.create_agent(
            name="ContextAwareAgent",
            instructions="You are a helpful assistant.",
        )
        
        # The agent traces will be children of this parent span
        with tracer.start_as_current_span("agent_interaction"):
            result = await agent.run("Hello, can you help me?")
            print(result.text)


if __name__ == "__main__":
    asyncio.run(main())
