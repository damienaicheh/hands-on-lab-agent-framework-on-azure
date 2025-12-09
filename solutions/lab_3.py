import os
from agent_framework import ToolMode
from agent_framework.azure import AzureAIAgentClient
from azure.identity.aio import AzureCliCredential
from dotenv import load_dotenv
from agent_framework.devui import serve
from models.issue_analyzer import IssueAnalyzer
from tools.time_per_issue_tools import TimePerIssueTools

load_dotenv()

def main():

    settings = {
        "project_endpoint": os.environ["AZURE_AI_PROJECT_ENDPOINT"],
        "model_deployment_name": os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        "async_credential": AzureCliCredential(),
    }
    timePerIssueTools = TimePerIssueTools()
    issue_analyzer_agent = AzureAIAgentClient(**settings).create_agent(
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
        name="IssueAnalyzerAgent",
        response_format=IssueAnalyzer,
        tool_choice=ToolMode.AUTO,
        tools=[timePerIssueTools.calculate_time_based_on_complexity]
    ) 
    
    serve(entities=[issue_analyzer_agent], port=8090, auto_open=True, tracing_enabled=True)


if __name__ == "__main__":
    main()
