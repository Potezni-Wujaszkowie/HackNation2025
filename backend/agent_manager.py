from loguru import logger
import yaml

from backend.llms.llm_interface import LllmInterface
from backend.llms.llm_gemini import LlmGemini
from backend.llms.llm_pllum import LlmPllum
from backend.summary_cache import SummaryCache

from backend.agents.agent_interface import AgentInterface
from backend.agents.agent_plan_and_solve import PlanAndSolve


class AgentManager:
    def __init__(self, default_llm: str, default_agent: str):
        with open("config.yaml", "r") as f:
            self.config_file = yaml.safe_load(f)

        self.summary_cache = SummaryCache()

        self.llms = {
            LlmGemini.name(): LlmGemini(),
            LlmPllum.name(): LlmPllum(max_tokens=16000),
        }
        self.set_llm(default_llm)

        self.agents = {
            PlanAndSolve.name(): PlanAndSolve(),
        }
        self.set_agent(default_agent)

    def get_llm(self) -> LllmInterface:
        return self.llm

    def set_llm(self, llm_name: str):
        if llm_name not in self.llms.keys():
            raise RuntimeError("Invalid name for llm. Use LlmInterface.name().")
        self.llm = self.llms[llm_name]


    def get_agent(self) -> AgentInterface:
        return self.agent

    def set_agent(self, agent_name: str):
        if agent_name not in self.agents.keys():
            raise RuntimeError("Invalid name for agent. Use AgentInterface.name().")
        self.agent = self.agents[agent_name]

    def generate_brief(self, document: str, max_words: int) -> str:
        logger.info("Generating brief for a document")
        prompt = f'Używając maksymalnie {max_words} słów wygeneruj streszczenie poniższego dokumentu (uwzględnij jak najwięcej faktów, liczb oraz konkretów; WAŻNE: jeśli dokument nie niesie większej wartości merytorycznej po prostu zwróć pusty string):\n\n{document}'
        return self.llm.generate_response(prompt)

    def generate_data_summary(self, briefs_with_weights: list[tuple[int, str, str]], max_words: int) -> str:
        logger.info("Generating data summary from briefs with weights")
        formatted_context = ""

        for weight, text, source in briefs_with_weights:
            if not text or text.strip() == "":
                continue
            formatted_context += f"[WAGA: {weight}] [ŹRÓDŁO: {source}] TREŚĆ: {text}\n\n"

        if not formatted_context:
            return "Brak danych do wygenerowania streszczenia."

        prompt = (
            f"Jesteś Analitykiem Informacji Strategicznej w MSZ. "
            f"Twoim zadaniem jest przygotowanie 'Streszczenia Wykonawczego' (Executive Summary) całego zbioru danych.\n\n"

            f"### DANE WEJŚCIOWE (NOTATKI Z WAGAMI):\n"
            f"{formatted_context}\n"

            f"### INSTRUKCJE:\n"
            f"1. **Synteza, nie lista:** Nie wymieniaj dokumentów po kolei. Stwórz spójny, narracyjny obraz sytuacji wyłaniający się z tych danych.\n"
            f"2. **Hierarchia Ważności:** Narrację buduj na informacjach z dokumentów o wysokiej wadze.\n"
            f"3. **Przejrzystość:** Tekst ma być zrozumiały w 30 sekund.\n"
            f"4. **Ograniczenia:**\n"
            f"   - Maksymalnie **{max_words} słów**.\n"
            f"   - Język: Polski, profesjonalny.\n"
            f"   - Styl: 2-3 konkretne akapity.\n\n"

            f"Wygeneruj teraz syntetyczne streszczenie danych."
        )

        return self.llm.generate_response(prompt)

    def generate_recommendations(self, system_prompt: str, brief_prompts: str, generated_scenarios_text: str) -> str:
        """
        Generuje Sekcję C (Rekomendacje) na podstawie profilu Atlantis, danych i wygenerowanych scenariuszy.
        """

        recommendation_prompt = (
            f"Działasz jako Główny Doradca Strategiczny Rządu Atlantis. "
            f"Twoim zadaniem jest sformułowanie konkretnych rekomendacji decyzyjnych w oparciu o analizę scenariuszową.\n\n"

            f"### BAZA WIEDZY:\n{system_prompt}\n\n"
            f"### DANE ŹRÓDŁOWE (Z PODANYM POLAMI 'ŹRÓDŁO'):\n{brief_prompts}\n\n"
            f"### SCENARIUSZE:\n{generated_scenarios_text}\n\n"

            f"### ZADANIE:\n"
            f"Napisz **SEKCJĘ C: REKOMENDACJE** (Defensywne i Ofensywne).\n\n"

            f"### WYMOGI CYTOWANIA:\n"
            f"- Uzasadniając rekomendację, powołaj się na konkretne `ŹRÓDŁO` z danych (np. 'Zgodnie z ostrzeżeniami zawartymi w [Źródło: wywiad_mosad.txt], należy wzmocnić cyberbezpieczeństwo').\n"
            f"- NIE wspominaj o 'wagach' dokumentów w tekście wynikowym.\n\n"

            f"Wygeneruj teraz Sekcję C w języku polskim."
        )
        return self.llm.generate_response(recommendation_prompt)

    @staticmethod
    def compose_briefs_with_weights(weigths_briefs: list[tuple[int, str, str]]) -> str:
        return "\n\n".join([
            f"WAGA: {weight}; STRESZCZENIE: {brief}; ŹRÓDŁO: {source}"
            for weight, brief, source in weigths_briefs
        ])

    def generate_scenarios_and_summary(self, briefs: list[tuple[int, str, str]]):
        briefs_with_weights = [(weight, brief) for weight, brief, _ in briefs]
        aggregated_brief = AgentManager.compose_briefs_with_weights(briefs_with_weights)

        logger.debug(f"Aggregated briefs: {aggregated_brief}")

        with open("./backend/atlantis_context.txt", "r") as f:
            context = f.read()

        hiperparams = (
            {
                "type": "pozytywny",
                "time": 12
            },
            {
                "type": "negatywny",
                "time": 12
            },
            {
                "type": "pozytywny",
                "time": 36
            },
            {
                "type": "negatywny",
                "time": 36
            },
        )
        scenarios = []

        for hparam in hiperparams:
            logger.info(f"Foreseeing {hparam['type']} for {hparam['time']} months ahead")
            scenarios.append(self.agent.run(
                llm=self.llm,
                hiperparams=hparam,
                context=context,
                merged_briefs=aggregated_brief,
            ))

        logger.info(f"Foreseeing done with agent: {self.agent.name()} and llm: {self.llm.name()}.")
        recommendations = self.generate_recommendations(
            system_prompt=context,
            brief_prompts=aggregated_brief,
            generated_scenarios_text="\n\n".join([scenario.text for scenario in scenarios])
        )
        return {
            "data_summary": self.generate_data_summary(briefs_with_weights, self.config_file["max_brief_words"]),
            "scenarios": [scenario.text for scenario in scenarios],
            "recommendations": recommendations.text
        }


if __name__ == "__main__":
    llm_manager = AgentManager(
        default_llm=LlmGemini().name(),
        default_agent=PlanAndSolve().name()
    )
    documents = []
    with open("test.txt", "r") as f:
        documents.append(f.read())

    for doc in documents:
        brief = llm_manager.generate_brief(doc, max_words=250)

    brief_weight = [(10, brief, "test.txt") for brief in documents]
    out = llm_manager.generate_scenarios_and_summary(brief_weight)
    print(out)