import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="BRAINROT COLLECTOR", layout="wide")

# On récupère la clé depuis les Secrets de Streamlit pour éviter les erreurs ASN.1
try:
    # On reconstruit les infos du compte de service proprement
    info = {
        "type": "service_account",
        "project_id": "brainrot-project-491423",
        "private_key_id": "dd28909d6aaaaf314cc05b83ce8856ff9c9fe03e",
        "private_key": st.secrets["GCP_PRIVATE_KEY"].replace("\\n", "\n"),
        "client_email": "brainrot-bot@brainrot-project-491423.iam.gserviceaccount.com",
        "client_id": "107186528494643778636",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/brainrot-bot%40brainrot-project-491423.iam.gserviceaccount.com"
    }
    
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    gc = gspread.authorize(creds)
    
    # Ouverture du Sheet
    sh = gc.open_by_key("1QpDkvd06ZmAWbVmFvpOdFO0_Tb3UvNMVnPlSy3hPzwQ")
    worksheet = sh.get_worksheet(0)
    df = pd.DataFrame(worksheet.get_all_records())

except Exception as e:
    st.error(f"Erreur fatale : {e}")
    st.info("Vérifie que tu as bien mis 'GCP_PRIVATE_KEY' dans les Secrets de Streamlit Cloud.")
    st.stop()

st.title("💎 BRAINROT COLLECTOR")

if not df.empty:
    for index, row in df.iterrows():
        c1, c2 = st.columns([1, 9])
        with c1:
            # On vérifie la colonne 'possede' (Colonne E)
            is_owned = str(row.get('possede', 0)) == "1"
            if st.button("✅" if is_owned else "⬜", key=f"btn_{index}"):
                new_val = 1 if not is_owned else 0
                worksheet.update_cell(index + 2, 5, new_val)
                st.rerun()
        with c2:
            st.write(f"**{row.get('nom', 'Inconnu')}**")
else:
    st.warning("Le Google Sheet semble vide.")
