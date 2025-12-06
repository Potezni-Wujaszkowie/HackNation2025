import os
from langchain_openai import ChatOpenAI

from backend.llms.llm_interface import LllmInterface
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class LlmPllum(LllmInterface):
    def __init__(self, temperature: float = 0.7, max_tokens = 3000):
        api_key = os.environ["PLLUM_API_KEY"]
        if api_key is None:
            raise RuntimeError("PLLUM_API_KEY environment variable not set.")
        self.llm = ChatOpenAI(
            model=str(self),
            openai_api_key="EMPTY",
            openai_api_base="https://apim-pllum-tst-pcn.azure-api.net/vllm/v1",
            temperature=temperature,
            max_tokens=max_tokens,
            default_headers={
                'Ocp-Apim-Subscription-Key': api_key
            }
        )

    @staticmethod
    def name() -> str:
        return "Pllum"

    def __str__(self) -> str:
        return "CYFRAGOVPL/pllum-12b-nc-chat-250715"

    def generate_response(self, prompt: str) -> str:
        return self.llm.invoke(prompt).json()['choices'][0]['message']['content']
