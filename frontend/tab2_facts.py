import streamlit as st
import pandas as pd
from datetime import datetime

def tab2_view():
    st.header("Fakty")

    if "tab2_data" not in st.session_state:
        st.session_state.tab2_data = pd.DataFrame(
            [{
                "fakt": "Pierwszy testowy fakt",
                "zrodlo": "System",
                "waga": 1.0,
                "data": "2025-01-01 00:00:00",
            }]
        )

    def update_weight(idx, new_weight):
        st.session_state.tab2_data.at[idx, "waga"] = float(new_weight)

    def delete_row(idx):
        st.session_state.tab2_data = st.session_state.tab2_data.drop(idx).reset_index(drop=True)
        st.rerun()

    # FORM
    with st.expander("➕ Dodaj nowy fakt", expanded=False):
        fakt = st.text_area("Fakt")
        weight = st.number_input("Waga", 0.0, 1.0, value=1.0, step=0.01)

        if st.button("Dodaj"):
            if fakt.strip():
                new = {
                    "fakt": fakt,
                    "zrodlo": "Dodane przez użytkownika",
                    "waga": float(weight),
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.tab2_data = pd.concat(
                    [st.session_state.tab2_data, pd.DataFrame([new])],
                    ignore_index=True
                )
                st.rerun()

    st.write("---")
    st.subheader("📄 Lista faktów")

    for idx, row in st.session_state.tab2_data.iterrows():
        st.markdown(
            f"""
            <div style="
                padding:18px; 
                border:1px solid #e0e0e0;
                border-radius:12px; 
                margin-bottom:14px;
                background:#fafafa; 
                box-shadow:0 2px 4px rgba(0,0,0,0.05);
                color:#000000;         /* <- tekst zawsze czarny */
                font-size:16px;
            ">
                <b>📌 Fakt:</b><br>{row['fakt']}<br><br>
                <b>📁 Źródło:</b> {row['zrodlo']}<br>
                <b>🎯 Waga:</b> {row['waga']}<br>
                <b>📅 Data:</b> {row['data']}
            </div>
            """,
            unsafe_allow_html=True
        )


        new_weight = st.slider(
            "Zmień wagę", 0.0, 1.0, float(row["waga"]),
            step=0.01, key=f"sl_{idx}"
        )

        if st.button("💾 Zapisz", key=f"save_{idx}"):
            update_weight(idx, new_weight)
            st.rerun()

        if st.button("🗑️ Usuń", key=f"del_fact_{idx}"):
            delete_row(idx)
