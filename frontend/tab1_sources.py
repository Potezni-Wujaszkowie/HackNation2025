import streamlit as st
from db import init_db, add_source, get_sources, update_source_waga, delete_source
import os

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def tab1_view():
    st.header("Źródła")

    init_db()  # upewniamy się, że tabela istnieje

    chosen_option = st.radio(
        "Wybierz opcję dodawania:", ["Dodaj URL", "Dodaj plik"], horizontal=True
    )

    if chosen_option == "Dodaj URL":
        st.subheader("Dodaj nowy URL")
        new_tab1_url = st.text_input(
            "Nowy adres:", placeholder="https://przykladowa_strona.pl"
        )

        if st.button("+ Dodaj URL"):
            if new_tab1_url.strip():
                add_source("url", new_tab1_url.strip(), 0.0)
                st.success("Dodano URL!")

    else:
        st.subheader("Dodaj plik (drag & drop)")
        uploaded_file = st.file_uploader("Wybierz plik:", accept_multiple_files=False)
        new_file_weight = st.number_input("Waga pliku", 0.0, 100.0, 0.0, 0.01)

        if uploaded_file and st.button("+ Dodaj plik"):
            file_path = os.path.join(UPLOAD_FOLDER, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            add_source("file", file_path, new_file_weight)
            st.success(f"Dodano plik: {uploaded_file.name}")

    st.markdown("---")
    st.subheader("Dodane źródła")

    # --- lista źródeł z bazy ---
    sources = get_sources()
    for source_id, typ, nazwa, waga, data in sources:
        col1, col2, col3, col4 = st.columns([0.6, 0.2, 0.2, 0.2])
        with col1:
            display_name = os.path.basename(nazwa) if typ == "file" else nazwa
            st.write(display_name)
        with col2:
            new_waga = st.number_input(
                "Waga", 0.0, 100.0, value=waga, step=0.01, key=f"w_{source_id}"
            )
        with col3:
            if st.button("💾 Zapisz", key=f"save_{source_id}"):
                update_source_waga(source_id, new_waga)
                st.rerun()
        with col4:
            if st.button("🗑️ Usuń", key=f"del_{source_id}"):
                delete_source(source_id)
                st.rerun()
