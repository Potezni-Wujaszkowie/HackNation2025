import streamlit as st
import pandas as pd
from datetime import datetime
from db import add_fakt, init_db, get_all_fakty, update_waga, delete_fakt


def tab2_view():
    st.header("Fakty")

    init_db()  # upewniamy się, że tabela istnieje

    # --- Dodawanie nowego faktu ---
    with st.expander("➕ Dodaj nowy fakt", expanded=False):
        fakt = st.text_area("Fakt")
        weight = st.number_input("Waga", 0.0, 1.0, value=1.0, step=0.01)

        if st.button("Dodaj fakt"):
            if fakt.strip():
                add_fakt(fakt, "Dodane przez użytkownika", weight)
                st.success("Dodano fakt do bazy!")
            else:
                st.warning("Fakt nie może być pusty.")

    st.write("---")
    with st.expander("📄 Wylistuj wszystkie fakty", expanded=False):

        # --- Pobranie danych z bazy ---
        fakty = get_all_fakty()
        selected_ids = []

        for fakt_id, fakt_text, zrodlo, waga, data in fakty:
            col_chk, col_fakt, col_waga, col_del = st.columns([0.05, 0.6, 0.25, 0.1])

            # checkbox do zaznaczania
            with col_chk:
                checked = st.checkbox("", key=f"chk_{fakt_id}")
                if checked:
                    selected_ids.append(fakt_id)

            # wyświetlanie faktu
            with col_fakt:
                st.markdown(
                    f"""
                    <div style="
                        padding:18px; border:1px solid #e0e0e0;
                        border-radius:12px; margin-bottom:14px;
                        background:#fafafa; box-shadow:0 2px 4px rgba(0,0,0,0.05);
                        color:#000000; font-size:16px;
                    ">
                        <b>📌 Fakt:</b><br>{fakt_text}<br><br>
                        <b>📁 Źródło:</b> {zrodlo}<br>
                        <b>🎯 Waga:</b> {waga}<br>
                        <b>📅 Data:</b> {data}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            # slider do edycji wagi
            with col_waga:
                new_waga = st.slider(
                    "Zmień wagę", 0.0, 1.0, value=waga, step=0.01, key=f"sl_{fakt_id}"
                )
                if new_waga != waga:
                    update_waga(fakt_id, new_waga)

            # przycisk do usuwania
            with col_del:
                if st.button("🗑️", key=f"del_{fakt_id}"):
                    delete_fakt(fakt_id)

        # --- Wyświetlenie zaznaczonych ID ---
        if selected_ids:
            st.write("Zaznaczone ID:", selected_ids)
