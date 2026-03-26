import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="BRAINROT COLLECTOR", layout="wide")

# Connexion via le fichier JSON que tu viens d'ajouter
@st.cache_resource
def connect_to_gsheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # On lit le fichier creds.json directement sur GitHub
    creds = Credentials.from_service_account_file("creds.json", scopes=scope)
    return gspread.authorize(creds)

try:
    gc = connect_to_gsheet()
    # Ton ID de Sheet
    sh = gc.open_by_key("1QpDkvd06ZmAWbVmFvpOdFO0_Tb3UvNMVnPlSy3hPzwQ")
    worksheet = sh.get_worksheet(0)
    df = pd.DataFrame(worksheet.get_all_records())
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

st.title("💎 BRAINROT COLLECTOR")

# Affichage des items
if not df.empty:
    for index, row in df.iterrows():
        c1, c2 = st.columns([1, 9])
        with c1:
            val = str(row.get('possede', 0))
            if st.button("✅" if val == "1" else "⬜", key=f"btn_{index}"):
                new_val = 1 if val == "0" else 0
                worksheet.update_cell(index + 2, 5, new_val) # Colonne 5 = 'possede'
                st.rerun()
        with c2:
            st.write(f"**{row.get('nom', 'Inconnu')}**")
        with c2:
            st.write(f"**{row.get('nom', 'Inconnu')}**")
else:
    st.warning("Le tableau est vide.")
