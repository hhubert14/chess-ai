import time
from typing import Any, Optional, Callable

from langchain_core.runnables import RunnableSerializable
from langchain_core.messages import BaseMessage

def safe_invoke(chain: RunnableSerializable[dict, BaseMessage], inputs: dict, max_retries: int = 3) -> Optional[str]:
    """Safely invoke an API chain with retry logic.
    
    Args:
        chain: The LangChain chain to invoke
        inputs: The inputs to pass to the chain
        max_retries: Maximum number of retry attempts
        
    Returns:
        The content of the response if successful, None otherwise
    """
    for attempt in range(max_retries):
        try:
            return chain.invoke(inputs).content
        except Exception as e:
            if attempt == max_retries - 1:
                print(f"Failed after {max_retries} attempts: {e}")
                return None
            print(f"Attempt {attempt + 1} failed: {e}. Retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff