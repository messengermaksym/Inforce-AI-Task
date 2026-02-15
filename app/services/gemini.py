"""
Сервіс роботи з Gemini API: клієнт, розрахунок вартості.
Усі параметри беруться з конфігурації (.env).
"""
from google import genai

from app.config import settings


def get_client() -> genai.Client:
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY не задано в .env")
    return genai.Client(api_key=settings.GEMINI_API_KEY)


def get_model_id() -> str:
    return settings.GEMINI_MODEL_ID


def calculate_gemini_cost(prompt_tokens: int, completion_tokens: int) -> float:
    input_price = settings.GEMINI_INPUT_PRICE_PER_MILLION / 1_000_000
    output_price = settings.GEMINI_OUTPUT_PRICE_PER_MILLION / 1_000_000
    cost = (prompt_tokens * input_price) + (completion_tokens * output_price)
    return round(cost, 8)
