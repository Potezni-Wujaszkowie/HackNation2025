from loguru import logger

from agents.agent_interface import AgentInterface, format_previous_attempts
from llms.llm_interface import LllmInterface


class PlanAndSolve(AgentInterface):
    @staticmethod
    def name() -> str:
        return "Planandsolve"

    def run(
        self, llm: LllmInterface, context: str, brief_prompts: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        reasoning_plan = self.plan(llm, context, brief_prompts, user_prompt, previous_attempts)
        return self.solve(llm, context, reasoning_plan, brief_prompts, user_prompt, previous_attempts)

    @staticmethod
    def plan(
        llm: LllmInterface, system_prompt: str, brief_prompts: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        logger.info("Generating reasoning plan...")
        """
        Planning — understand intent and design an execution strategy.
        """
        chat_history = format_previous_attempts(previous_attempts)

        planning_prompt = (
            f"Jesteś Głównym Analitykiem Strategicznym Republiki Atlantis. "
            f"Twoim zadaniem jest przeanalizowanie danych wywiadowczych i stworzenie PLANU ROZUMOWANIA (Chain of Thought).\n\n"

            f"### KONTEKST STATYCZNY (PROFIL PAŃSTWA ATLANTIS):\n{system_prompt}\n\n"

            f"### DANE WEJŚCIOWE (STRESZCZENIA DOKUMENTÓW):\n{brief_prompts}\n\n"

            f"### HISTORIA ROZMOWY:\n{chat_history}\n\n"

            f"### AKTUALNE ZAPYTANIE UŻYTKOWNIKA:\n{user_prompt}\n\n"

            f"### INSTRUKCJE:\n"
            f"1. Przeanalizuj dane wejściowe (mogą być po angielsku) pod kątem interesów Atlantis.\n"
            f"2. Zidentyfikuj intencję użytkownika: czy chce pełnego raportu, czy odpowiedzi na konkretne pytanie (czat).\n"
            f"3. Stwórz ustrukturyzowany plan odpowiedzi. NIE pisz jeszcze finalnego tekstu raportu/odpowiedzi.\n"
            f"4. **UWAGA: Cały Twój proces myślowy i plan muszą być w JĘZYKU POLSKIM.**\n\n"

            f"W swoim planie uwzględnij:\n"
            f"- **Filtr Istotności:** Które dokumenty (cytuj ID, np. [DOC_01]) są kluczowe dla zapytania?\n"
            f"- **Analiza Korelacji:** Jakie są ukryte powiązania między faktami?\n"
            f"- **Szkic Odpowiedzi/Scenariuszy:** Główne tezy, które poruszysz.\n"
            f"- **Weryfikacja Źródeł:** Potwierdź, że masz dowody (ID) na swoje tezy.\n\n"

            f"Wygeneruj teraz plan rozumowania w języku polskim."
        )

        return llm.generate_response(planning_prompt)

    @staticmethod
    def solve(
        llm: LllmInterface, system_prompt: str, plan: str, brief_prompts: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        """
        Solving — Generate the final Diplomatic Report based on the reasoning plan.
        """
        chat_history = format_previous_attempts(previous_attempts)

        solving_prompt = (
            f"Działasz jako Sekretarz ds. Raportów Dyplomatycznych Republiki Atlantis. "
            f"Twoim celem jest wykonanie przygotowanego planu i wygenerowanie finalnej odpowiedzi dla Ambasadora.\n\n"

            f"### BAZA WIEDZY (PROFIL ATLANTIS):\n{system_prompt}\n\n"
            f"### DANE ŹRÓDŁOWE:\n{brief_prompts}\n\n"
            f"### HISTORIA ROZMOWY:\n{chat_history}\n\n"
            f"### PLAN ANALITYKA (TWOJE WYTYCZNE):\n{plan}\n\n"
            f"### ZAPYTANIE UŻYTKOWNIKA:\n{user_prompt}\n\n"

            f"### INSTRUKCJE WYKONAWCZE:\n"
            f"1. Jeśli plan zakłada **Pełny Raport**, zachowaj strukturę:\n"
            f"   - SEKCJA A: Streszczenie Wykonawcze\n"
            f"   - SEKCJA B: Scenariusze Strategiczne (Narracja + Wyjaśnienie przyczn)\n"
            f"   - SEKCJA C: Rekomendacje (Ofensywne/Defensywne)\n"
            f"2. Jeśli plan zakłada **Odpowiedź na Pytanie** (tryb czatu), udziel konkretnej odpowiedzi merytorycznej.\n"
            f"3. **JĘZYK:** Cała odpowiedź musi być w profesjonalnym **JĘZYKU POLSKIM**.\n\n"

            f"### KRYTYCZNE ZASADY:\n"
            f"- **Wyjaśnialność (Explainability):** KAŻDE stwierdzenie oparte na faktach musi zawierać przypis do ID źródła (np. [DOC_01], [DOC_15]).\n"
            f"- **Ton:** Profesjonalny, dyplomatyczny, bezstronny.\n"
            f"- **Formatowanie:** NIE używaj nagłówków typu 'Do:', 'Od:', 'Data:'. Zacznij od razu od treści raportu (np. '**SEKCJA A...**') lub bezpośredniej odpowiedzi.\n"
            f"- **Ciągłość:** Jeśli użytkownik prosi o poprawkę, uwzględnij historię rozmowy.\n\n"

            f"Wygeneruj teraz finalną treść w języku polskim."
        )

        return llm.generate_response(solving_prompt)
