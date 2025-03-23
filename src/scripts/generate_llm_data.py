import os

from dotenv import load_dotenv
from openai import OpenAI
from langchain_deepseek import ChatDeepSeek

from prompts import (
    SYSTEM_PROMPT,
    POSITION_ASSESSMENT_PROMPT,
    KING_SAFETY_PROMPT,
    TACTICAL_ANALYSIS_PROMPT,
    STRATEGIC_ANALYSIS_PROMPT,
    BEST_MOVE_PROMPT,
)

load_dotenv()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

llm = ChatDeepSeek(
    api_key=DEEPSEEK_API_KEY,
    model="deepseek-reasoner",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

messages = [
    ("system", SYSTEM_PROMPT),
    ("human", "I love programming."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)