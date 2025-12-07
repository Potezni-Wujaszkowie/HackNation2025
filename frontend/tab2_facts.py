import streamlit as st
import pandas as pd
from datetime import datetime
from db import add_fakt, init_db, get_all_fakty, update_waga, delete_fakt, get_fakt_by_id
from loguru import logger
from extract_engine import TEXT_OUTPUT_FOLDER
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import json


        # shorts.append()

    # return shorts

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


def generate_final_AI_output(selected_ids, llm_manager):
    """
    Logika generowania finalnego outputu AI na podstawie zaznaczonych faktów w tab2_view.
    :param selected_ids: Lista ID zaznaczonych faktów
    """
    st.write("Generating final AI output based on selected facts...")
    facts_list = []

    for fakt_id in selected_ids:
        fakt_record = get_fakt_by_id(fakt_id)
        if fakt_record:
            fakt_id, fakt_text, zrodlo, waga, data = fakt_record
            facts_list.append((waga, fakt_text, zrodlo))
        else:
            logger.warning(f"Fakt with ID {fakt_id} not found in database.")

    model_output = llm_manager.generate_scenarios_and_summary(facts_list)
    return model_output


def tab2_view(llm_manager):
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
    # st.header("Fakty")

    init_db()

    with st.expander("Dodaj nowy fakt lub założenie", expanded=False):
        fakt = st.text_area("Fakt lub założenie", height=150)
        weight = st.number_input("Waga", 0.0, 100.0, value=0.0, step=0.01)

        if st.button("➕ Dodaj fakt"):
            if fakt.strip():
                add_fakt(fakt, "Dodane przez użytkownika", weight)
                st.success("Dodano fakt do bazy!")
            else:
                st.warning("Fakt nie może być pusty.")


    selected_ids = []
    st.write("---")
    if st.button("🤖 Generuj predykcje dla wybranych faktów", key=f"tab2_generate_facts"):
            model_output = generate_final_AI_output(selected_ids, llm_manager)
            generate_pdf_report(model_output, os.path.join(TEXT_OUTPUT_FOLDER, f"analiza_atlantis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"))
            st.success("Wygenerowano odpowidź na podstawie zaznaczonych faktów.")

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
        
        

            # context_paths = []
            # output_path = "./uploads_text"

            # for file_name in os.listdir(output_path):
            #     if file_name.endswith(".txt"):
            #         context_path = os.path.join(output_path, file_name)
            #         context_paths.append(context_path)

            # shorts = generate_AI_output(context_paths)


            # logger.info(f"context_paths: {context_paths}")
            # st.write("Shorts: ", shorts)


            
            
            
            
        if selected_ids:
            # st.write("Shorts: ", shorts)
            st.write("Zaznaczone ID:", selected_ids)


def generate_pdf_report(output_dict, filename):
    """
    Generuje raport PDF z podanymi analizami.

    :param output_dict: słownik z wynikami AI
    :param filename: Nazwa pliku PDF do wygenerowania
    """
    # Zarejestruj czcionkę Arial (plik Arial.ttf musi być w katalogu projektu)
    try:
        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
    except Exception as e:
        st.warning(f"Nie znaleziono czcionki Arial.ttf: {e}")
        st.info("Polskie znaki mogą nie być poprawnie wyświetlane w PDF.")

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    arial_body = ParagraphStyle('ArialBody', parent=styles['BodyText'], fontName='Arial', fontSize=12)
    arial_title = ParagraphStyle('ArialTitle', parent=styles['Title'], fontName='Arial', fontSize=18)
    arial_heading1 = ParagraphStyle('ArialHeading1', parent=styles['Heading1'], fontName='Arial', fontSize=14)
    arial_heading2 = ParagraphStyle('ArialHeading2', parent=styles['Heading2'], fontName='Arial', fontSize=12)

    story = []
    story.append(Paragraph("Analiza strategiczna dla państwa Atlantis", arial_title))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("1. Streszczenie dokumentu", arial_heading1))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(output_dict["data_summary"], arial_body))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("2. Scenariusze", arial_heading1))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("2.1 Scenariusz pozytywny 12-miesięczny", arial_heading2))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(output_dict["scenarios"][0], arial_body))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("2.2 Scenariusz pozytywny 36-miesięczny", arial_heading2))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(output_dict["scenarios"][2], arial_body))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("2.3 Scenariusz negatywny 12-miesięczny", arial_heading2))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(output_dict["scenarios"][1], arial_body))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("2.4 Scenariusz negatywny 36-miesięczny", arial_heading2))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(output_dict["scenarios"][3], arial_body))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("3. Rekomendacje", arial_heading1))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("3.1 Unikanie scenariuszy negatywnych", arial_heading2))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(output_dict["recommendations"], arial_body))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph("3.2 Generowanie scenariuszy pozytywnych", arial_heading2))
    story.append(Spacer(1, 0.5 * cm))

    story.append(Paragraph(output_dict["recommendations"], arial_body))
    story.append(Spacer(1, 0.5 * cm))

    doc.build(story)
    st.success(f"Raport PDF został wygenerowany: {filename}")

    
    txt_filename = filename.replace(".pdf", ".txt")
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(json.dumps(output_dict, ensure_ascii=False, indent=2))
    st.success(f"Zapisano także plik tekstowy: {txt_filename}")