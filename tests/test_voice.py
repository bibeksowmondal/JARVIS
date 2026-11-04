
import pyttsx3

engine = pyttsx3.init("sapi5")

voices = engine.getProperty("voices")

print("Available voices:")
for i, voice in enumerate(voices):
    print(i, voice.name, voice.id)

engine.setProperty("voice", voices[1].id if len(voices) > 1 else voices[0].id)
engine.setProperty("rate", 165)
engine.setProperty("volume", 1.0)

print("Speaking test...")

engine.say("Hello Bibek. JARVIS voice output is working.")
engine.runAndWait()

print("Speech test finished.")
engine.stop()
