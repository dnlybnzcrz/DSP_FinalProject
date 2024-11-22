import streamlit as st
from gtts import gTTS
import sounddevice as sd
import scipy.io.wavfile as wav
import speech_recognition as sr
import numpy as np

# Record audio using sounddevice
def record_audio(duration=5, samplerate=44100):
    st.info("🎙️ Recording... Speak now!")
    audio = sd.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    st.success("Recording complete!")
    return samplerate, audio

# Save recorded audio
def save_audio(filename, samplerate, audio):
    wav.write(filename, samplerate, audio)

# Streamlit App
st.title("🔊 Speech to Text with Playback")

# Step 1: Record Speech
if st.button("Record Speech"):
    duration = st.slider("Select duration (seconds):", min_value=1, max_value=10, value=5)
    samplerate, audio = record_audio(duration)
    save_audio("recorded_audio.wav", samplerate, audio)
    st.audio("recorded_audio.wav", format="audio/wav")
    st.write("🎧 Listen to the recorded speech above.")

    # Step 2: Detect Speech
    recognizer = sr.Recognizer()
    with sr.AudioFile("recorded_audio.wav") as source:
        audio_data = recognizer.record(source)
        try:
            detected_text = recognizer.recognize_google(audio_data)
            st.success(f"🗣️ Detected Speech: {detected_text}")

            # Save detected speech as audio
            tts = gTTS(text=detected_text, lang="en")
            tts.save("detected_speech.mp3")
            st.audio("detected_speech.mp3", format="audio/mp3")
            st.write("🎧 Listen to the detected speech above.")
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("❌ Could not request results from Google Speech Recognition.")
