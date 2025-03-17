import speech_recognition as sr

def recognize_speech():
    recognizer = sr.Recognizer()
    mic_index = 1  # Change this if needed

    with sr.Microphone(device_index=mic_index) as source:
        print(f"Using microphone: {sr.Microphone.list_microphone_names()[mic_index]}")
        print("Adjusting for background noise... Speak now!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=5)

        try:
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand the audio. Try speaking louder.")
        except sr.RequestError:
            print("Could not request results. Check your internet connection.")

if __name__ == "__main__":
    recognize_speech()
