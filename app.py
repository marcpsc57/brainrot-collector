import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import os

# 1. CONFIG
st.set_page_config(page_title="BRAINROT COLLECTOR", page_icon="💎", layout="wide")

# 2. CONNEXION VIA LE FICHIER JSON
@st.cache_resource
def get_gspread_client():
    # On définit les accès
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # On cherche le fichier creds.json que tu as mis sur GitHub
    if os.path.exists("creds.json"):
        creds = Credentials.from_service_account_file("creds.json", scopes=scope)
    else:
        st.error("Fichier creds.json introuvable sur GitHub !")
        st.stop()
        
    return gspread.authorize(creds)

# 3. LECTURE DU SHEET
SHEET_ID = "1QpDkvd06ZmAWbVmFvpOdFO0_Tb3UvNMVnPlSy3hPzwQ"

try:
    gc = get_gspread_client()
    sh = gc.open_by_key(SHEET_ID)
    worksheet = sh.get_worksheet(0)
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

# 4. INTERFACE
st.title("💎 BRAINROT COLLECTOR")

if not df.empty:
    for index, row in df.iterrows():
        c1, c2 = st.columns([1, 9])
        with c1:
            is_owned = str(row.get('possede', 0)) == "1"
            if st.button("✅" if is_owned else "⬜", key=f"btn_{index}"):
                new_val = 0 if is_owned else 1
                # On met à jour la colonne E (5)
                worksheet.update_cell(index + 2, 5, new_val)
                st.rerun()
        with c2:
            st.write(f"**{row.get('nom', 'Inconnu')}**")
else:
    st.warning("Le tableau est vide.")
