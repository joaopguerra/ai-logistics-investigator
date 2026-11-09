import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


def get_chat_model() -> ChatGoogleGenerativeAI:
    load_dotenv()

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY não configurada")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        timeout=30,
        max_retries=0,
    )