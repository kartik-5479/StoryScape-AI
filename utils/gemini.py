import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


@st.cache_resource
def get_gemini_client():
    """Create and cache the Gemini client."""
    return genai.Client(api_key=API_KEY)


def test_gemini(genre, art_style):
    client = get_gemini_client()

    prompt = f"""
    You are an AI Visual Novel narrator.

    Create the opening scene of a {genre} story.

    Art Style: {art_style}

    Return ONLY a valid JSON object in this format:

    {{
    "story_text": "A short story paragraph",
    "image_prompt": "A detailed image generation prompt",
    "options": [
        "Choice 1",
        "Choice 2",
        "Choice 3"
    ],
    "is_end": false
}}

    If the story reaches a satisfying conclusion, set "is_end" to true and return an empty "options" array.
    Otherwise, set "is_end" to false and provide exactly 3 choices.
    Do not include markdown.
    Do not wrap the JSON inside ```json.
    Return only the JSON.
    """

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    if response.text is None:
        raise ValueError("Gemini returned an empty response.")
    return response.text

def continue_story(choice):
    client = get_gemini_client()

    prompt = f"""
    You are continuing an interactive visual novel.

    The player chose:

    {choice}

    Continue the story naturally based on that choice.

    Return ONLY valid JSON in this format:

    {{
    "story_text":"...",
    "image_prompt":"...",
    "options":[
        "...",
        "...",
        "..."
    ],
    "is_end": false
}}
    If the story reaches a satisfying conclusion, set "is_end" to true and return an empty "options" array.
    Otherwise, set "is_end" to false and provide exactly 3 choices.
    Do not include markdown.
    Return only JSON.
    """



    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
)

    if response.text is None:
        raise ValueError("Empty response from Gemini")

    return response.text