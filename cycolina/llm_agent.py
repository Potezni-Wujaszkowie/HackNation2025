import os
from google import genai
from google.genai.errors import APIError


def generate_text_with_gemini(prompt: str):
    """
    Łączy się z API Google Gemini i generuje odpowiedź tekstową.
    """
    if not os.getenv("GEMINI_API_KEY"):
        print("BŁĄD: Zmienna środowiskowa GEMINI_API_KEY nie jest ustawiona.")
        print("Upewnij się, że ustawiłeś swój klucz API.")
        return

    try:
        client = genai.Client()

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        print("--- Zapytanie ---")
        print(prompt)
        print("\n--- Odpowiedź Gemini ---")
        print(response.text)

    except APIError as e:
        print(f"Wystąpił błąd API: {e}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

if __name__ == "__main__":
    moje_zapytanie = "Wytłumacz, czym jest kwantowa spójność w jednym zdaniu."
    generate_text_with_gemini(moje_zapytanie)