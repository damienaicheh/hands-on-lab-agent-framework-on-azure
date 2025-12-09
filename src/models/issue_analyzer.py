from pydantic import BaseModel
from enum import Enum

class Complexity(Enum):
    NA = 0
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class IssueAnalyzer(BaseModel):
    """Information about an issue."""

    title: str | None = None
    description: str | None = None
    reason: str | None = None
    complexity: Complexity | None = None
    time_estimate_hours: str | None = None
