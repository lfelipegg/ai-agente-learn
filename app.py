import streamlit as st
import os
from datetime import datetime
import asyncio
from context import LearnerProfile
from ai_agents.architect import learning_architect_agent
from ai_agents.memory import memory_recall_agent
from ai_agents.cognitive import cognitive_coach_agent
from agents import Runner
from agents.exceptions import InputGuardrailTripwireTriggered
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
    "architect": (
        learning_architect_agent,
        "This agent will help you create a personalized study plan. "
        "You might say: *'I’m preparing for the MCAT in 3 months. Build a study plan for me.'*"
    ),
    "memory": (
        memory_recall_agent,
        "This agent helps convert material into flashcards and set up spaced review. "
        "Try something like: *'Convert my biology notes into flashcards and set up a review schedule.'*"
    ),
    "cognitive": (
        cognitive_coach_agent,
        "This agent boosts focus, reduces procrastination, and teaches metacognitive strategies. "
        "Try: *'I keep getting distracted when I study. What can I do?'*"
    )
}

# Agent selection
agent_display_names = {
    "architect": "Learning Architect",
    "memory": "Memory & Recall",
    "cognitive": "Cognitive Coach"
}

selected_key = st.selectbox("Choose your agent:", list(agent_display_names.keys()), format_func=lambda k: agent_display_names[k])

# Reassign agent only if user changed selection or it's the first load
if (
    st.session_state.agent is None
    or st.session_state.agent.name.lower().replace(" ", "_") not in selected_key
):
    st.session_state.agent = agents[selected_key][0]
    st.session_state.agent_done = False
    st.session_state.chat_history = []

    st.markdown(f"### {agent_display_names[selected_key]}")
    st.markdown(agents[selected_key][1])

# Chat input
user_input = st.chat_input("Type your message")

async def handle_message(user_input):
    full_input = st.session_state.chat_history + [{"role": "user", "content": user_input}]
    try:
        result = await Runner.run(
            st.session_state.agent,
            input=full_input,
            context=st.session_state.profile
        )

        st.session_state.chat_history = result.to_input_list()

        if hasattr(result.final_output, 'preferences') and result.final_output.preferences:
            st.session_state.profile.preferences = result.final_output.preferences

        st.chat_message("assistant").markdown(result.final_output.message)

        if result.final_output.done and not st.session_state.agent_done:
            st.session_state.agent_done = True
            filename = os.path.join(
                st.session_state.save_dir,
                f"{st.session_state.agent.name.replace(' ', '_').lower()}.md"
            )
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"# {st.session_state.agent.name}\n\n{result.final_output.message}")

            st.success(f"✅ {st.session_state.agent.name} completed. Output saved to {filename}.")

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

    except InputGuardrailTripwireTriggered:
        st.chat_message("assistant").markdown(
            "⚠️ I can only assist with personalized learning plans and study goals. Try asking about how to learn better or structure your study time."
        )

if user_input:
    st.chat_message("user").markdown(user_input)
    asyncio.run(handle_message(user_input))
