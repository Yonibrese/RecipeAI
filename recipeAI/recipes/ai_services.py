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
        "category": "A short 1-3 word category name (e.g., Chicken Main, Soup, Appetizer, Pasta, Vegetarian)"
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

def professionalize_instructions(raw_text):
    """
    Sends raw, messy instructions to Gemini and asks for a professional, 
    formatted rewrite. Returns plain text.
    """
    # Use the same active model you found during the diagnosis step
    model = genai.GenerativeModel("gemini-3.5-flash")
    
    prompt = f"""
    You are an expert culinary editor. Please rewrite the following recipe instructions 
    to sound highly professional, clear, and appetizing. 
    Fix any grammar or spelling mistakes. 
    Format it as clear, step-by-step paragraphs or numbered points.
    
    Here are the raw instructions:
    {raw_text}
    
    Return ONLY the rewritten instructions. Do not include introductory or concluding remarks.
    """
    
    try:
        # Standard text generation (no JSON forcing needed here)
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Gemini API Error (Rewrite): {e}")
        return None