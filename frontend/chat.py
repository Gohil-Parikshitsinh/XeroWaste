# import os
# import google.generativeai as genai
#
# # Configure API key
# genai.configure(api_key=os.getenv("AIzaSyAd3YbRi038N55z7uJXaGBV5ulL2BmNiQk"))

import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Get API key from .env
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("API key is missing! Add it to the .env file.")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

# Initialize the model
# model = genai.GenerativeModel("gemini-pro")
model = genai.GenerativeModel("gemini-1.5-pro-latest")


def get_recipe_recommendations(ingredients):
    prompt = f"""
    You are an AI-powered food recommendation assistant.
    Suggest *Indian recipes* based on the given ingredients.
    If no exact match is found, suggest alternatives with similar ingredients.

    *Ingredients provided:* {', '.join(ingredients)}

    Provide:
    - *Recipe Name*
    - *Brief Description*
    - *Preparation Time*
    - *Cooking Time*
    - *Serving Size*
    - *Key Ingredients* (highlighting provided ones)
    - *Cooking Instructions* (step-by-step)

    Keep the response structured and user-friendly.
    """

    response = model.generate_content(prompt)
    return response.text


# Example usage
if __name__ == "_main_":
    user_ingredients = input(
        "Enter your available ingredients (comma-separated): "
    ).split(",")
    user_ingredients = [i.strip() for i in user_ingredients]  # Clean spaces
    recommendations = get_recipe_recommendations(user_ingredients)
    print("\nRecommended Recipes:\n", recommendations)