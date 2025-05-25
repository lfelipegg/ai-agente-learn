import asyncio
from agents import Runner
from context import LearnerProfile
from ai_agents.architect import learning_architect_agent
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def main():
    profile = LearnerProfile()
    chat_history = []
    current_agent = learning_architect_agent

    print("🧠 Learning Architect Agent is ready. Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        full_input = chat_history + [{"role": "user", "content": user_input}]
        result = await Runner.run(current_agent, input=full_input, context=profile)

        print(f"Agent: {result.final_output.message}\n")
        chat_history = result.to_input_list()
        current_agent = result.last_agent

        if result.final_output.done:
            print("✅ The agent has completed the learning plan. Ending session.")
            break

if __name__ == "__main__":
    asyncio.run(main())