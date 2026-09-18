import os
import re
import uuid
import time
import asyncio
import pygame
import edge_tts

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

# 🌟 डिफ़ॉल्ट False
is_speaking = False

VOICE = "hi-IN-SwaraNeural"
PITCH = "+28Hz"
RATE = "+2%"

os.makedirs("temp", exist_ok=True)

offline_engine = None
if pyttsx3 is not None:
    try:
        offline_engine = pyttsx3.init()
        offline_engine.setProperty('rate', 190)
        voices = offline_engine.getProperty('voices')
        for v in voices:
            if "female" in v.name.lower() or "zira" in v.name.lower() or "hindi" in v.name.lower():
                offline_engine.setProperty('voice', v.id)
                break
    except Exception:
        offline_engine = None

def ensure_mixer():
    if not pygame.mixer.get_init():
        try:
            pygame.mixer.pre_init(24000, -16, 2, 512)
            pygame.mixer.init()
        except Exception:
            pass

async def generate(clean_text, filename):
    communicate = edge_tts.Communicate(
        text=clean_text,
        voice=VOICE,
        pitch=PITCH,
        rate=RATE
    )
    await communicate.save(filename)

def speak(text):
    global is_speaking
    if not text or not str(text).strip():
        return
    
    # नोट: ऑडियो बनने से पहले is_speaking को False ही रखेंगे
    is_speaking = False
    filename = os.path.abspath(os.path.join("temp", f"{uuid.uuid4().hex}.mp3"))
    
    try:
        ensure_mixer()
        clean_text = re.sub(r'[*#_~`>]', '', str(text)).strip()
        print(f"🤖 Pihu: {clean_text}")
        
        # 1. पहले ऑडियो फ़ाइल डाउनलोड होने दें
        try:
            asyncio.run(generate(clean_text, filename))

            if os.path.exists(filename):
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                
                # 🌟 ठीक ऑडियो शुरू होने पर ही is_speaking = True होगा
                is_speaking = True
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.01)
                    
                pygame.mixer.music.unload()
        except Exception:
            # 2. ऑफ़लाइन बैकअप
            if offline_engine:
                is_speaking = True
                offline_engine.say(clean_text)
                offline_engine.runAndWait()
    
    except Exception as e:
        print(f"Voice Error: {e}")
    finally:
        # बोलना खत्म होते ही तुरंत False
        is_speaking = False
        
        if os.path.exists(filename):
            try:
                os.remove(filename)
            except Exception:
                pass

if __name__ == "__main__":
    speak("Hello Boss! Main Pihu hu, bataiye main aapke liye kya karu?")