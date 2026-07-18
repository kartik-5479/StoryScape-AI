import requests
import urllib.parse

def get_image_url(prompt):
    prompt = urllib.parse.quote(prompt)
    return f"https://image.pollinations.ai/prompt/{prompt}"