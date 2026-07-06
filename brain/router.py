from core.actions import execute
from core.ai_manager import get_reply
from core.memory import (
    remember,
    recall,
    remember_conversation
)


def process(text):
    text = text.lower().strip()

    # Exit
    if text in [
        "bye", "goodbye", "exit", "stop",
        "बाय", "बंद हो जाओ"
    ]:
        return "__EXIT__"

    # -----------------------------
    # Remember User Name
    # -----------------------------
    if (
        "my name is" in text
        or "माय नेम इस" in text
        or "mera naam" in text
        or "मेरा नाम" in text
    ):

        name = (
            text.replace("my name is", "")
                .replace("माय नेम इस", "")
                .replace("mera naam", "")
                .replace("मेरा नाम", "")
                .replace("है", "")
                .strip()
        )

        if name:
            remember("name", name)
            return f"Nice to meet you {name}. I will remember your name."

    # -----------------------------
    # Recall User Name
    # -----------------------------
    if (
        "what is my name" in text
        or "व्हाट इस माय नेम" in text
        or "mera naam kya hai" in text
        or "मेरा नाम क्या है" in text
        or "mera naam" == text
        or "नाम क्या है" in text
    ):

        name = recall("name")

        if name:
            return f"Your name is {name}."

        return "I don't know your name yet."

    # -----------------------------
    # Windows Commands
    # -----------------------------
    result = execute(text)

    if result is not None:
        return result

    # -----------------------------
    # AI Reply
    # -----------------------------
    reply = get_reply(text)

    remember_conversation(text, reply)

    return reply