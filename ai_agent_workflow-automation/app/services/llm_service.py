from typing import Any, Dict, Optional

from langchain_groq import ChatGroq


class LLMService:
    """
    Centralized LLM service used by workflow steps.

    Keeps LLM-specific implementation outside
    the workflow engine.
    """

    def __init__(
        self,
        model: str = "openai/gpt-oss-120b",
        temperature: float = 0,
    ):
        self.model = model
        self.temperature = temperature

        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
        )

    def generate(
        self,
        instruction: str,
        context: Optional[Any] = None,
    ) -> str:

        prompt = f"""
You are an AI workflow execution assistant.

Task:
{instruction}

Context:
{context}

Return a concise, useful result.
Do not invent facts that are not present in the context.
"""

        response = self.llm.invoke(prompt)

        return response.content