import asyncio
from agents import Runner
from datetime import datetime
from context import LearnerProfile
from ai_agents.architect import learning_architect_agent
from ai_agents.memory import memory_recall_agent
from ai_agents.cognitive import cognitive_coach_agent
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


SAVE_DIR = f"outputs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(SAVE_DIR, exist_ok=True)

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
            filename = os.path.join(SAVE_DIR, f"{agent.name.replace(' ', '_').lower()}.md")
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {agent.name}\n\n{result.final_output.message}")
            return chat_history

async def main():
    profile = LearnerProfile()
    chat_history = []

    agents = {
        "architect": (learning_architect_agent, "This agent will help you create a personalized study plan. You might say: 'I’m preparing for the MCAT in 3 months. Build a study plan for me.'"),
        "memory": (memory_recall_agent, "This agent helps convert material into flashcards and set up spaced review. Try something like: 'Convert my biology notes into flashcards and set up a review schedule.'"),
        "cognitive": (cognitive_coach_agent, "This agent boosts focus, reduces procrastination, and teaches metacognitive strategies. Try: 'I keep getting distracted when I study. What can I do?'")
    }

    print("Available agents:")
    for key in agents:
        print(f"- {key}")

    chosen_key = input("\nWhich agent would you like to use? (architect/memory/cognitive): ").strip().lower()
    if chosen_key not in agents:
        print("❌ Invalid choice. Exiting.")
        return

    agent, description = agents[chosen_key]
    print(f"\n🧠 Starting with the {agent.name}...")
    print(description + "\n")
    chat_history = await run_agent(agent, profile, chat_history)

    if agent == learning_architect_agent:
        print("🧠 Now continuing with the Memory & Recall Agent...")
        print(agents["memory"][1] + "\n")
        await run_agent(memory_recall_agent, profile, chat_history)

    # Create index.md
    index_path = os.path.join(SAVE_DIR, "index.md")
    with open(index_path, "w", encoding="utf-8") as f:
        f.write("# Learning Session Summary\n\n")
        f.write("## Included Plans:\n\n")
        for key, (agent, _) in agents.items():
            filename = f"{agent.name.replace(' ', '_').lower()}.md"
            if os.path.exists(os.path.join(SAVE_DIR, filename)):
                f.write(f"- [{agent.name} Output](./{filename})\n")

    print(f"📄 Summary written to {index_path}")

if __name__ == "__main__":
    asyncio.run(main())
