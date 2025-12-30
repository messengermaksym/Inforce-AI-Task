import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_ID = "gemini-2.5-flash"
GEMINI_PRICING = {
    "input": 0.30 / 1_000_000,
    "output": 2.50 / 1_000_000
}

def calculate_gemini_cost(prompt_tokens, completion_tokens):
    cost = (prompt_tokens * GEMINI_PRICING["input"]) + (completion_tokens * GEMINI_PRICING["output"])
    return round(cost, 8)