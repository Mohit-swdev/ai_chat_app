from google import genai
import os
from dotenv import load_dotenv

# Force load from current directory
load_dotenv(dotenv_path=".env")

print("API KEY:", os.getenv("GOOGLE_API_KEY"))

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

response = client.models.generate_content(
    model="gemini-flash-latest",
    contents="Explain recursion in simple terms"
)

print(response.text)