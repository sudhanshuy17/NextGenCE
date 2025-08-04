import os
import base64
import tempfile
from gtts import gTTS
import whisper
import streamlit as st

class VoiceSystem:
    def __init__(self):
        # Load Whisper model for speech-to-text
        self.stt_model = whisper.load_model("base")

    def text_to_speech(self, text, lang='en'):
        """Convert text to speech using gTTS and return the audio file path."""
        try:
            tts = gTTS(text=text, lang=lang, slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                return fp.name
        except Exception as e:
            raise Exception(f"Text-to-speech error: {str(e)}")

    def speech_to_text(self, audio_path):
        """Convert speech to text using Whisper and return the transcribed text."""
        try:
            result = self.stt_model.transcribe(audio_path)
            return result["text"]
        except Exception as e:
            raise Exception(f"Speech-to-text error: {str(e)}")

    def autoplay_audio(self, file_path):
        """Auto-play audio in Streamlit using HTML."""
        with open(file_path, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            audio_html = f"""
                <audio autoplay>
                <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
            """
            st.markdown(audio_html, unsafe_allow_html=True)

    def record_audio(self, label="Record your message", key="audio_recorder"):
        """Record audio from the user in Streamlit and return the file path."""
        audio_bytes = st.file_uploader(label, type=["wav", "mp3"], key=key)
        if audio_bytes is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as fp:
                fp.write(audio_bytes.read())
                return fp.name
        return None

# Example usage in Streamlit:
# voice = VoiceSystem()
# audio_file = voice.record_audio()
# if audio_file:
#     text = voice.speech_to_text(audio_file)
#     st.write("You said:", text)
#     tts_file = voice.text_to_speech("Hello, this is a test.")
#     voice.autoplay_audio(tts_file)