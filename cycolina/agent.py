from llms.llm_interface import LllmInterface

class Agent:
    def __init__(self, llm: LllmInterface):
        self.llm = llm

    def get_phase1_control_prompt(self) -> str:
        ...
        # zwraca prompt sterujący (streść pliki)

