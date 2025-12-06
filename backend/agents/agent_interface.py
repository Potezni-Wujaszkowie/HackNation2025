from abc import ABC, abstractmethod
from backend.llms.llm_interface import LllmInterface


class AgentInterface(ABC):
    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    async def run(
        self, llm: LllmInterface, context: str, brief_prompts: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        pass

def format_previous_attempts(previous_attempts: list[dict] | None) -> str:
    if not previous_attempts:
        return ""

    formatted = "\n\n<previous attempt>\n"
    for attempt in previous_attempts:
        formatted += f"- Question: {attempt.get('Input', 'N/A')}\n"
        formatted += f"- Answer: {attempt.get('Output', 'N/A')}\n"
    formatted += "</previous attempt>\n"
    return formatted
