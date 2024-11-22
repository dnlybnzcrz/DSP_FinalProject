import streamlit as st
from gtts import gTTS
import os
import mysql.connector
import speech_recognition as sr

# Database connection
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)

mycursor = mydb.cursor()


class SoundEncryptionDecryptionProgram:
    def __init__(self):
        self.codes = {
            'a': 'z', 'b': 'x', 'c': 'y', 'd': 's', 'e': 'u', 'f': 'a',
            'g': 'e', 'h': 'c', 'i': 'k', 'j': 'r', 'k': 'n', 'l': 'g',
            'm': 'd', 'n': 'l', 'o': 'm', 'p': 't', 'q': 'f', 'r': 'i',
            's': 'h', 't': 'o', 'u': 'j', 'v': 'p', 'w': 'v', 'x': 'b',
            'y': 'w', 'z': 'q'
        }
        self.list_1 = []
        self.list_2 = []
        self.r = sr.Recognizer()
        self.dec1 = []
        self.dec2 = []

    def encryption(self, input_text):
        x = input_text.split(" ")
        inverse_text = x[::-1]
        z = ""

        for word in inverse_text:
            z += "".join(reversed(word)) + " "

        for i in z:
            self.list_1.append(i)

        for char in self.list_1:
            if char != ' ':
                for key in self.codes.keys():
                    if key in char:
                        self.list_2.append(self.codes.get(key))
            else:
                self.list_2.append("/s")

        encrypt = ""
        for item in self.list_2:
            if item == "/s":
                encrypt += " "
            else:
                encrypt += item

        return encrypt

    def decryption(self, encrypted_text):
        z = list(encrypted_text)
        for char in z:
            if char != " ":
                if char in self.codes.values():
                    self.dec1.append(
                        list(self.codes.keys())[list(self.codes.values()).index(char)]
                    )
            else:
                self.dec1.append("/s")

        decrypted_text = ""
        for item in self.dec1:
            if item == "/s":
                decrypted_text += " "
            else:
                decrypted_text += item

        reversed_words = decrypted_text.split(" ")
        rev = reversed_words[::-1]
        final_text = ""

        for word in rev:
            final_text += "".join(reversed(word)) + " "

        return final_text.strip()


# Initialize Streamlit app
st.set_page_config(page_title="Sound Encryption & Decryption", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox("Choose an action:", ["Home", "Encrypt Text", "Decrypt Text"])

st.sidebar.title("About")
st.sidebar.info("This app allows you to encrypt and decrypt text using custom mappings and save the result as an audio file.")

# Main section
st.title("🔒 Sound Encryption & Decryption App")

program = SoundEncryptionDecryptionProgram()

if app_mode == "Home":
    st.header("Welcome to the Sound Encryption & Decryption App!")
    st.write("""
    - Encrypt your text securely.
    - Decrypt encrypted messages.
    - Generate audio files for the encrypted or decrypted text.
    """)
    st.image("https://via.placeholder.com/800x400?text=Encryption+App", use_column_width=True)

elif app_mode == "Encrypt Text":
    st.header("Text Encryption")
    input_text = st.text_area("Enter the text you want to encrypt:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Encrypt"):
            if input_text:
                encrypted_text = program.encryption(input_text.lower())
                st.success(f"🔐 Encrypted Text: {encrypted_text}")

                # Save as audio
                if st.checkbox("Generate audio file"):
                    tts = gTTS(text=encrypted_text, lang='en')
                    tts.save("encrypted.mp3")
                    st.audio("encrypted.mp3", format="audio/mp3")
                    st.write("Audio file saved as `encrypted.mp3`.")
            else:
                st.warning("Please enter text to encrypt.")

elif app_mode == "Decrypt Text":
    st.header("Text Decryption")
    encrypted_text = st.text_area("Enter the encrypted text:")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Decrypt"):
            if encrypted_text:
                decrypted_text = program.decryption(encrypted_text)
                st.success(f"🔓 Decrypted Text: {decrypted_text}")

                # Save as audio
                if st.checkbox("Generate audio file"):
                    tts = gTTS(text=decrypted_text, lang='en')
                    tts.save("decrypted.mp3")
                    st.audio("decrypted.mp3", format="audio/mp3")
                    st.write("Audio file saved as `decrypted.mp3`.")
            else:
                st.warning("Please enter encrypted text to decrypt.")
