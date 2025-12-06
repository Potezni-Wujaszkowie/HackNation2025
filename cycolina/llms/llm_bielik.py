from llms.llm_interface import LlmInterface

class LlmBielik(LlmInterface):
    def __init__(self):
        raise NotImplementedError()

    @staticmethod
    def name() -> str:
        raise NotImplementedError()

    def generate_response(self, prompt: str) -> str:
        raise NotImplementedError()