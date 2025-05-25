To structure a scalable multi-agent system with shared context in the OpenAI Agents SDK, here’s how you should organize your project:

---

### 📁 Project Layout (Recommended)

```
learning_system/
├── main.py                     # Entry point: chat loop, manages sessions
├── context.py                  # Shared LearnerProfile dataclass
├── agents/
│   ├── __init__.py
│   ├── architect.py            # Learning Architect Agent
│   ├── memory.py               # Memory Agent (e.g., flashcards, recall)
│   ├── motivation.py           # Motivation Agent (e.g., goal setting)
│   └── practice.py             # Practice Optimizer Agent
├── tools/
│   └── learner_tools.py        # Context-aware tools, shared across agents
├── utils/
│   └── storage.py              # Optional: for saving/loading context (e.g., DB)
```

---

### 📄 File Responsibilities

- **`context.py`**

  - Define the `LearnerProfile` dataclass.

- **`agents/architect.py`**

  - Define the `Learning Architect Agent`, typed with `Agent[LearnerProfile]`.

- **`tools/learner_tools.py`**

  - Place any `@function_tool` functions that interact with the context.

- **`main.py`**

  - Run the chat loop, manage session memory, load/save `LearnerProfile`, handle input/output.
  - Instantiate all agents and route conversations accordingly.

- **`utils/storage.py`** (optional but recommended)

  - Persist context to disk (JSON), a DB, or Redis for continuity between sessions.

---

### 🔄 Runtime Flow

1. `main.py` loads the context (new or persisted).
2. It runs a chat loop or handles routing.
3. It passes context and prior messages to the appropriate agent.
4. The agent reads from `LearnerProfile` and optionally calls tools to update it.
5. Updates are stored for reuse by other agents or in future sessions.

---
