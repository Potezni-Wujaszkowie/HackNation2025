from llm_gemini import LlmGemini
from summary_cache import SummaryCache


def main():
    summary_cache = SummaryCache()
    llms = {
        LlmGemini.name(): LlmGemini()
    }
    msz_prompt = "" # from frontends
    with open("phase1_prompt.txt", "r") as f:
        system_prompt = f.read()
    for document in summary_cache.cache.keys():
        ph1_prompt += f"\n- {document}"

    response = llms[LlmGemini.name()].generate_response(prompt)
    print("--- Zapytanie ---")
    print(ph1_prompt)
    print("\n--- Odpowiedź Gemini ---")
    print(response.text)


if __name__ == "__main__":
    main()
