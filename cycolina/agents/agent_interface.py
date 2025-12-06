from abc import ABC, abstractmethod
from llms.llm_interface import LllmInterface


class AgentInterface(ABC):
    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    async def run(
        self, llm: LllmInterface, context: str, prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        pass
