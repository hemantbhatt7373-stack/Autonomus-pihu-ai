from core.ai import ask_ai

print("AI Manager Loaded")


def get_reply(message):
    """
    AI Manager

    1. Pehle Gemini try karega.
    2. Agar Gemini fail ho jaye to Offline Brain reply dega.
    """

    try:
        return ask_ai(message)

    except Exception as e:
        print("Offline Mode:", e)

    text = message.lower().strip()

    # Greetings
    if any(x in text for x in [
        "hello", "hi", "hey", "helo",
        "हेलो", "हाय"
    ]):
        return "Hello Hemant! 😊 Main Pihu hoon. Batao main kya help kar sakti hoon?"

    # How are you
    if any(x in text for x in [
        "how are you",
        "kaise ho",
        "कैसे हो"
    ]):
        return "Main bilkul theek hoon. Tum kaise ho?"

    # Thanks
    if any(x in text for x in [
        "thank",
        "thanks",
        "thank you",
        "shukriya",
        "धन्यवाद"
    ]):
        return "You're most welcome Hemant. 😊"

    # Who are you
    if any(x in text for x in [
        "who are you",
        "tum kaun ho",
        "तुम कौन हो"
    ]):
        return "Main Pihu hoon. Tumhari personal AI assistant."

    # Bye
    if any(x in text for x in [
        "bye",
        "goodbye",
        "exit",
        "stop",
        "बाय"
    ]):
        return "Goodbye Hemant. Apna khayal rakhna."

    # Offline fallback
    return (
        "Mera AI abhi available nahi hai. "
        "Lekin main basic baatein aur commands kar sakti hoon."
    )