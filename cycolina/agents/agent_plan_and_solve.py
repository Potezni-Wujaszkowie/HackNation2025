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
            f"You are the Chief Strategic Intelligence Analyst for Atlantis. "
            f"Your task is to analyze raw intelligence data and create a STRATEGIC REASONING PLAN.\n\n"

            f"### STATIC CONTEXT (ATLANTIS PROFILE):\n{system_prompt}\n\n"

            f"### CONVERSATION HISTORY (CONTEXT):\n"
            f"{chat_history}\n\n"

            f"### INPUT DATA (INTELLIGENCE BRIEFS):\n{brief_prompts}\n\n"

            f'### THE USER PROMPT (USER QUESTION OR INTENT):\n{user_prompt}\n\n'

            f"### INSTRUCTIONS:\n"
            f"Analyze the input data and outline your reasoning strategy. DO NOT write the final report yet. "
            f"Instead, produce a structured plan covering:\n"
            f"1. **Relevance Filter:** Which specific documents (cite IDs) are critical for Atlantis's security/economy?\n"
            f"2. **Correlation Analysis:** Identify hidden links between documents (e.g., [DOC_1] + [DOC_4] implies Risk X).\n"
            f"3. **Scenario Skeleton:** Briefly define the 4 required scenarios (12m+/-, 36m+/-). For each, list the 'Trigger Event' and the 'Chain of Causality'.\n"
            f"4. **Citation Strategy:** List which ID you will use to prove each major claim.\n\n"
            f"5. **Formatting:** Do NOT use email/memo headers (To/From/Date/Subject). Start the response IMMEDIATELY with the exact string '**SECTION A: Executive Summary**'.\n\n"
            f"Output your response as a structured thinking process."
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
            f"You are the Diplomatic Report Writer for the Republic of Atlantis. "
            f"Execute the provided reasoning plan to generate the final Strategic Foresight Report.\n\n"

            f"### STATIC CONTEXT (ATLANTIS PROFILE):\n{system_prompt}\n\n"

            f"### INPUT DATA (INTELLIGENCE BRIEFS):\n{brief_prompts}\n\n"

            f"### CONVERSATION HISTORY:\n"
            f"{chat_history}\n\n"

            f"### ANALYST'S REASONING PLAN:\n{plan}\n\n"

            f'### THE USER PROMPT (USER QUESTION OR INTENT):\n{user_prompt}\n\n'

            f"### EXECUTION INSTRUCTIONS:\n"
            f"Write the final report (2000-3000 words) strictly following the Plan above.\n"
            f"Structure:\n"
            f"**SECTION A: Executive Summary**\n"
            f"**SECTION B: Strategic Scenarios** (For each: Narrative, Chain of Thought, Impact)\n"
            f"**SECTION C: Recommendations** (Defensive/Offensive)\n\n"

            f"### CRITICAL RULES:\n"
            f"1. **Explainability:** CITATIONS ARE MANDATORY. You must cite source IDs (e.g., [DOC_01]) for every claim.\n"
            f"2. **Tone:** Professional, diplomatic, tailored to the Ambassador.\n"
            f"3. **Continuity:** If the user asked for a change, ensure this report reflects that change compared to history.\n"
            f"4. **No Appendices:** Do not list source data at the end (the system will handle that).\n\n"

            f"Generate the final report content now."
        )

        return llm.generate_response(solving_prompt)
