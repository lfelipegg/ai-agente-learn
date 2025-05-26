import streamlit as st
import os
from datetime import datetime
import asyncio
from context import LearnerProfile
from ai_agents.architect import learning_architect_agent
from ai_agents.memory import memory_recall_agent
from ai_agents.cognitive import cognitive_coach_agent
from agents import Runner
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="Learning Agent System")
st.title("🧠 Multi-Agent Learning Assistant")

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # Initialize chat history
if "profile" not in st.session_state:
    st.session_state.profile = LearnerProfile()
if "agent" not in st.session_state:
    st.session_state.agent = None
if "agent_done" not in st.session_state:
    st.session_state.agent_done = False
if "save_dir" not in st.session_state:
    st.session_state.save_dir = f"outputs/session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(st.session_state.save_dir, exist_ok=True)

agents = {
    "Learning Architect": (learning_architect_agent, "Build a personalized study plan."),
    "Memory & Recall": (memory_recall_agent, "Create flashcards and review schedules."),
    "Cognitive Coach": (cognitive_coach_agent, "Improve focus, reduce procrastination, build mental clarity.")
}

# Agent selection
agent_name = st.selectbox("Choose your agent:", list(agents.keys()))
if st.session_state.agent is None:
    st.session_state.agent = agents[agent_name][0]
    st.markdown(f"**{agent_name}**: {agents[agent_name][1]}")

# Chat input
user_input = st.chat_input("Type your message")

async def handle_message(user_input):
    full_input = st.session_state.chat_history + [{"role": "user", "content": user_input}]
    result = await Runner.run(st.session_state.agent, input=full_input, context=st.session_state.profile)

    st.session_state.chat_history = result.to_input_list()

    # Update profile preferences if present
    if hasattr(result.final_output, 'preferences') and result.final_output.preferences:
        st.session_state.profile.preferences = result.final_output.preferences

    # Display response
    st.chat_message("assistant").markdown(result.final_output.message)

    # Save output if done
    if result.final_output.done and not st.session_state.agent_done:
        st.session_state.agent_done = True
        filename = os.path.join(
            st.session_state.save_dir,
            f"{st.session_state.agent.name.replace(' ', '_').lower()}.md"
        )
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# {st.session_state.agent.name}\n\n{result.final_output.message}")

        st.success(f"✅ {st.session_state.agent.name} completed. Output saved to {filename}.")

        # Automatic chaining logic
        if st.session_state.agent == learning_architect_agent:
            st.info("⏭ Now continuing with Memory & Recall Agent...")
            st.session_state.agent = memory_recall_agent
            st.session_state.agent_done = False
            st.session_state.chat_history = []

        elif st.session_state.agent == memory_recall_agent:
            if st.session_state.profile.preferences and any(word in st.session_state.profile.preferences.lower() for word in ["focus", "distract", "attention", "concentrate"]):
                st.info("📌 Insight: You mentioned difficulty focusing. Launching Cognitive Coach Agent...")
                st.session_state.agent = cognitive_coach_agent
                st.session_state.agent_done = False
                st.session_state.chat_history = []

if user_input:
    st.chat_message("user").markdown(user_input)
    asyncio.run(handle_message(user_input))
