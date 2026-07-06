import asyncio
import edge_tts
import pygame
import os
import time

VOICE = "hi-IN-SwaraNeural"

os.makedirs("temp", exist_ok=True)

pygame.mixer.init()


async def _generate_speech(text):
    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE,
        rate="+5%",
        pitch="+2Hz"
    )

    await communicate.save("temp/voice.mp3")


def speak(text):
    try:

        if not text:
            return

        print("Pihu:", text)

        # Bahut lamba reply avoid karo
        if len(text) > 500:
            text = text[:500]

        filepath = "temp/voice.mp3"

        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except:
                pass

        asyncio.run(_generate_speech(text))

        pygame.mixer.music.load(filepath)

        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            time.sleep(0.05)

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()

        try:
            os.remove(filepath)
        except:
            pass

    except Exception as e:
        print("Voice Error:", e)