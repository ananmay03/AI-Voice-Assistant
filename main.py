import speech_recognition as sr
import google.generativeai as genai
import pyttsx3
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the correct model from your available list
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# Initialize Text-to-Speech
engine = pyttsx3.init()

def recognize_speech():
    recognizer = sr.Recognizer()
    mic_index = 1  # Your default microphone index

    with sr.Microphone(device_index=mic_index) as source:
        print(f"Using microphone: {sr.Microphone.list_microphone_names()[mic_index]}")
        print("Adjusting for background noise... Speak now!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio. Try speaking louder.")
            return None
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")
            return None

def get_gemini_response(user_input):
    try:
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I encountered an error."


def speak_response(response_text):
    engine.say(response_text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        user_input = recognize_speech()
        if user_input:
            ai_response = get_gemini_response(user_input)
            print(f"AI: {ai_response}")
            speak_response(ai_response)
