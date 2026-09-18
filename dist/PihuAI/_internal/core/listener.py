import speech_recognition as sr
import time
import core.voice

# 1. रिकॉग्नाइज़र को ग्लोबली एक ही बार इनिशियलाइज़ करें
r = sr.Recognizer()

# 2. माइक की संवेदनशीलता को स्टेबल और फिक्स रखें
r.energy_threshold = 280            # हल्की आवाज़ भी आसानी से पकड़ेगा
r.dynamic_energy_threshold = False  # ऑटो-एडजस्ट बंद ताकि माइक बहरा न हो
r.pause_threshold = 0.8             # बोलने के तुरंत बाद प्रोसेस करे (तेज़ रिस्पॉन्स)
r.non_speaking_duration = 0.3

# 3. सिर्फ ऐप स्टार्ट होने पर एक बार नॉइज़ कैलिब्रेट करें
_mic_calibrated = False

def _ensure_mic_calibrated():
    global _mic_calibrated
    if not _mic_calibrated:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.6)
            _mic_calibrated = True
        except Exception:
            pass

def listen():
    if getattr(core.voice, 'is_speaking', False):
        time.sleep(0.2)
        return ""

    _ensure_mic_calibrated()

    with sr.Microphone() as source:
        try:
            print("\n🎤 Listening...")
            # timeout=4 से बिना बात के लंबा इंतज़ार नहीं होगा
            audio = r.listen(source, timeout=4, phrase_time_limit=10)

            if getattr(core.voice, 'is_speaking', False):
                return ""

            # Google Speech Recognition (भारतीय इंग्लिश + हिंग्लिश सपोर्ट)
            query = r.recognize_google(audio, language="en-IN")
            print(f"👤 You said: '{query}'")
            return query.lower().strip()

        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except Exception as e:
            return ""

def wait_for_wake_word():
    _ensure_mic_calibrated()
    
    with sr.Microphone() as source:
        while True:
            if getattr(core.voice, 'is_speaking', False):
                time.sleep(0.2)
                continue
            try:
                # वेक-वर्ड के लिए छोटा लिसन विंडो
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
                wake = r.recognize_google(audio, language="en-IN").lower().strip()
                
                # मिस-हियरिंग को भी हैंडल करें (जैसे piyush, pehu, hey pi)
                wake_variants = [
                    "pihu", "hey pihu", "hello pihu", "sun pihu",
                    "pehu", "piyush", "hey pi"
                ]
                if any(w in wake for w in wake_variants):
                    print(f"⚡ Wake word detected: '{wake}'")
                    return True
            except (sr.WaitTimeoutError, sr.UnknownValueError):
                continue
            except Exception:
                time.sleep(0.1)
                continue