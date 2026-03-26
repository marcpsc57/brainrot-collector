import streamlit as st
import pandas as pd
import gspread
import json
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="BRAINROT COLLECTOR", layout="wide")

@st.cache_resource
def connect_to_gsheet():
    # On récupère la ligne de texte MY_JSON_KEY
    json_text = st.secrets["MY_JSON_KEY"]
    # On la transforme en vrai dictionnaire
    info = json.loads(json_text)
    
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    return gspread.authorize(creds)

try:
    gc = connect_to_gsheet()
    # On ouvre ton Sheet
    sh = gc.open_by_key("1QpDkvd06ZmAWbVmFvpOdFO0_Tb3UvNMVnPlSy3hPzwQ")
    worksheet = sh.get_worksheet(0)
    df = pd.DataFrame(worksheet.get_all_records())
    st.success("C'est connecté ! 🎉")
    st.dataframe(df)
except Exception as e:
    st.error(f"Erreur : {e}")
            worksheet.update_cell(index + 2, 5, new_val)
            st.rerun()
    with c2:
        st.write(f"**{row.get('nom', 'Inconnu')}**")
