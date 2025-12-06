from loguru import logger

from backend.agents.agent_interface import AgentInterface, format_previous_attempts
from backend.llms.llm_interface import LllmInterface


class PlanAndSolve(AgentInterface):
    @staticmethod
    def name() -> str:
        return "Planandsolve"

    def run(
        self, llm: LllmInterface, hiperparams: dict,context: str, merged_briefs: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        reasoning_plan = self.plan(llm, hiperparams, context, merged_briefs, user_prompt, previous_attempts)
        return self.solve(llm, hiperparams, reasoning_plan, merged_briefs, user_prompt, previous_attempts)

    @staticmethod
    def plan(
        llm: LllmInterface, hiperparams: dict, system_prompt: str, merged_briefs: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        """
        Planning — understand intent and design an execution strategy.
        """
        logger.info("Generating reasoning plan")
        chat_history = format_previous_attempts(previous_attempts)

        planning_prompt = (
            f"Jesteś Głównym Analitykiem Strategicznym Republiki Atlantis. "
            f"Twoim zadaniem jest przeanalizowanie ważonych danych wywiadowczych i stworzenie PLANU ROZUMOWANIA.\n\n"

            f"### KONTEKST STATYCZNY (PROFIL ATLANTIS):\n{system_prompt}\n\n"

            f"### DANE WEJŚCIOWE Z WAGAMI (PRIORYTETY):\n"
            f"Format danych to: 'WEIGHT: [Wartość] BRIEF: [Treść]'.\n"
            f"{merged_briefs}\n\n"

            f"### HISTORIA ROZMOWY:\n{chat_history}\n\n"

            f"### AKTUALNE ZAPYTANIE:\n{user_prompt}\n\n"

            f"### INSTRUKCJE ANALITYCZNE:\n"
            f"1. **ANALIZA WAG (KLUCZOWE):** Zwróć szczególną uwagę na parametr `WEIGHT` przy każdym streszczeniu.\n"
            f"   - **Wysoka waga:** Informacje te są krytyczne, pewne i nadrzędne. Muszą stanowić fundament scenariuszy.\n"
            f"   - **Niska waga:** Informacje pomocnicze. W razie sprzeczności z dokumentem o wyższej wadze – ignoruj je.\n"
            f"2. Zidentyfikuj intencję użytkownika (Raport vs Czat).\n"
            f"3. Stwórz plan w JĘZYKU POLSKIM.\n\n"

            f"W swoim planie uwzględnij:\n"
            f"- **Filtr Istotności:** Wymień ID dokumentów o NAJWYŻSZEJ wadze, na których oprzesz analizę.\n"
            f"- **Rozwiązywanie Konfliktów:** Jeśli dokumenty są sprzeczne, wskaż, że wybierasz wersję z dokumentu o wyższej wadze.\n"
            f"- **Szkic Scenariuszy:** Główne tezy oparte na priorytetowych danych.\n\n"

            f"Wygeneruj teraz plan rozumowania."
        )

        return llm.generate_response(planning_prompt)

    @staticmethod
    def solve(
        llm: LllmInterface, hiperparams: dict, system_prompt: str, plan: str, brief_prompts: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        """
        Solving — Generate the final Diplomatic Report based on the reasoning plan.
        """
        logger.info("Generating solution from plan")
        chat_history = format_previous_attempts(previous_attempts)

        solving_prompt = (
            f"Działasz jako Sekretarz ds. Raportów Dyplomatycznych Republiki Atlantis. "
            f"Twoim celem jest wykonanie przygotowanego planu i wygenerowanie finalnej odpowiedzi dla Ambasadora.\n\n"

            f"### BAZA WIEDZY (PROFIL ATLANTIS):\n{system_prompt}\n\n"

            f"### DANE ŹRÓDŁOWE Z WAGAMI (PRIORYTETY):\n"
            f"Format: 'WEIGHT: [Wartość] BRIEF: [Treść]'.\n"
            f"{brief_prompts}\n\n"

            f"### HISTORIA ROZMOWY:\n{chat_history}\n\n"
            f"### PLAN ANALITYKA (TWOJE WYTYCZNE):\n{plan}\n\n"
            f"### ZAPYTANIE UŻYTKOWNIKA:\n{user_prompt}\n\n"

            f"### INSTRUKCJE WYKONAWCZE:\n"
            f"1. **Hierarchia Ważności:** Budując narrację, opieraj główne tezy na dokumentach o najwyższej wadze (`WEIGHT`). Informacje o niskiej wadze traktuj jako tło lub niepotwierdzone sygnały.\n"
            f"2. Jeśli plan zakłada **Pełny Raport**, zachowaj strukturę:\n"
            f"   - SEKCJA A: Streszczenie Wykonawcze\n"
            f"   - SEKCJA B: Scenariusze Strategiczne (Narracja + Wyjaśnienie przyczyn)\n"
            f"   - SEKCJA C: Rekomendacje (Ofensywne/Defensywne)\n"
            f"3. Jeśli plan zakłada **Odpowiedź na Pytanie** (tryb czatu), udziel konkretnej odpowiedzi merytorycznej.\n"
            f"4. **JĘZYK:** Cała odpowiedź musi być w profesjonalnym **JĘZYKU POLSKIM**.\n\n"

            f"### KRYTYCZNE ZASADY:\n"
            f"- **Wyjaśnialność (Explainability):** KAŻDE stwierdzenie oparte na faktach musi zawierać przypis do ID źródła (np. [DOC_01]).\n"
            f"- **Wagi a Język Pewności (Kluczowe):** Dostosuj stopień stanowczości do wagi źródła.\n"
            f"    - **Wysoka waga:** Używaj sformułowań pewnych: 'Zagrożenie jest krytyczne', 'Dane potwierdzają', 'Jest wysoce prawdopodobne'.\n"
            f"    - **Niska waga:** Używaj trybu przypuszczającego: 'Istnieją przesłanki', 'Wymaga weryfikacji', 'Możliwy scenariusz', 'Według niepotwierdzonych doniesień'.\n"
            f"- **Ton:** Profesjonalny, dyplomatyczny, bezstronny.\n"
            f"- **Formatowanie:** NIE używaj nagłówków typu 'Do:', 'Od:', 'Data:'. Zacznij od razu od treści raportu (np. '**SEKCJA A...**') lub bezpośredniej odpowiedzi.\n"
            f"- **Ciągłość:** Jeśli użytkownik prosi o poprawkę, uwzględnij historię rozmowy.\n\n"

            f"Wygeneruj teraz finalną treść ({hiperparams['type']} scenariusz) w języku polskim dla horyzontu czasowego {hiperparams['time']} miesięcy w przód."
        )

        return llm.generate_response(solving_prompt)
