from loguru import logger

from agent_interface import AgentInterface
from llms.llm_interface import LllmInterface


class MRKL(AgentInterface):
    def __init__(self):
        pass

    def name(self) -> str:
        return "Mrkl"

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

    @staticmethod
    def get_extract_table_prompt(sql_context: str, sql_prompt: str, previous_attempts_str: str = "") -> str:
        return (
            "Based on provided SQL context you need to extract what tables are useful in context of <Prompt>, "
            + "those columns will later be used to generate query to answer this question."
            + "Return only names in format of 'table.column_name', do not generate SQL QUERY yet.\n\n"
            + f"<Context>{sql_context}</Context>\n\n"
            + f"<Prompt>{sql_prompt}</Prompt>\n"
            + previous_attempts_str
        )

    @staticmethod
    def get_sql_generation_prompt(
        sql_context: str, sql_prompt: str, extract_tables: str, previous_attempts_str: str = ""
    ):
        return (
            "Based on provided SQL context, column names in format of 'table.column_name', your task is to generate query which will answer in <Prompt>."
            + "Generated SQL must precisely answer question. Do not return any additional data. Generated code needs to be valid SQL query which will be executed\n\n"
            + "Return only the SQL query, no explanations, no backticks.\n\n"
            + f"<Context>{sql_context}</Context>\n\n"
            + f"<Table_to_extract>{extract_tables}</Table_to_extract>\n\n"
            + f"<Prompt>{sql_prompt}</Prompt>\n"
            + previous_attempts_str
        )

    async def run(
        self, llm: LLMProvider, sql_context: str, sql_prompt: str, previous_attempts: list[dict] = None
    ) -> str:
        with self.lf_client.start_as_current_span(
            name="MRKL_Run",
            metadata={"approach": "MRKL", "llm": llm.name()},
        ) as run:
            logger.info("Running MRKL approach")

            prev_attempts_str = self._format_previous_attempts(previous_attempts)

            extract_tables = llm.generate_text(
                [
                    {
                        "role": "system",
                        "content": MRKL.get_extract_table_prompt(sql_context, sql_prompt, prev_attempts_str),
                    }
                ]
            )

            sqlQuery = llm.generate_text(
                [
                    {
                        "role": "system",
                        "content": MRKL.get_sql_generation_prompt(
                            sql_context, sql_prompt, extract_tables, prev_attempts_str
                        ),
                    }
                ]
            )
            run.update(output=sqlQuery)
            return sqlQuery
