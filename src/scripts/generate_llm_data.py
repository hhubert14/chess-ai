import os

from dotenv import load_dotenv
from openai import OpenAI
from langchain_deepseek import ChatDeepSeek

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

# client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")

llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,
    model="deepseek-reasoner",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

messages = [
    (
        "system",
        "You are a chess tutor",
    ),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)