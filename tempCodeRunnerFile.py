import threading
import asyncio
from commands import processCommand
from speech.speech_to_text import listen
from speak import speak
from client import ask_jarvis
from LLMs.browser_llm import browser_agent as browser
from bridge.browser_bridge import start_bridge


def run_bridge():
    """Runs the WebSocket bridge server in a background thread."""
    asyncio.run(start_bridge())


if __name__ == "__main__":

    # Start bridge server silently in background
    bridge_thread = threading.Thread(target=run_bridge, daemon=True)
    bridge_thread.start()

    speak("Initializing Jarvis.")
    speak("At your service, sir. How can I help you?")
    print("Calibrating...")

    while True:
        try:
            print("How can I help you?")
            print("Listening...")

            command = listen()
            handled = browser(command)

            if handled:
                print(f"[Jarvis] Browser handled: {command}")
            else:
                response = ask_jarvis(command)
                speak(response)

        except Exception as e:
            print(e)