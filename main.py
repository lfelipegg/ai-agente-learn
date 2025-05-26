import asyncio
from agents import Runner
from context import LearnerProfile
from ai_agents.architect import learning_architect_agent
from ai_agents.memory import memory_recall_agent
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def run_agent(agent, profile, chat_history):
    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        full_input = chat_history + [{"role": "user", "content": user_input}]
        result = await Runner.run(agent, input=full_input, context=profile)

        print(f"{agent.name}: {result.final_output.message}\n")
        chat_history = result.to_input_list()

        if result.final_output.done:
            print(f"✅ {agent.name} completed its task.")
            return chat_history  # Continue with next agent

async def main():
    profile = LearnerProfile()
    chat_history = []

    print("🧠 Starting with the Learning Architect Agent...")
    print("This agent will help you create a personalized study plan. You might say: 'I’m preparing for the MCAT in 3 months. Build a study plan for me.'\n")
    chat_history = await run_agent(learning_architect_agent, profile, chat_history)

    print("🧠 Now continuing with the Memory & Recall Agent...")
    print("This agent helps convert material into flashcards and set up spaced review. Try something like: 'Make flashcards and set up a review schedule of the Learning Architect Agent.'\n")
    await run_agent(memory_recall_agent, profile, chat_history)

if __name__ == "__main__":
    asyncio.run(main())