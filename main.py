from loguru import logger

from backend.llms.llm_interface import LllmInterface
from backend.llms.llm_gemini import LlmGemini
from backend.summary_cache import SummaryCache
from backend.agents.agent_plan_and_solve import PlanAndSolve

import yaml

def compose_briefs_with_weights(weigths_briefs: list[tuple[int, str]]) -> str:
    return "\n\n".join([f"WAGA: {weight}; STRESZCZENIE: {brief}" for weight, brief in weigths_briefs])

def generate_brief(llm: LllmInterface, document: str, max_words: int) -> str:
    logger.info("Generating brief for a document")
    prompt = f'Używając maksymalnie {max_words} słów wygeneruj streszczenie poniższego dokumentu (uwzględnij jak najwięcej faktów, liczb oraz konkretów; WAŻNE: jeśli dokument nie niesie większej wartości merytorycznej po prostu zwróć pusty string):\n\n{document}'
    return llm.generate_response(prompt)

def generate_data_summary(llm: LllmInterface, briefs_with_weights: list[tuple[int, str]], max_words: int) -> str:
    logger.info("Generating data summary from briefs with weights")
    formatted_context = ""
    for weight, text in briefs_with_weights:
        if not text or text.strip() == "":
            continue
        formatted_context += f"[WAGA DOKUMENTU: {weight}] TREŚĆ: {text}\n\n"

    if not formatted_context:
        return "Brak danych do wygenerowania streszczenia."

    prompt = (
        f"Jesteś Analitykiem Informacji Strategicznej w MSZ. "
        f"Twoim zadaniem jest przygotowanie 'Streszczenia Wykonawczego' (Executive Summary) całego zbioru danych.\n\n"

        f"### DANE WEJŚCIOWE (NOTATKI Z WAGAMI):\n"
        f"{formatted_context}\n"

        f"### INSTRUKCJE:\n"
        f"1. **Synteza, nie lista:** Nie wymieniaj dokumentów po kolei. Stwórz spójny, narracyjny obraz sytuacji wyłaniający się z tych danych.\n"
        f"2. **Hierarchia Ważności (KLUCZOWE):** Narrację buduj WYŁĄCZNIE na informacjach z dokumentów o wysokiej wadze (np. 8-10). Dokumenty o niskiej wadze traktuj tylko jako tło lub ciekawostkę.\n"
        f"3. **Przejrzystość (User-Friendly):** Tekst ma być zrozumiały dla Ambasadora w 30 sekund. Używaj języka prostego, konkretnego.\n"
        f"4. **Ograniczenia:**\n"
        f"   - Maksymalnie **{max_words} słów**.\n"
        f"   - Język: Polski, profesjonalny.\n"
        f"   - Styl: 2-3 konkretne akapity (bez nagłówków, bez wstępów typu 'Oto streszczenie').\n\n"

        f"Wygeneruj teraz syntetyczne streszczenie danych."
    )

    return llm.generate_response(prompt)

def main():
    with open("config.yaml", "r") as f:
        config_file = yaml.safe_load(f)

    llms = {
        LlmGemini.name(): LlmGemini()
    }

    chosen_llm = llms[LlmGemini.name()]
    summary_cache = SummaryCache()
    with open("./backend/test.txt", "r") as f:
        document = f.read()
    # documents: dict = {} # taken from the scrapping stage
    for id, document in documents:
        summary_cache.add_to_cache(id, generate_brief(chosen_llm, document, config_file["max_brief_words"]))
    logger.info("Briefs added to the SummaryCache")

    data_summary = generate_data_summary(chosen_llm, briefs_with_weights=None, max_words=config_file["max_summary_words"])

    with open("./backend/atlantis_context.txt", "r") as f:
        context = f.read()

    agent = PlanAndSolve()
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

    for hparam in hiperparams:
        logger.info(f"Foreseeing {hparam["type"]} for {hparam["time"]} months ahead")
        out = agent.run(
            llm=llms[LlmGemini.name()],
            hiperparams=hparam,
            context=context,
            brief_prompts=str(summary_cache.cache),
            user_prompt="Generate a strategic report on potential threats and opportunities to Atlantis based on the provided intelligence briefs."
        )
    logger.info(f"Foreseeing done with agent: {agent.name()} and llm: {chosen_llm.name()}.")

    print(out.text)

if __name__ == "__main__":
    main()
