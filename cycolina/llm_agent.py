import os
from google import genai
from google.genai.errors import APIError

# export GEMINI_API_KEY="GEMINI_API_KEY_HERE"

def generate_text_with_gemini(prompt: str):
    """
    Łączy się z API Google Gemini i generuje odpowiedź tekstową.
    """
    # 1. Ustawienie klucza API
    # Najlepszą praktyką jest ustawienie klucza API jako zmiennej środowiskowej
    # o nazwie GEMINI_API_KEY. Jeśli nie jest ustawiona, program zgłosi błąd.
    if not os.getenv("GEMINI_API_KEY"):
        print("BŁĄD: Zmienna środowiskowa GEMINI_API_KEY nie jest ustawiona.")
        print("Upewnij się, że ustawiłeś swój klucz API.")
        return

    try:
        # 2. Inicjalizacja klienta
        # Klient automatycznie użyje klucza z GEMINI_API_KEY.
        client = genai.Client()

        # 3. Wywołanie API
        # Używamy modelu 'gemini-2.5-flash', który jest szybki i efektywny.
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        # 4. Wyświetlenie wyniku
        print("--- Zapytanie ---")
        print(prompt)
        print("\n--- Odpowiedź Gemini ---")
        print(response.text)

    except APIError as e:
        print(f"Wystąpił błąd API: {e}")
    except Exception as e:
        print(f"Wystąpił nieoczekiwany błąd: {e}")

# --- Użycie funkcji ---
if __name__ == "__main__":
    moje_zapytanie = "Wytłumacz, czym jest kwantowa spójność w jednym zdaniu."
    generate_text_with_gemini(moje_zapytanie)