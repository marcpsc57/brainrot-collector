import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# 1. CONFIGURATION
st.set_page_config(page_title="BRAINROT COLLECTOR", page_icon="💎", layout="wide")

# 2. TES ACCÈS (On les nettoie nous-mêmes)
def get_gspread_client():
    info = {
        "type": "service_account",
        "project_id": "brainrot-app-491421",
        "private_key_id": "5e47d0ba10b7451547eff21bd09d1243962a2ecd",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC6O4z/IuX76f5O\nF75r1osxNpRLZbyWnKhn6h2VOx6ihMec7QqsEopZUlNY42GZCEISbCKlL97C+0wB\nJfo0BjjQf+D4PTY0gZ3pLRk4GMXDBdjs1Qm+9Cr1pN7vhsmPSVQXf5N8B/RDrjpa\nz+uTBfGTVkpOpDvOo31d1pL/WnEkKZMZ5dhPpticKE5mb1OMhZg0hyjBjXt59y1v\nwXfkJZHDOG44WmBY/7s4IDkB+ALCXO8RZq49uTZ03nyxL+GFsTUqjuZ7cJ/X6pIf\n4w27avtJtd/sZSRaHow1TBqweVqaED6zHEfuOlPZyh+fBwVBcjWYr25YtloMEAKy\no6M96dDpAgMBAAECggEAD1HrSyjEiRjqc+OlpUrgp/OAtwQfQ7eO7f93IAndPwrT\nve/NDzM2QNtSIm+QHY3tm4TcQ8EAnwMbsUN9xe5WGabPa7RjY2XfRumQF8qH6D9w\npSjwVI5TA2Kk+UjaB2jFm2pCCHPCDxhD0iklDLLyOMfiNH5zsg/GdiP68zkuMgZ6\nf0RBkvwVGYF5sMVesu0ZZ3VmPGYIG4YjH/Kif1IQbyfreqCpjGgVqPcoPzssh/GA\nfRdUL7zMQxAHBwxnXbWA+j7GuvYdJLXzNGHVV1d8HGse+D4OO3XLzrxqeuvt36du\nMMu//Bx6f0Z+y+dHBTOCXxEbYRicXXKWNrlsnorzxQKBgQDq+p00ra3vwhKnR1WS\nAmKOvzqq/cpwkC3tmK4eUPYpAMl3u9C7MQiHmYMk6XBnDWfSZFqQv1f7ztk5wPcH\n8BHUS7ZjTrAGHVATyD4zroJNzgPhN3cn231ma/z1MkhyQR2k7+1QuPx81kEHvnLM\n6Vr8OcQp/jdZx/xF2g+lctN1tQKBgQDK5JG2mmcqCzET3F7Pwkvz6NBVjheEWhAp\nAgxobYPrVL1aZCvnFbmuuGsLLI9cBlgVocpTB3S7ur7fnwn5noIhjNcQtuE9s2Gl\nm6bPzynsZIYWz8HQsIjAbfNWSnMD+rlpwcMCLvan3JY7LMCS+BBoGofcb6yx175s\npFzMWg8u5QKBgCGWoVIeYXacLz5qG/k7DguJmkFG9eEROv9zi7AZspY53pKW7kdT\nwxf8HTfxhne0mtqgLbHzKAh+kN6Ijsc7sdC+4dtgLBkzp3ascPfCQi4M/ND8tLOl\n1E8HsKj7/w8V777b7PhU+QJ/Pdx1hMN1t+PF/hxiklbrF0yE1ye3OjLhAoGBAIgq\n/uBen/5HpJh/veIRtIfuKGRDCOV6zH25MjqjxXWbWbngoNZmbkgk3TKSpWRNnbBm\n9TLkPiQAITpTso4lI5EAxRYipuiSC2bqH/o4Pxq4HIYSyTEWSbFcGYRAUxDIpMel\nkwtUGZZvJSRx1IzOj7ROmgAHsw9ojBS9+snrZ2VBAoGBALONAwRjcxYvxUOym1ji\nv2l4oe7ivWECu0of7tamX5w31Miip6nklADGo/UUOOVphs6StZyyaJNqNntdzVgC\nlk75An5KXC5v6Wq6bcBSLXSsRPYKyJX+v7y7GA6kmQJe+ZVGCWZXO2c4iJXHFiel\nCMmkHQwzyy9BE/z2Roh+UE1c\n-----END PRIVATE KEY-----\n",
        "client_email": "brainrot-bot@brainrot-app-491421.iam.gserviceaccount.com",
        "client_id": "115312792267646427801",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/brainrot-bot%40brainrot-app-491421.iam.gserviceaccount.com"
    }
    # On force le remplacement des \n pour que la clé soit valide
    info["private_key"] = info["private_key"].replace("\\n", "\n")
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    return gspread.authorize(creds)

# 3. LECTURE / ÉCRITURE
SHEET_ID = "1QpDkvd06ZmAWbVmFvpOdFO0_Tb3UvNMVnPlSy3hPzwQ"

try:
    client = get_gspread_client()
    sh = client.open_by_key(SHEET_ID)
    worksheet = sh.get_worksheet(0) # Prend la première feuille
    data = worksheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

# 4. INTERFACE
st.title("💎 BRAINROT COLLECTOR")

RARITIES = {"COMMON": "#2ECC71", "RARE": "#3498DB", "EPIC": "#9B59B6", "LEGENDAIRE": "#F1C40F", "MYTHIC": "#E74C3C", "BRAINROTGOD": "#FF69B4", "SECRET": "#FFFFFF"}

# Affichage des items
for index, row in df.iterrows():
    col1, col2 = st.columns([1, 9])
    with col1:
        check = "✅" if str(row['possede']) == "1" else "⬜"
        if st.button(check, key=f"btn_{index}"):
            new_val = 1 if str(row['possede']) == "0" else 0
            # Met à jour DIRECTEMENT dans Google Sheets (index+2 car Gspread commence à 1 et saute le header)
            # On cherche la colonne 'possede' (souvent la 5ème : E)
            worksheet.update_cell(index + 2, 5, new_val)
            st.rerun()
    with col2:
        color = RARITIES.get(row['rarete'], "#FFFFFF")
        st.markdown(f"<span style='color:{color}'>**{row['nom']}**</span>", unsafe_allow_html=True)
