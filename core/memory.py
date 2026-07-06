import json
import os

MEMORY_FILE = "data/memory.json"


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=4)


def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)


def recall(key):
    memory = load_memory()
    return memory.get(key)


def remember_conversation(user, ai):
    memory = load_memory()

    history = memory.get("history", [])

    history.append({
        "user": user,
        "assistant": ai
    })

    # Sirf last 20 conversations rakho
    history = history[-20:]

    memory["history"] = history

    save_memory(memory)


def get_history():
    memory = load_memory()
    return memory.get("history", [])