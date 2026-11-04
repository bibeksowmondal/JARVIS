
import os
import speech_recognition as sr
import pyttsx3

from dotenv import load_dotenv
from google import genai
from google.genai import types

from automation.browser import browser_controller

from automation.file_manager import (
    initialize_workspace,
    create_folder,
    create_file,
    list_files,
    read_file,
    append_file,
    write_file,
    copy_file,
    move_file,
    rename_file,
    delete_file,
    delete_folder,
)

from automation.applications import (
    open_application,
    close_application,
    minimize_application,
    maximize_application,
    switch_application,
    open_website,
)

from automation.system_monitor import (
    get_cpu_usage,
    get_ram_usage,
    get_battery_status,
    get_disk_usage,
    get_system_info,
    get_system_status
)

pending_file_deletion = None

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
        timeout=50000,
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
recognizer.pause_threshold = 1.0
recognizer.non_speaking_duration = 0.5

MICROPHONE_INDEX = 1

# ==================================================
# 4. TEXT-TO-SPEECH
# ==================================================



def speak(text):
    """Speak JARVIS responses using a fresh SAPI5 engine."""

    text = str(text).strip()

    if not text:
        text = "I did not receive a response."

    print(f"\nJARVIS: {text}\n", flush=True)

    engine = None

    try:
        engine = pyttsx3.init("sapi5")

        voices = engine.getProperty("voices")

        if voices:
            voice_index = 1 if len(voices) > 1 else 0
            engine.setProperty("voice", voices[voice_index].id)

        engine.setProperty("rate", 165)
        engine.setProperty("volume", 1.0)

        engine.say(text)
        engine.runAndWait()

        print("[TTS] Speech completed successfully.", flush=True)

    except Exception as error:
        print(
            f"[TTS ERROR] {type(error).__name__}: {error}",
            flush=True
        )

    finally:
        if engine is not None:
            engine.stop()
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
                timeout=12,
                phrase_time_limit=20,
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
        print(
            f"[AI ERROR] {type(error).__name__}: {error}", 
              flush=True
            )

        return (
            "The AI service is taking too long to respond. "
            "Please try again."
        )


# ==================================================
# 7. COMPUTER AUTOMATION
# ==================================================


def handle_computer_command(question):

    text = question.lower().strip()

    if text.startswith("jarvis"):
        text = text[len("jarvis"):].strip(" ,.!")

    # Normalize common voice variations
    text = text.replace("the ", "")

    print(f"[COMMAND ROUTER] Detected: {text}", flush=True)

    # ==========================================
    # APPLICATION AUTOMATION
    # ==========================================

    # Open applications
    for app in ("notepad", "calculator", "paint"):

        if text in (
            f"open {app}",
            f"launch {app}",
            f"start {app}",
            f"open {app} app"
        ):
            return open_application(app)

    # Close applications
    for app in ("notepad", "calculator", "paint"):

        if text in (f"close {app}", f"exit {app}"):
            return close_application(app)

    # Minimize applications
    for app in ("notepad", "calculator", "paint"):

        if text in (f"minimize {app}", f"hide {app}"):
            return minimize_application(app)

    # Maximize applications
    for app in ("notepad", "calculator", "paint"):

        if text == f"maximize {app}":
            return maximize_application(app)

    # Switch applications
    for app in ("notepad", "calculator", "paint"):

        if text in (f"switch to {app}", f"focus {app}"):
            return switch_application(app)

    # ==========================================
    # GOOGLE CHROME AUTOMATION
    # ==========================================

    # Open Chrome
    if text in (
        "open chrome",
        "launch chrome",
        "start chrome",
        "open google chrome"
    ):
        return browser_controller.open_browser()

    # Close Chrome
    if text in (
        "close chrome",
        "close google chrome",
        "exit chrome"
    ):
        return browser_controller.close_browser()

    # Open common websites in Chrome
    websites = {
        "google": "https://www.google.com",
        "youtube": "https://www.youtube.com",
        "github": "https://github.com",
        "stackoverflow": "https://stackoverflow.com"
    }

    for site, url in websites.items():

        if text in (
            f"open {site}",
            f"open {site} website"
        ):
            return browser_controller.open_url(url)

    # Google search
    if text.startswith("search google for "):

        query = text.replace(
            "search google for ", "", 1
        )

        return browser_controller.google_search(query)

    # YouTube search
    if text.startswith("search youtube for "):

        query = text.replace(
            "search youtube for ", "", 1
        )

        return browser_controller.youtube_search(query)

    # General Google search
    if text.startswith("search for "):

        query = text.replace(
            "search for ", "", 1
        )

        return browser_controller.google_search(query)

    # Open a custom website
    if text.startswith("open website "):

        address = text.replace(
            "open website ", "", 1
        )

        return browser_controller.open_url(address)

    # Browser tabs
    if text in (
        "open new tab",
        "new tab",
        "open a new tab"
    ):
        return browser_controller.new_tab()

    if text in (
        "close tab",
        "close browser tab"
    ):
        return browser_controller.close_tab()

    # Browser navigation
    if text in (
        "go back",
        "browser back"
    ):
        return browser_controller.go_back()

    if text in (
        "go forward",
        "browser forward"
    ):
        return browser_controller.go_forward()

    # ==========================================
    # SYSTEM MONITORING - UNCHANGED
    # ==========================================

    if text in ("cpu usage", "check cpu", "cpu status"):
        return get_cpu_usage()

    if text in ("ram usage", "memory usage", "check ram"):
        return get_ram_usage()

    if text in ("battery status", "check battery"):
        return get_battery_status()

    if text in ("disk usage", "storage status", "check storage"):
        return get_disk_usage()

    if text in ("system information", "computer information"):
        return get_system_info()

    if text in ("system status", "computer status", "full system status"):
        return get_system_status()

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
