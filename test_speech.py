from speech.speech_to_text import listen

try:
    text = listen()
    print("You said:", text)

except Exception as e:
    print("ERROR:")
    print(e)