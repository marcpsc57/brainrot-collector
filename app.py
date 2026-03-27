import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="BRAINROT COLLECTOR", layout="wide")

@st.cache_resource
def connect_to_gsheet():
    # On récupère le dictionnaire directement depuis les secrets de Streamlit
    # Ça évite toute corruption de texte ou d'encodage
    info = st.secrets["gcp_service_account"]
    
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    return gspread.authorize(creds)

try:
    gc = connect_to_gsheet()
    sh = gc.open_by_key("1QpDkvd06ZmAWbVmFvpOdFO0_Tb3UvNMVnPlSy3hPzwQ")
    worksheet = sh.get_worksheet(0)
    df = pd.DataFrame(worksheet.get_all_records())
except Exception as e:
    st.error(f"Erreur : {e}")
    st.stop()

st.title("💎 BRAINROT COLLECTOR")

if not df.empty:
    for index, row in df.iterrows():
        c1, c2 = st.columns([1, 9])
        with c1:
            is_owned = str(row.get('possede', 0)) == "1"
            if st.button("✅" if is_owned else "⬜", key=f"btn_{index}"):
                new_val = 1 if not is_owned else 0
                worksheet.update_cell(index + 2, 5, new_val)
                st.rerun()
        with c2:
            st.write(f"**{row.get('nom', 'Inconnu')}**")
