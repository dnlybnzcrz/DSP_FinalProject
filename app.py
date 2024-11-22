import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import os


def get_speech_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙️ Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            st.success("✅ Speech recorded successfully!")
            return audio
        except sr.UnknownValueError:
            st.error("❌ Could not understand the audio.")
        except sr.RequestError:
            st.error("❌ Could not request results from Google Speech Recognition.")
        except Exception as e:
            st.error(f"❌ An error occurred: {e}")
        return None


def recognize_speech(audio):
    recognizer = sr.Recognizer()
    try:
        text = recognizer.recognize_google(audio)
        st.success(f"🗣️ Detected Speech: {text}")
        return text
    except sr.UnknownValueError:
        st.error("❌ Could not understand the audio.")
    except sr.RequestError:
        st.error("❌ Could not request results from Google Speech Recognition.")
    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
    return None


st.title("🔊 Speech to Text with Playback")

# Step 1: Record Speech
if st.button("Record Speech"):
    audio = get_speech_input()
    if audio:
        # Save the recorded audio for playback
        with open("recorded_audio.wav", "wb") as f:
            f.write(audio.get_wav_data())
        st.audio("recorded_audio.wav", format="audio/wav")
        st.write("🎧 Listen to the recorded speech above.")

        # Step 2: Detect Speech
        detected_text = recognize_speech(audio)
        if detected_text:
            # Save detected speech as audio
            tts = gTTS(text=detected_text, lang="en")
            tts.save("detected_speech.mp3")
            st.audio("detected_speech.mp3", format="audio/mp3")
            st.write("🎧 Listen to the detected speech above.")
