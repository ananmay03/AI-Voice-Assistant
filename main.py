import pvporcupine
import pyaudio
import struct
import ollama
import pyttsx3
import speech_recognition as sr

# 🔹 Initialize Text-to-Speech
engine = pyttsx3.init()

# 🔹 Load Porcupine wake word detector
porcupine = pvporcupine.create(
    access_key="4MwfdyeJf8ipi3rHAxin8hNblKy4KeLyodxE0FwnmyO+Qsso8mNiiA==",  # Replace with your Picovoice API key
    keyword_paths=["hey_mistral.ppn"]  # Ensure this file is in the project folder
)

# 🔹 Audio setup
pa = pyaudio.PyAudio()
audio_stream = pa.open(
    rate=porcupine.sample_rate,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=porcupine.frame_length
)

def listen_for_commands():
    """Listens for commands continuously until user says 'bye' or similar exit phrases."""
    recognizer = sr.Recognizer()
    mic_index = 1  # Your default mic

    with sr.Microphone(device_index=mic_index) as source:
        print("Listening for commands... Say 'bye' to exit.")

        while True:
            recognizer.adjust_for_ambient_noise(source, duration=1)  # Adjust for better recognition
            print("Start speaking...")

            audio = recognizer.listen(source, timeout=None, phrase_time_limit=10)

            try:
                command = recognizer.recognize_google(audio).lower().strip()
                print(f"You said: {command}")

                exit_phrases = ["bye", "bye bye", "okay bye", "ok thanks", "goodbye", "see you"]
                if any(phrase in command for phrase in exit_phrases):  # Check if any exit phrase is in command
                    print("Goodbye! Stopping assistant.")
                    speak_response("Goodbye!")
                    exit(0)  # Forcefully stop execution

                ai_response = get_mistral_response(command)
                print(f"AI: {ai_response}")
                speak_response(ai_response)

            except sr.UnknownValueError:
                print("Didn't catch that. Say it again.")
            except sr.RequestError:
                print("Could not request results. Check your internet connection.")



def get_mistral_response(user_input):
    """Gets AI-generated response from Mistral."""
    try:
        response = ollama.chat(model="mistral", messages=[{"role": "user", "content": user_input}])
        return response['message']['content']
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I encountered an error."

def speak_response(response_text):
    """Speaks out the AI-generated response."""
    engine.say(response_text)
    engine.runAndWait()

def detect_wake_word():
    """Listens for 'Hey Mistral' using Porcupine and keeps listening for follow-ups."""
    print("Listening for 'Hey Mistral'...")

    while True:
        pcm = audio_stream.read(porcupine.frame_length)
        pcm_unpacked = struct.unpack_from("h" * porcupine.frame_length, pcm)

        keyword_index = porcupine.process(pcm_unpacked)
        if keyword_index >= 0:
            print("Wake word detected! Now listening for commands...")
            speak_response("Yes? I'm listening.")
            listen_for_commands()  # Now continuously listens until exit command

if __name__ == "__main__":
    detect_wake_word()  # Start wake-word detection
