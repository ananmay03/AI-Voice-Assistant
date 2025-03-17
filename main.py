import speech_recognition as sr
import ollama
import pyttsx3

# Initialize Text-to-Speech
engine = pyttsx3.init()

def recognize_speech():
    recognizer = sr.Recognizer()
    mic_index = 1  # Your default mic

    with sr.Microphone(device_index=mic_index) as source:
        print("Listening for 'Hey Mistral'...")

        while True:  # Keep listening without timeout
            recognizer.adjust_for_ambient_noise(source, duration=0.5)  # Adjust for noise
            audio = recognizer.listen(source)

            try:
                text = recognizer.recognize_google(audio).lower()
                print(f"You said: {text}")

                if "hey mistral" in text:
                    print("Wake word detected! Listening for command...")
                    return listen_for_command(recognizer, source)  # Listen for next phrase

            except sr.UnknownValueError:
                continue  # Ignore unrecognized sounds
            except sr.RequestError:
                print("Error: Could not access speech recognition service.")
                return None

def listen_for_command(recognizer, source):
    """Listens for a command after 'Hey Mistral' is detected."""
    print("Listening for your command...")
    recognizer.adjust_for_ambient_noise(source, duration=0.5)
    audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"Command: {command}")
        return command
    except sr.UnknownValueError:
        print("Didn't catch that. Say it again.")
        return None

def get_mistral_response(user_input):
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": user_input}])
        return response['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I encountered an error."

def speak_response(response_text):
    engine.say(response_text)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
        user_input = recognize_speech()  # Waits until "Hey Mistral" is detected
        if user_input:
            ai_response = get_mistral_response(user_input)
            print(f"AI: {ai_response}")
            speak_response(ai_response)
