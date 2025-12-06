from agents.agent_interface import AgentInterface
from llms.llm_interface import LllmInterface


class PlanAndSolve(AgentInterface):
    """
    An agentic planning approach that separates 'planning' and 'solving'
    for translating natural language into SQL.
    """

    def __init__(self):
        """
        Initialize the SQL planning agent.
        """
        self.lf_client = get_client()

    @staticmethod
    def name() -> str:
        return "PLAN_AND_SOLVE"

    @staticmethod
    def _format_previous_attempts(previous_attempts: list[dict] | None) -> str:
        if not previous_attempts:
            return ""

        formatted = "\n\n<previous attempt>\n"
        for attempt in previous_attempts:
            formatted += f"- generated sql: {attempt.get('sql', 'N/A')}\n"
            formatted += f"- query result: {attempt.get('error', '') or attempt.get('result', 'N/A')}\n"
        formatted += "</previous attempt>\n"
        return formatted

    async def run(
        self, llm: LLMProvider, sql_context: str, sql_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        """
        Run the agentic approach: planning + solving.
        """
        with self.lf_client.start_as_current_span(
            name="Plan_And_Solve_Run",
            metadata={"approach": "PLAN_AND_SOLVE", "llm": llm.name()},
        ) as run:
            reasoning_plan = await self.plan(llm, sql_context, sql_prompt, previous_attempts)
            sql_query = await self.solve(llm, sql_context, reasoning_plan, sql_prompt, previous_attempts)
            run.update(output=sql_query)

        return sql_query

    async def plan(
        self, llm: LLMProvider, system_prompt: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        """
        Planning — understand intent and design an execution strategy.
        """
        prev_attempts_str = self._format_previous_attempts(previous_attempts)

        planning_prompt = (
            f"You are an expert AI agent that plans how to translate natural "
            f"language questions into SQL queries.\n\n"
            f"### Database schema and context:\n{system_prompt}\n\n"
            f"### User query:\n{user_prompt}\n\n"
            + prev_attempts_str
            + "\nAnalyze the user query and describe your reasoning plan step-by-step, identifying:\n"
            "- The user’s intent\n"
            "- The relevant tables and columns (based on schema)\n"
            "- Any joins, filters, or aggregations needed\n"
            "Do NOT write SQL yet — only describe the plan."
        )

        return await llm.generate_text(
            messages=[
                {"role": "system", "content": "You are a planning agent specializing in SQL translation."},
                {"role": "user", "content": planning_prompt},
            ],
        )

    async def solve(
        self, llm: LLMProvider, system_prompt: str, plan: str, user_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        """
        Solving — generate SQL query using the reasoning plan and schema context.
        """
        prev_attempts_str = self._format_previous_attempts(previous_attempts)

        solving_prompt = (
            f"You are an expert SQL generation agent.\n\n"
            f"### Database schema and context:\n{system_prompt}\n\n"
            f"### Reasoning plan:\n{plan}\n\n"
            f"### User request:\n{user_prompt}\n\n"
            + prev_attempts_str
            + "\nNow generate the final SQL query that fulfills the user request. "
            "Use only the tables and columns defined in the schema. "
            "Return only the SQL query, no explanations."
        )

        return await llm.generate_text(
            messages=[
                {"role": "system", "content": "You are an SQL generation agent."},
                {"role": "user", "content": solving_prompt},
            ],
        )
