from llms.llm_interface import LllmInterface
from llms.llm_gemini import LlmGemini
from summary_cache import SummaryCache
from agents.agent_plan_and_solve import PlanAndSolve

import yaml

def generate_brief(llm: LllmInterface, document: str, max_words: int) -> str:
    prompt = f'Używając maksymalnie {max_words} słów wygeneruj streszczenie'
    f'poniższego dokumentu (uwzględnij jak najwięcej faktów, liczb oraz konkretów):\n\n{document}'
    return llm.generate_response(prompt)

def main():
    with open("config.yaml", "r") as f:
        config_file = yaml.safe_load(f)

    llms = {
        LlmGemini.name(): LlmGemini()
    }

    chosen_llm = llms[LlmGemini.name()]
    summary_cache = SummaryCache()
    documents: dict = {} # taken from the scrapping stage
    for id, document in documents:
        summary_cache.add_to_cache(id, generate_brief(chosen_llm, document, config_file["max_brief_words"]))

    with open("atlantis_context.txt", "r") as f:
        context = f.read()

    agent = PlanAndSolve()
    out = agent.run(
        llm=llms[LlmGemini.name()],
        context=context,
        brief_prompts=str(summary_cache.cache),
        user_prompt="Generate a strategic report on potential economic threats to Atlantis over the next 5 years based on the provided intelligence briefs."
    )
    print(out)


if __name__ == "__main__":
    main()
