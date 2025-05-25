from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class LearnerProfile:
    goal: Optional[str] = None
    timeframe: Optional[str] = None
    availability: Optional[str] = None
    prior_knowledge: Optional[str] = None
    preferences: Optional[str] = None
    context: Optional[str] = None
    history: List[dict] = field(default_factory=list)