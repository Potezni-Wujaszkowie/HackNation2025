from loguru import logger

from backend.agents.agent_interface import AgentInterface, format_previous_attempts
from llms.llm_interface import LllmInterface


class MRKL(AgentInterface):
    def __init__(self):
        pass

    def name(self) -> str:
        return "Mrkl"

    @staticmethod
    def get_extract_table_prompt(context: str, prompt: str) -> str:
        return (
            "Based on provided SQL context you need to extract what tables are useful in context of <Prompt>, "
            + "those columns will later be used to generate query to answer this question."
            + "Return only names in format of 'table.column_name', do not generate SQL QUERY yet.\n\n"
            + f"<Context>{context}</Context>\n\n"
            + f"<Prompt>{prompt}</Prompt>\n"
        )

    @staticmethod
    def get_sql_generation_prompt(
        context: str, prompt: str, extract_tables: str, previous_attempts_str: str = ""
    ):
        return (
            "Based on provided SQL context, column names in format of 'table.column_name', your task is to generate query which will answer in <Prompt>."
            + "Generated SQL must precisely answer question. Do not return any additional data. Generated code needs to be valid SQL query which will be executed\n\n"
            + "Return only the SQL query, no explanations, no backticks.\n\n"
            + f"<Context>{context}</Context>\n\n"
            + f"<Table_to_extract>{extract_tables}</Table_to_extract>\n\n"
            + f"<Prompt>{prompt}</Prompt>\n"
            + previous_attempts_str
        )

    def run(
        self, llm: LllmInterface, hiperparams: dict, context: str, merged_briefs: str
    ) -> str:
        logger.info("Running MRKL approach")

        prev_attempts_str = format_previous_attempts(previous_attempts)

        extract_tables = llm.generate_text(
            [
                {
                    "role": "system",
                    "content": MRKL.get_extract_table_prompt(sql_context, sql_prompt, prev_attempts_str),
                }
            ]
        )

        output = llm.generate_text(
            [
                {
                    "role": "system",
                    "content": MRKL.get_sql_generation_prompt(
                        context, prompt, extract_tables, prev_attempts_str
                    ),
                }
            ]
        )
        return output
