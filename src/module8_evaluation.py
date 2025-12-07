"""Module 8: Evaluation - Testing agent quality.

This module demonstrates how to implement evaluation for agent
quality and performance using local tests and Azure AI Foundry evaluators.
"""
import asyncio
import os
import json
from dataclasses import dataclass
from typing import Literal
from azure.identity import DefaultAzureCredential
from agent_framework.azure_openai import AzureOpenAIChatClient


@dataclass
class TestCase:
    """A single test case for evaluation."""
    input: str
    expected_category: Literal["network", "hardware", "software", "access", "other"]
    expected_severity: Literal["low", "medium", "high", "critical"]
    description: str = ""


@dataclass
class TestResult:
    """Result of a single test case."""
    input: str
    expected_category: str
    actual_category: str
    category_correct: bool
    expected_severity: str
    actual_severity: str
    severity_correct: bool
    overall_pass: bool
    response_time_ms: float
    error: str | None = None


# Test dataset
TEST_CASES = [
    TestCase(
        input="I can't log in to my email",
        expected_category="access",
        expected_severity="medium",
        description="Basic access issue",
    ),
    TestCase(
        input="URGENT: Production database is down!",
        expected_category="software",
        expected_severity="critical",
        description="Critical production issue",
    ),
    TestCase(
        input="How do I set up email forwarding?",
        expected_category="software",
        expected_severity="low",
        description="Simple how-to question",
    ),
    TestCase(
        input="My laptop screen is cracked",
        expected_category="hardware",
        expected_severity="medium",
        description="Hardware damage",
    ),
    TestCase(
        input="WiFi keeps disconnecting in the conference room",
        expected_category="network",
        expected_severity="medium",
        description="Network connectivity issue",
    ),
    TestCase(
        input="Need admin access to install software",
        expected_category="access",
        expected_severity="low",
        description="Permission request",
    ),
    TestCase(
        input="The entire office network is down, we can't do anything!",
        expected_category="network",
        expected_severity="critical",
        description="Critical network outage",
    ),
]


async def evaluate_agent(verbose: bool = True) -> dict:
    """Run evaluation on the ticket analyst agent."""
    
    client = AzureOpenAIChatClient(
        credential=DefaultAzureCredential(),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        deployment_name="gpt-4o",
    )
    
    agent = client.create_agent(
        name="TicketAnalyst",
        instructions="""Analyze IT tickets and respond with JSON only:
        {
            "category": "network|hardware|software|access|other",
            "severity": "low|medium|high|critical",
            "summary": "brief description"
        }
        
        Respond ONLY with the JSON, no other text.""",
    )
    
    results: list[TestResult] = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        if verbose:
            print(f"Running test case {i}/{len(TEST_CASES)}...")
        
        import time
        start_time = time.time()
        
        try:
            result = await agent.run(f"Analyze: {test_case.input}")
            elapsed_ms = (time.time() - start_time) * 1000
            
            # Parse response
            response = json.loads(result.text)
            
            category_match = response.get("category") == test_case.expected_category
            severity_match = response.get("severity") == test_case.expected_severity
            
            results.append(TestResult(
                input=test_case.input,
                expected_category=test_case.expected_category,
                actual_category=response.get("category", "unknown"),
                category_correct=category_match,
                expected_severity=test_case.expected_severity,
                actual_severity=response.get("severity", "unknown"),
                severity_correct=severity_match,
                overall_pass=category_match and severity_match,
                response_time_ms=elapsed_ms,
            ))
            
        except json.JSONDecodeError as e:
            elapsed_ms = (time.time() - start_time) * 1000
            results.append(TestResult(
                input=test_case.input,
                expected_category=test_case.expected_category,
                actual_category="parse_error",
                category_correct=False,
                expected_severity=test_case.expected_severity,
                actual_severity="parse_error",
                severity_correct=False,
                overall_pass=False,
                response_time_ms=elapsed_ms,
                error=f"Invalid JSON: {str(e)}",
            ))
        except Exception as e:
            elapsed_ms = (time.time() - start_time) * 1000
            results.append(TestResult(
                input=test_case.input,
                expected_category=test_case.expected_category,
                actual_category="error",
                category_correct=False,
                expected_severity=test_case.expected_severity,
                actual_severity="error",
                severity_correct=False,
                overall_pass=False,
                response_time_ms=elapsed_ms,
                error=str(e),
            ))
    
    # Calculate metrics
    total = len(results)
    passed = sum(1 for r in results if r.overall_pass)
    category_correct = sum(1 for r in results if r.category_correct)
    severity_correct = sum(1 for r in results if r.severity_correct)
    avg_response_time = sum(r.response_time_ms for r in results) / total
    
    return {
        "total_tests": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": passed / total,
        "category_accuracy": category_correct / total,
        "severity_accuracy": severity_correct / total,
        "avg_response_time_ms": avg_response_time,
        "details": results,
    }


