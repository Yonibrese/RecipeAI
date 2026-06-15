import json
import google.generativeai as genai
from django.conf import settings

# Configure the SDK with your loaded settings key
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_ai_recipe(ingredients_input):
    """
    Sends raw text ingredients to Gemini and returns a structured dictionary
    matching the Django Recipe model layout.
    """
    model = genai.GenerativeModel("gemini-3.5-flash")
    prompt = f"""
    You are a professional chef. A user has the following ingredients in their fridge: {ingredients_input}.
    Generate a creative, delicious recipe that utilizes these ingredients. Please adhear to orthox kosher dietary laws. 
    
    You MUST respond with a single, valid JSON object matching this exact structure:
    {{
        "title": "Name of the recipe",
        "description": "A short 1-2 sentence description of the dish",
        "instructions": "Step-by-step instructions separated by newlines",
        "ingredients": [
            {{"name": "Ingredient Name", "quantity": "amount", "unit": "g/ml/tbsp/pcs/etc"}},
            {{"name": "Ingredient Name 2", "quantity": "amount", "unit": "g/ml/tbsp/pcs/etc"}}
        ]
    }}
    Do not wrap the response in markdown blocks like ```json ... ```. Return raw JSON text only.
    """
    try:
        # 3. Call the API forcing JSON output
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # 4. Parse the plain text string into a native Python dictionary
        recipe_data = json.loads(response.text)
        return recipe_data
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return None
    