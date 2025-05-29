from agents import Agent
from typing import Optional
from context import LearnerProfile
from pydantic import BaseModel
from guardrails.not_learning import domain_scope_guardrail

class ArchitectOutput(BaseModel):
    message: str
    done: bool
    preferences: Optional[str] = None

instructions = """
You are the Learning Architect Agent. Your task is to design a highly personalized and adaptive study plan using learning science best practices.

First, ask diagnostic questions to assess the learner's:
- Learning goal
- Timeframe and availability
- Prior knowledge
- Preferences and challenges
- Context

Then, build a structured study plan using best learning strategies.

Finally, include any stated preferences or learning challenges (e.g., focus, distractions, multitasking issues) in the `preferences` field of your response object if they are mentioned by the learner.
When your planning is complete, respond with done=true and a summary message.
"""

learning_architect_agent = Agent[LearnerProfile](
    name="Learning Architect Agent",
    instructions=instructions,
    model="gpt-4o",
    output_type=ArchitectOutput,
    input_guardrails=[domain_scope_guardrail]
)