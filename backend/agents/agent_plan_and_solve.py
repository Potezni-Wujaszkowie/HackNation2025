from loguru import logger

from backend.agents.agent_interface import AgentInterface
from backend.llms.llm_interface import LllmInterface


class PlanAndSolve(AgentInterface):
    @staticmethod
    def name() -> str:
        return "Planandsolve"

    def run(
        self, llm: LllmInterface, hiperparams: dict,context: str, merged_briefs: str
    ) -> str:
        reasoning_plan = self.plan(llm, hiperparams, context, merged_briefs)
        return self.solve(llm, hiperparams, reasoning_plan, merged_briefs)

    def plan(
        llm: LllmInterface, hiperparams: dict, system_prompt: str, merged_briefs: str
    ) -> str:
        """
        Planning — understand intent and design an execution strategy.
        """
        logger.info("Generating reasoning plan")
        planning_prompt = (
            f"Jesteś Głównym Analitykiem Strategicznym Republiki Atlantis. "
            f"Twoim zadaniem jest przeanalizowanie danych wywiadowczych i stworzenie PLANU ROZUMOWANIA dla scenariusza: {hiperparams['type']} ({hiperparams['time']} mies.).\n\n"

            f"### KONTEKST STATYCZNY (PROFIL ATLANTIS):\n{system_prompt}\n\n"

            f"### DANE WEJŚCIOWE (Z WAGAMI I ŹRÓDŁAMI):\n"
            f"Format danych: 'WAGA: [1-10]; STRESZCZENIE: [...]; ŹRÓDŁO: [Nazwa Pliku/Instytucji]'.\n"
            f"{merged_briefs}\n\n"

            f"### INSTRUKCJE ANALITYCZNE:\n"
            f"1. **FILTR WAG (LOGIKA WEWNĘTRZNA):** Użyj parametru `WAGA` do oceny wiarygodności. Informacje z wagą wysoką (8-10) są pewnikami. Informacje z wagą niską (1-3) traktuj ostrożnie.\n"
            f"2. **SELEKCJA ŹRÓDEŁ:** Wybierz konkretne `ŹRÓDŁA`, które potwierdzają tezy dla scenariusza {hiperparams['type']}.\n"
            f"3. **PLAN:** Stwórz plan w JĘZYKU POLSKIM.\n\n"

            f"W swoim planie uwzględnij:\n"
            f"- **Kluczowe Fakty:** Jakie konkretne informacje ze streszczeń wykorzystasz?\n"
            f"- **Weryfikacja Źródeł:** Przy każdym fakcie zanotuj sobie `ŹRÓDŁO` (np. 'raport_NATO.pdf'), które zacytujesz w finale.\n"
            f"- **Logika Scenariusza:** Jak te fakty prowadzą do {hiperparams['type']} rozwoju wydarzeń w ciągu {hiperparams['time']} miesięcy?\n\n"

            f"Wygeneruj teraz plan rozumowania."
        )

        return llm.generate_response(planning_prompt)

    @staticmethod
    def solve(
        llm: LllmInterface, hiperparams: dict, system_prompt: str, plan: str, brief_prompts: str
    ) -> str:
        """
        Solving — Generate the final Diplomatic Report based on the reasoning plan.
        """
        logger.info("Generating solution from plan")

        solving_prompt = (
            f"Działasz jako Sekretarz ds. Raportów Dyplomatycznych Republiki Atlantis. "
            f"Twoim celem jest wygenerowanie treści scenariusza strategicznego na podstawie planu.\n\n"

            f"### BAZA WIEDZY (PROFIL ATLANTIS):\n{system_prompt}\n\n"

            f"### DANE ŹRÓDŁOWE:\n{brief_prompts}\n\n"

            f"### PLAN ANALITYKA:\n{plan}\n\n"

            f"### ZADANIE:\n"
            f"Napisz treść scenariusza: **{hiperparams['type'].upper()}** na okres **{hiperparams['time']} MIESIĘCY**.\n\n"

            f"### STRUKTURA ODPOWIEDZI:\n"
            f"1. **Narracja Scenariusza:** Opis wydarzeń (co się wydarzy?).\n"
            f"2. **Analiza Korelacji i Przyczynowości:** Wyjaśnienie dlaczego tak się stanie, bazując na faktach.\n\n"

            f"### KRYTYCZNE ZASADY CYTOWANIA (BEZWZGLĘDNE):\n"
            f"1. **NIE CYTUJ WAG:** Nigdy nie pisz 'Waga 10 potwierdza...'. Użytkownik końcowy nie widzi wag.\n"
            f"2. **CYTUJ ŹRÓDŁA:** Każde kluczowe stwierdzenie musi kończyć się przypisem w nawiasie wskazującym na `ŹRÓDŁO`.\n"
            f"   - ŹLE: 'Gospodarka spowolni (Waga 9).'\n"
            f"   - DOBRZE: 'Gospodarka spowolni, co wynika z prognoz MFW [Źródło: raport_mfw_2024.pdf].'\n"
            f"3. **Wiarygodność:** Jeśli opierasz się na źródle o wysokiej wadze (którą znasz z danych wejściowych), używaj języka pewności ('Jest pewne, że...'). Jeśli na niskiej - języka przypuszczeń.\n\n"

            f"Wygeneruj teraz tekst scenariusza w języku polskim."
        )

        return llm.generate_response(solving_prompt)
