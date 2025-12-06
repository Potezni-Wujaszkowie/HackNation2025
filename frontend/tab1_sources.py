import streamlit as st
from db import init_db, add_source, get_sources, update_source_waga, delete_source
from extract_engine import process_file
import os
from backend.llms.llm_interface import LllmInterface
from backend.llms.llm_gemini import LlmGemini
from backend.summary_cache import SummaryCache
from backend.agents.agent_plan_and_solve import PlanAndSolve
import yaml
from db import add_fakt
import time
# from logguru import logger

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def generate_brief(llm: LllmInterface, document: str, max_words: int) -> str:
    prompt = f'Używając maksymalnie {max_words} słów wygeneruj streszczenie'
    f'poniższego dokumentu (uwzględnij jak najwięcej faktów, liczb oraz konkretów):\n\n{document}'
    return llm.generate_response(prompt)


def generate_AI_output(context_path):
    st.write("context_paths w funkcji generate_AI_output:", context_path)

    with open("config.yaml", "r") as f:
        config_file = yaml.safe_load(f)

    llms = {
        LlmGemini.name(): LlmGemini()
    }

    chosen_llm = llms[LlmGemini.name()]
    # summary_cache = SummaryCache()
    # documents: dict = {} # taken from the scrapping stage

    # shorts = []
    # for context_path in context_paths:
    with open(context_path, "r", encoding="utf-8") as f:
        document = f.read()

    st.write("document w generate_AI_output:", document)

    fakt = generate_brief(chosen_llm, document, config_file["max_brief_words"]).candidates[0].content.parts[0].text
    # logger.info("Generated fact from file %s: %s", context_path.name, fakt)


    st.write("Generated fact from file", context_path.name, ":", generate_brief(chosen_llm, document, config_file["max_brief_words"]))
    st.write("Generated fact:", fakt)
    weight = 0.0
    add_fakt(fakt, os.path.splitext(context_path.name)[0], weight)


def tab1_view():
    st.header("Źródła")

    init_db()

    chosen_option = st.radio(
        "Wybierz opcję dodawania:", ["Dodaj URL", "Dodaj plik"], horizontal=True
    )

    if chosen_option == "Dodaj URL":
        st.subheader("Dodaj nowy URL")
        new_tab1_url = st.text_input(
            "Nowy adres:", placeholder="https://przykladowa_strona.pl"
        )
        new_tab1_url_desc = st.text_input("Opis:", "")
        if st.button("➕ Dodaj URL"):
            if new_tab1_url.strip():
                add_source("url", new_tab1_url.strip(), new_tab1_url_desc, 0.0)
                st.success("Dodano URL!")

    else:
        st.subheader("Dodaj plik (drag & drop)")
        uploaded_file = st.file_uploader("Wybierz plik:", accept_multiple_files=False)
        new_file_weight = st.number_input("Waga pliku", 0.0, 100.0, 0.0, 0.01)
        new_file_desc = st.text_input("Opis:", "")

        if uploaded_file and st.button("➕ Dodaj plik"):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)

            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            add_source("file", file_path, new_file_desc, new_file_weight)
            process_file(file_path)
            
            time.sleep(1)

            output_path = "./uploads_text"
            file_name_without_ext = os.path.splitext(uploaded_file.name)[0]
            file_name_txt = file_name_without_ext + ".txt"
            context_path = os.path.join(output_path, file_name_txt)
            fact_text = generate_AI_output(context_path) 



            # st.write("context_path: ", context_path)
            # st.write("file_path: ", file_path)
            

            # context_paths = []
            # output_path = "./uploads_text"

            # for file_name in os.listdir(output_path):
            #     if file_name.endswith(".txt"):
            #         context_path = os.path.join(output_path, file_path)
            #         context_paths.append(context_path)
            # shorts = 

            st.success(f"Dodano plik: {uploaded_file.name}")

    st.markdown("---")
    st.subheader("Dodane źródła")

    # --- lista źródeł z bazy ---
    sources = get_sources()
    for source_id, typ, nazwa, opis, waga, data in sources:
        col1, col2, col3, col4, col5 = st.columns([0.6, 0.2, 0.2, 0.2, 0.2])
        with col1:
            display_name = os.path.basename(nazwa) if typ == "file" else nazwa
            st.write(display_name)
        with col2:
            st.write(opis)
        with col3:
            new_waga = st.number_input(
                "Waga", 0.0, 100.0, value=waga, step=0.01, key=f"w_{source_id}"
            )
        with col4:
            if st.button("💾 Zapisz", key=f"tab1_save_source_{source_id}"):
                update_source_waga(source_id, new_waga)
                st.rerun()
        with col5:
            if st.button("❌ Usuń", key=f"tab1_del_source_{source_id}"):
                delete_source(source_id)
                st.rerun()
