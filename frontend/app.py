import streamlit as st
import sys
import subprocess
import os
from backend.agent_manager import AgentManager
from backend.agents.agent_plan_and_solve import PlanAndSolve
from backend.llms.llm_gemini import LlmGemini
from backend.llms.llm_pllum import LlmPllum
from tab1_sources import tab1_view
from tab2_facts import tab2_view
from tab3_analysis import tab3_view


def main():
    st.title("Cyfrowy Wieszcz")
    option = st.selectbox(
        "Wybierz model",
        ["PLLUM", "Gemini"],
        index=1,
    )


    tab1, tab2, tab3 = st.tabs(
        ["1. Źródła", "2. Fakty i założenia", "3. Przewidywania i analiza"]
    )

    llm_manager = AgentManager(
        default_llm=LlmGemini().name(),
        default_agent=PlanAndSolve().name()
    )

    if option == "Gemini":
        llm_manager.set_llm(LlmGemini().name())
    elif option == "PLLUM":
        llm_manager.set_llm(LlmPllum().name())
    
    with tab1:
        tab1_view(llm_manager)

    with tab2:
        tab2_view(llm_manager)

    with tab3:
        tab3_view()


    
if __name__ == "__main__":
    main()