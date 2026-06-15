import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("--- My Available Models ---")
try:
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            # This strips 'models/' prefix so you see the raw string name
            print(model.name.replace('models/', ''))
except Exception as e:
    print(f"Error connecting: {e}")