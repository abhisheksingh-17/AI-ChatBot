import streamlit as st
import openai
import speech_recognition as sr
from gtts import gTTS
import os

# Set your OpenAI API key here
openai.api_key = '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'

st.title('AI Chatbot')

# Communication mode: Text or Audio
st.sidebar.header("Choose Communication Mode")
communication_mode = st.sidebar.radio('', ('Text', 'Audio'))

# Language selection: Hindi or English
st.sidebar.header("Choose Language")
language = st.sidebar.radio('', ('Hindi', 'English'))

# User and Chatbot icons
user_icon = 'user_icon.png'
bot_icon = 'bot_icon.png'

def generate_response(user_input, language='en'):
    # Call the OpenAI API to generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=user_input,
        max_tokens=150
    )
    return response.choices[0].text.strip()

def convert_speech_to_text(audio_data, language='en'):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_data) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said."
    except sr.RequestError:
        return "Oops! An error occurred while processing your audio."

# Function to display user message with user icon on the left
def display_user_message(message):
    st.markdown('<div style="display: flex; flex-direction: row; margin-bottom: 20px;">'
                f'<img src="{user_icon}" style="width: 50px; height: 50px; border-radius: 50%; margin-right: 10px;" />'
                f'<div style="background-color: #DCF8C6; color: black; border-radius: 15px; padding: 10px;">'
                f'<p style="margin: 0;">{message}</p>'
                '</div></div>',
                unsafe_allow_html=True)

# Function to display chatbot message with chatbot icon on the right
def display_bot_message(message):
    st.markdown('<div style="display: flex; flex-direction: row; justify-content: flex-end; margin-bottom: 20px;">'
                f'<div style="background-color: #007BFF; color: white; border-radius: 15px; padding: 10px;">'
                f'<p style="margin: 0;">{message}</p>'
                '</div>'
                f'<img src="{bot_icon}" style="width: 50px; height: 50px; border-radius: 50%; margin-left: 10px;" />'
                '</div>',
                unsafe_allow_html=True)

if communication_mode == 'Text':
    user_input = st.text_input('You:')
    if st.button('Send'):
        if user_input:
            st.text('You: ' + user_input)

            # Call the OpenAI API to generate a response
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=user_input,
                max_tokens=150
            )
            bot_response = response.choices[0].text.strip()

            st.text('Bot: ' + bot_response)
elif communication_mode == 'Audio':
    audio_data = st.audio('Record your audio message:', format='audio/wav')
    if audio_data:
        st.text('Audio recording complete!')

        audio_file = "user_audio.wav"
        with open(audio_file, "wb") as f:
            f.write(audio_data.read())

        user_audio_text = convert_speech_to_text(audio_file, language=language)
        st.text('You said (audio): ' + user_audio_text)

        # Call the OpenAI API to generate a response
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=user_audio_text,
            max_tokens=150
        )
        bot_response = response.choices[0].text.strip()

        st.text('Bot: ' + bot_response)

        # Clean up the generated audio file after displaying it
        if os.path.exists(audio_file):
            os.remove(audio_file)
