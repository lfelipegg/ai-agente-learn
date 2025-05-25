from agents import Agent
from context import LearnerProfile
from pydantic import BaseModel

class ArchitectOutput(BaseModel):
    message: str
    done: bool

instructions = """
You are the Learning Architect Agent. Your task is to design a highly personalized and adaptive study plan using learning science best practices.

First, ask diagnostic questions to assess the learner's:
- Learning goal
- Timeframe and availability
- Prior knowledge
- Preferences and challenges
- Context

Then, build a structured study plan using best learning strategies.
"""

learning_architect_agent = Agent[LearnerProfile](
    name="Learning Architect Agent",
    instructions=instructions,
    model="gpt-4o",
    output_type=ArchitectOutput
)