from agents import function_tool, RunContextWrapper
from context import LearnerProfile

@function_tool
def get_learning_goal(ctx: RunContextWrapper[LearnerProfile]) -> str:
    return ctx.context.goal or "Goal not yet set"