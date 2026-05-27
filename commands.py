import webbrowser
import musicLibrary
import newsAPI
from speak import speak
from client import ask_jarvis


def processCommand(c):
    if "open youtube" in c.lower():
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        return True
    elif "open google" in c.lower():
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        return True
    elif "open instagram" in c.lower():
        speak("Opening Instagram")
        webbrowser.open("https://www.instagram.com")
        return True
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split(" ")[1]
            link = musicLibrary.music[song]
            webbrowser.open(link)
            return True
        except:
            speak("Couldn't find song")
            print("Couldn't find song")
            return True
    elif "news" in c.lower():
        if newsAPI.response.status_code == 200:
            data = newsAPI.response.json()
            articles = data.get("articles", [])

            for article in articles[:3]:
                title = article.get("title")
                link = article.get("url")

                print("Opening:", title)
                webbrowser.open(link)
        else:
            speak("Couldn't find news")

        return True

    return False










