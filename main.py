from config import APP_NAME, VERSION
from core.voice import speak
from core.listener import listen
from brain.router import process


def main():
    print("=" * 50)
    print(APP_NAME)
    print("Version:", VERSION)
    print("=" * 50)

    speak("Hello Hemant. I am Pihu. How can I help you?")

    while True:

        text = listen()

        if not text:
            continue

        print("You:", text)

        reply = process(text)

        if reply == "__EXIT__":
            speak("Goodbye Hemant. Have a nice day.")
            break

        print("Pihu:", reply)

        speak(reply)


if __name__ == "__main__":
    main()