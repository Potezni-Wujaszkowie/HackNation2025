from llms.llm_gemini import LlmGemini
from summary_cache import SummaryCache
from agents.agent_plan_and_solve import PlanAndSolve

def main():
    # get from
    summary_cache = SummaryCache()
    summary_cache.add_to_cache("DOC_1", "Summary of document 1...")
    summary_cache.add_to_cache("DOC_2", "Summary of document 2...")
    llms = {
        LlmGemini.name(): LlmGemini()
    }
    with open("atlantis_context.txt", "r") as f:
        context = f.read()

    brief_prompts = str(summary_cache.cache)

    agent = PlanAndSolve()
    out = agent.run(
        llm=llms[LlmGemini.name()],
        context=context,
        brief_prompts=brief_prompts,
        user_prompt="Generate a strategic report on potential economic threats to Atlantis over the next 5 years based on the provided intelligence briefs."
    )
    print(out)


if __name__ == "__main__":
    main()
