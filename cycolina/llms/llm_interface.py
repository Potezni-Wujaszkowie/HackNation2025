from abc import ABC, abstractmethod

class LllmInterface(ABC):
    @staticmethod
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def generate_response(self, prompt: str) -> str:
        pass