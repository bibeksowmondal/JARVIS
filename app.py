
import os
import speech_recognition as sr
import pyttsx3

from dotenv import load_dotenv
from google import genai
from google.genai import types

from automation.applications import open_application, open_website


# ==================================================
# 1. CONFIGURATION
# ==================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )


# ==================================================
# 2. GEMINI AI
# ==================================================

client = genai.Client(
    api_key=api_key,
    http_options=types.HttpOptions(
        timeout=15000,
        retry_options=types.HttpRetryOptions(attempts=1),
    ),
)

MODEL = "gemini-3.5-flash"

INSTRUCTIONS = """
You are JARVIS, a personal AI assistant.
Answer clearly and concisely.
Use short spoken responses unless more detail is requested.
Help with programming, learning, and productivity.
Never claim to have performed an action that was not executed.
"""

previous_interaction_id = None


# ==================================================
# 3. MICROPHONE
# ==================================================

recognizer = sr.Recognizer()
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.8

MICROPHONE_INDEX = 1


# ==================================================
# 4. TEXT-TO-SPEECH
# ==================================================

speaker = pyttsx3.init("sapi5")

voices = speaker.getProperty("voices")

if voices:
    voice_index = 1 if len(voices) > 1 else 0
    speaker.setProperty("voice", voices[voice_index].id)

speaker.setProperty("rate", 165)
speaker.setProperty("volume", 1.0)


def speak(text):
    """Print and speak text using Windows SAPI5."""

    text = str(text).strip()

    if not text:
        text = "I did not receive a response."

    print(f"\nJARVIS: {text}\n", flush=True)

    try:
        

        # Ensure the response is passed as a string.
        speaker.say(text)

        # Process the speech queue and wait until playback finishes.
        speaker.runAndWait()

        print("[TTS] Speech playback finished.", flush=True)

    except Exception as error:
        print(f"[TTS ERROR] {error}", flush=True)


# ==================================================
# 5. SPEECH RECOGNITION
# ==================================================

def listen():
    """Capture speech and convert it to text."""

    try:
        with sr.Microphone(
            device_index=MICROPHONE_INDEX
        ) as source:

            print("Calibrating microphone...", flush=True)

            recognizer.adjust_for_ambient_noise(
                source,
                duration=0.5,
            )

            print("Listening...", flush=True)

            audio = recognizer.listen(
                source,
                timeout=8,
                phrase_time_limit=15,
            )

        print("Recognizing speech...", flush=True)

        question = recognizer.recognize_google(
            audio,
            language="en-IN",
        )

        print(f"\nYou: {question}", flush=True)

        return question

    except sr.WaitTimeoutError:
        print("No speech detected. Try again.", flush=True)

    except sr.UnknownValueError:
        print("Could not understand the audio.", flush=True)

    except sr.RequestError as error:
        print(f"Speech recognition error: {error}", flush=True)

    except OSError as error:
        print(f"Microphone error: {error}", flush=True)

    return None


# ==================================================
# 6. GEMINI RESPONSE
# ==================================================

def ask_jarvis(question):
    """Send a question to Gemini and preserve conversation context."""

    global previous_interaction_id

    params = {
        "model": MODEL,
        "input": question,
        "system_instruction": INSTRUCTIONS,
    }

    if previous_interaction_id:
        params["previous_interaction_id"] = previous_interaction_id

    try:
        print("[AI] Sending question to Gemini...", flush=True)

        response = client.interactions.create(**params)

        previous_interaction_id = response.id

        answer = response.output_text

        if answer is None or not str(answer).strip():
            print("[AI] Gemini returned no text.", flush=True)
            return "I received an empty response. Please try again."

        answer = str(answer).strip()

        print("[AI] Gemini response received.", flush=True)
        print(f"[AI] Response length: {len(answer)} characters.", flush=True)

        return answer

    except Exception as error:
        print(f"[AI ERROR] {type(error).__name__}: {error}", flush=True)

        return (
            "Sorry, I could not get an answer from the AI service. "
            "Please check your internet connection and try again."
        )


# ==================================================
# 7. COMPUTER AUTOMATION
# ==================================================

def handle_computer_command(question):
    """Execute only approved local application and website commands."""

    text = question.lower().strip()

    if text.startswith("jarvis"):
        text = text[len("jarvis"):].strip(" ,.!")

    # Approved Windows applications.
    for app in ("notepad", "calculator", "paint"):
        if text in (
            f"open {app}",
            f"launch {app}",
            f"start {app}",
        ):
            return open_application(app)

    # Approved websites.
    for site in ("google", "youtube", "github"):
        if text in (
            f"open {site}",
            f"open {site} website",
        ):
            return open_website(site)

    return None


# ==================================================
# 8. MAIN LOOP
# ==================================================

def main():

    print("=" * 48)
    print("          JARVIS VOICE ASSISTANT")
    print("=" * 48)
    print("Press Enter to use your microphone.")
    print("Type /text to enter a question.")
    print("Type exit to close JARVIS.")
    print("=" * 48)

    speak("Hello. JARVIS is online.")

    while True:
        try:
            command = input(
                "\nPress Enter to speak, /text, or exit: "
            ).strip()

            if command.lower() in {"exit", "quit"}:
                speak("Goodbye. Shutting down.")
                break

            if command.lower() == "/text":
                question = input("You: ").strip()
            else:
                question = listen()

            if not question:
                continue

            if question.lower() in {"exit", "quit"}:
                speak("Goodbye.")
                break

            # Run an approved computer command if applicable.
            result = handle_computer_command(question)

            if result is not None:
                speak(result)
                continue

            # Otherwise, obtain an answer from Gemini.
            print("[JARVIS] Thinking...", flush=True)

            answer = ask_jarvis(question)

            # Send the actual Gemini answer to text-to-speech.
            speak(answer)

        except (KeyboardInterrupt, EOFError):
            print("\nJARVIS shutting down.", flush=True)
            break

        except Exception as error:
            print(
                f"[MAIN ERROR] {type(error).__name__}: {error}",
                flush=True,
            )


# ==================================================
# 9. START APPLICATION
# ==================================================

if __name__ == "__main__":
    main()
