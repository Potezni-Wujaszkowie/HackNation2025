import streamlit as st
import pandas as pd
from datetime import datetime
from db import add_fakt, init_db, get_all_fakty, update_waga, delete_fakt
from loguru import logger
from extract_engine import TEXT_OUTPUT_FOLDER
import os
from backend.llms.llm_interface import LllmInterface
from backend.llms.llm_gemini import LlmGemini
from backend.summary_cache import SummaryCache
from backend.agents.agent_plan_and_solve import PlanAndSolve
import yaml

def generate_brief(llm: LllmInterface, document: str, max_words: int) -> str:
    prompt = f'Używając maksymalnie {max_words} słów wygeneruj streszczenie'
    f'poniższego dokumentu (uwzględnij jak najwięcej faktów, liczb oraz konkretów):\n\n{document}'
    return llm.generate_response(prompt)


def generate_AI_output(context_paths):

    
    with open("config.yaml", "r") as f:
        config_file = yaml.safe_load(f)

    llms = {
        LlmGemini.name(): LlmGemini()
    }

    chosen_llm = llms[LlmGemini.name()]
    summary_cache = SummaryCache()
    documents: dict = {} # taken from the scrapping stage

    shorts = []
    for context_path in context_paths:
        with open(context_path, "r", encoding="utf-8") as f:
            document = f.read()

        shorts.append(generate_brief(chosen_llm, document, config_file["max_brief_words"]))

    return shorts

    # shorts = []
    # for id, document in documents:
        
    
    # logger.info("Briefs added to the SummaryCache")

    # #TODO tutaj pętla po context_path i scalenie ich do jednej zmiennej context
    # with open(context_path, "r") as f:
    #     context = f.read()

    # agent = PlanAndSolve()
    # out = agent.run(
    #     llm=llms[LlmGemini.name()],
    #     context=context,
    #     brief_prompts=str(summary_cache.cache),
    #     user_prompt="Generate a strategic report on potential economic threats to Atlantis over the next 5 years based on the provided intelligence briefs."
    # )
    # logger.info(f"Foreseeing done with agent: {agent.name()} and llm: {chosen_llm.name()}.")

    # print(out.text)


def tab2_view():
    st.markdown(
        """
        <style>
        .stButton button {
            white-space: nowrap !important;
            min-width: 90px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.header("Fakty")

    init_db()

    with st.expander("Dodaj nowy fakt", expanded=False):
        fakt = st.text_area("Fakt")
        weight = st.number_input("Waga", 0.0, 100.0, value=0.0, step=0.01)

        if st.button("➕ Dodaj fakt"):
            if fakt.strip():
                add_fakt(fakt, "Dodane przez użytkownika", weight)
                st.success("Dodano fakt do bazy!")
            else:
                st.warning("Fakt nie może być pusty.")

    st.write("---")
    with st.expander("Wylistuj wszystkie fakty", expanded=False):
        st.subheader("Filtry")
        st.info("Zaznacz fakty, które AI ma wziąć pod uwagę podczas generowania odpowiedzi (domyślnie wszystkie są zaznaczone).")

        col_src, col_sort = st.columns([0.5, 0.5])
        with col_src:
            filter_src = st.text_input(
                "Filtruj po nazwie źródła", value="", key="filter_src"
            )
        with col_sort:
            sort_order = st.selectbox(
                "Sortuj wg daty:", ["Od najnowszej", "Od najstarszej"], key="sort_date"
            )

        fakty = get_all_fakty()
        filtered_facts = []
        for fakt in fakty:
            _id, _text, _src, _waga, _data = fakt
            if filter_src.strip() == "" or filter_src.strip().lower() in _src.lower():
                filtered_facts.append(fakt)

        filtered_facts.sort(key=lambda x: x[4], reverse=(sort_order == "Od najnowszej"))

        selected_ids = []
        if not filtered_facts:
            st.info("Brak faktów spełniających kryteria.")
        else:
            for fakt_id, fakt_text, zrodlo, waga, data in filtered_facts:
                col_chk, col_fakt, col_waga, col_zapisz, col_del = st.columns(
                    [0.05, 0.35, 0.1, 0.15, 0.15]
                )

                with col_chk:
                    checked = st.checkbox("", key=f"chk_{fakt_id}", value=True)
                    if checked:
                        selected_ids.append(fakt_id)

                with col_fakt:
                    st.markdown(
                        f"""
                        <div style="
                            padding:18px; border:1px solid #e0e0e0;
                            border-radius:12px; margin-bottom:14px;
                            background:#fafafa; box-shadow:0 2px 4px rgba(0,0,0,0.05);
                            color:#000000; font-size:16px;
                        ">
                            <b>🎯 Fakt:</b><br>{fakt_text}<br><br>
                            <b>ℹ️ Źródło:</b> {zrodlo}<br>
                            <b>⚖️ Waga:</b> {waga}<br>
                            <b>📅 Data:</b> {data}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col_waga:
                    nowa_waga = st.number_input(
                        "Waga istotności",
                        min_value=0.0,
                        max_value=100.0,
                        value=waga,
                        step=0.01,
                        key=f"tab2_weight_fact_{fakt_id}",
                    )

                with col_zapisz:
                    if st.button("💾 Zapisz", key=f"tab2_save_fact_{fakt_id}"):
                        update_waga(fakt_id, nowa_waga)
                        st.success("Zapisano zmiany w wadze.")

                with col_del:
                    if st.button("❌ Usuń", key=f"tab2_del_fact_{fakt_id}"):
                        delete_fakt(fakt_id)
                        st.rerun()
        
        if st.button("GENERATE", key=f"tab2_generate_facts"):
            # tutaj chce pętle która która do listy zapisze wszystkie ścieżki do plików z folderu TEXT_OUTPUT_FOLDER
            context_paths = []

            for file_name in os.listdir(TEXT_OUTPUT_FOLDER):
                if file_name.endswith(".txt"):
                    context_path = os.path.join(TEXT_OUTPUT_FOLDER, file_name)
                    context_paths.append(context_path)

            shorts = generate_AI_output(context_paths)
            st.write("Shorts: ", shorts)

            
            
            
            st.success("Wygenerowano odpowidź na podstawie zaznaczonych faktów.")

        if selected_ids:
            st.write("Shorts: ", shorts)
            # st.write("Zaznaczone ID:", selected_ids)
