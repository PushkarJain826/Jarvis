import speech_recognition as sr 
r = sr.Recognizer()
r.pause_threshold = 2
r.energy_threshold = 300

with sr.Microphone() as source:

    print("Listening...")
    audio = r.listen(source, timeout=10, phrase_time_limit=10)
    text = r.recognize_google(audio)
    print("You said:", text)