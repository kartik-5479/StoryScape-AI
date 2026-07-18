from gtts import gTTS
import os


def generate_audio(text):
    os.makedirs("assets/audio", exist_ok=True)

    file_path = "assets/audio/story.mp3"

    tts = gTTS(text=text, lang="en")
    tts.save(file_path)

    return file_path