from backend.llms.llm_interface import LllmInterface
from google import genai
from dotenv import load_dotenv, find_dotenv
import os

from loguru import logger

load_dotenv(find_dotenv())

class LlmGemini(LllmInterface):
    def __init__(self, model: str = "gemini-2.5-flash"):
        if not os.getenv("GEMINI_API_KEY"):
            raise RuntimeError("GEMINI_API_KEY not set in environment variables.")

        self.model = model
        self.client = genai.Client()

        logger.info(f"Initialized Gemini LLM with model: {self.model}")


    @staticmethod
    def name() -> str:
        return "Gemini"

    def __str__(self):
        return self.model

    def generate_response(self, prompt: str) -> str:
        return self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )
