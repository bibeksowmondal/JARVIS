
import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

key = os.getenv("GEMINI_API_KEY")
if not key:
    raise RuntimeError("GEMINI_API_KEY is missing from .env")

print("1. Initializing Gemini...", flush=True)

client = genai.Client(
    api_key=key,
    http_options={"timeout": 15000}
)

print("2. Sending test request...", flush=True)
start = time.time()

try:
    response = client.interactions.create(
        model="gemini-3.5-flash",
        input="Reply with exactly: JARVIS ONLINE",
    )

    print(f"3. Response received in {time.time() - start:.1f}s")
    print("JARVIS:", response.output_text, flush=True)

except Exception as error:
    print(f"Request failed after {time.time() - start:.1f}s")
    print(type(error).__name__, str(error), flush=True)

