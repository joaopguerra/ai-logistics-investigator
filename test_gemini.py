import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

if not os.getenv("GOOGLE_API_KEY"):
    raise ValueError("GOOGLE_API_KEY não configurada")

model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    timeout=30,
    max_retries=0
)

response = model.invoke(
    "Explique em português, em três frases, "
    "o que é um sistema de rastreamento logístico."
)

print(response.content)