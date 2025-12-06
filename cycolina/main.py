from llm_gemini import LlmGemini


def main():
    llm = LlmGemini()
    prompt = "Wytłumacz, czym jest kwantowa spójność w jednym zdaniu."
    response = llm.generate_response(prompt)
    print("--- Zapytanie ---")
    print(prompt)
    print("\n--- Odpowiedź Gemini ---")
    print(response.text)


if __name__ == "__main__":
    main()
