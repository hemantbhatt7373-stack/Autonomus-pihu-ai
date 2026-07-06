import speech_recognition as sr

recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8
recognizer.non_speaking_duration = 0.5


def listen():
    with sr.Microphone() as source:

        print("🎤 Listening...")

        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=10
            )

        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(
            audio,
            language="hi-IN"
        )

        print("Hemant:", text)

        return text.lower().strip()

    except sr.UnknownValueError:
        return ""

    except sr.RequestError:
        print("Internet connection error.")
        return ""

    except Exception as e:
        print(e)
        return ""