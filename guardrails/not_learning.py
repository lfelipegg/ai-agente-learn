from pydantic import BaseModel
from context import LearnerProfile
from agents import Agent, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem

class ScopeCheckOutput(BaseModel):
    in_scope: bool
    reasoning: str

scope_guardrail_agent = Agent(
    name="Scope Classifier",
    instructions=(
        "Determine whether the user's message is about designing a personalized learning plan or improving learning effectiveness. "
        "Mark in_scope=False if the message asks for anything outside this, such as solving homework, giving therapy, making predictions, etc."
    ),
    output_type=ScopeCheckOutput,
    model="gpt-4o"
)

@input_guardrail
async def domain_scope_guardrail(
    ctx: RunContextWrapper[LearnerProfile],
    agent: Agent,
    input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    from agents import Runner
    result = await Runner.run(scope_guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.in_scope
    )