def print_results(metrics: dict) -> None:
    """Print evaluation results in a formatted table."""
    
    print("\n" + "=" * 60)
    print("📊 EVALUATION RESULTS")
    print("=" * 60)
    
    print(f"\n📈 Summary Metrics:")
    print(f"{'─' * 40}")
    print(f"Total Tests:        {metrics['total_tests']}")
    print(f"Passed:             {metrics['passed']}")
    print(f"Failed:             {metrics['failed']}")
    print(f"Pass Rate:          {metrics['pass_rate']:.1%}")
    print(f"Category Accuracy:  {metrics['category_accuracy']:.1%}")
    print(f"Severity Accuracy:  {metrics['severity_accuracy']:.1%}")
    print(f"Avg Response Time:  {metrics['avg_response_time_ms']:.0f}ms")
    
    print(f"\n📋 Detailed Results:")
    print(f"{'─' * 40}")
    
    for result in metrics['details']:
        status = "✅" if result.overall_pass else "❌"
        cat_status = "✓" if result.category_correct else "✗"
        sev_status = "✓" if result.severity_correct else "✗"
        
        print(f"\n{status} {result.input[:50]}...")
        print(f"   Category: {result.expected_category} → {result.actual_category} [{cat_status}]")
        print(f"   Severity: {result.expected_severity} → {result.actual_severity} [{sev_status}]")
        print(f"   Time: {result.response_time_ms:.0f}ms")
        
        if result.error:
            print(f"   ⚠️ Error: {result.error}")


async def run_regression_test(
    baseline_accuracy: float = 0.8,
    baseline_category_accuracy: float = 0.85,
) -> bool:
    """Run regression test against baseline metrics."""
    
    print("🧪 Running Regression Test...")
    print(f"   Baseline Pass Rate: {baseline_accuracy:.1%}")
    print(f"   Baseline Category Accuracy: {baseline_category_accuracy:.1%}")
    
    metrics = await evaluate_agent(verbose=False)
    
    passed = (
        metrics['pass_rate'] >= baseline_accuracy and
        metrics['category_accuracy'] >= baseline_category_accuracy
    )
    
    if passed:
        print(f"\n✅ Regression test PASSED")
        print(f"   Current Pass Rate: {metrics['pass_rate']:.1%} (>= {baseline_accuracy:.1%})")
        print(f"   Current Category Accuracy: {metrics['category_accuracy']:.1%} (>= {baseline_category_accuracy:.1%})")
    else:
        print(f"\n❌ Regression test FAILED")
        print(f"   Current Pass Rate: {metrics['pass_rate']:.1%} (expected >= {baseline_accuracy:.1%})")
        print(f"   Current Category Accuracy: {metrics['category_accuracy']:.1%} (expected >= {baseline_category_accuracy:.1%})")
    
    return passed


async def main() -> None:
    """Run evaluation and print results."""
    
    print("🧪 Running Agent Evaluation\n")
    
    metrics = await evaluate_agent()
    print_results(metrics)


if __name__ == "__main__":
    asyncio.run(main())
    
    # Uncomment to run regression test:
    # asyncio.run(run_regression_test())
