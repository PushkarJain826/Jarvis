import sounddevice as sd
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
import os


# Load Whisper model
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)


def listen():

    samplerate = 16000
    duration = 5

    print("Listening...")

    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=1,
        dtype='int16'
    )

    sd.wait()

    temp_audio = "temp_audio.wav"

    write(temp_audio, samplerate, audio)

    segments, info = model.transcribe(temp_audio)

    text = ""

    for segment in segments:
        text += segment.text

    os.remove(temp_audio)

    return text.strip()