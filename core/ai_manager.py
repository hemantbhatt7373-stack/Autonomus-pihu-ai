from core.ai import ask_ai


def get_reply(message):
    """
    AI Manager

    Pehle OpenRouter AI try karega.
    Agar koi error aaye to offline replies dega.
    """

    try:
        return ask_ai(message)

    except Exception as e:
        print("AI Error:", e)

    text = message.lower().strip()

    # Greetings
    if any(x in text for x in [
        "hello", "hi", "hey",
        "हेलो", "हाय"
    ]):
        return "Hello Hemant! 😊 Main Pihu hoon."

    # How are you
    if any(x in text for x in [
        "how are you",
        "kaise ho",
        "कैसे हो"
    ]):
        return "Main bilkul theek hoon. Tum kaise ho?"

    # Thanks
    if any(x in text for x in [
        "thank", "thanks", "thank you",
        "shukriya", "धन्यवाद"
    ]):
        return "You're welcome Hemant. 😊"

    # Bye
    if any(x in text for x in [
        "bye", "goodbye", "exit", "stop"
    ]):
        return "Goodbye Hemant."

    # Default
    return "Sorry Hemant, mujhe iska jawab nahi pata."