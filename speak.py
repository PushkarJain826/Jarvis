import asyncio
import edge_tts
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import time
import os


VOICE = "en-GB-RyanNeural"

pygame.mixer.init()


async def generate_voice(text):

    communicate = edge_tts.Communicate(
        text=text,
        voice=VOICE
    )

    await communicate.save("voice.mp3")


def speak(text, tim=0.5):

    asyncio.run(generate_voice(text))
    time.sleep(tim)
    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    pygame.mixer.music.unload()

    os.remove("voice.mp3")