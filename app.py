import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="BRAINROT COLLECTOR", layout="wide")

# --- LA ZONE À MODIFIER ---
# Ouvre ton fichier .json avec le BLOC-NOTES (Notepad)
# Copie TOUT ce qui est entre les guillemets de "private_key"
# Ça doit commencer par -----BEGIN PRIVATE KEY-----
private_key_brute = """-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDTxx+vkltYKShm\nou26Gnfx6o68qjPyvBSpjbiuFxReayb4hxvnOv18R3JSPQuzhUxd9q985UgJ6jbU\nVGjjIWrut74nhXVw49q5OnPji58Ukage9GD/0l66IRGb56UdvRk1sOOYSeAr+ky1\nD6CSiNK3FlW4HgcJq0sud3wp8IN8I62wp0RFtxR53kLbzJzToRjhA+dqFVqxC5dD\n1QoAcC4P3kWVNjFpzbYPSUtYboBmoquhT1i6Ntglb9NeRMBH6zG3Y4cUUoAtytJv\n5omnw3v0Vyfsfic73m8Vgz0ujHCxuxvnl47gjOIA6Fp4ew7RR1zr+RI1yU9hnaJH\nNVoIJr5BAgMBAAECggEABP/IH6iBFkB4zbfGduxkHN5xoo0TLJrUEzQPR4cah0eO\nLBNMEp4TKNrAErunl0QRZfhE/c9k7ydQ8RvHKDxsK34uzjycOvnapQvMO536l31V\nkQR/C9mVvEempHiNg+QTEHrFsUe7fleaYF2h8lo/PMyZdv8OIWRCd4fLyIApqcBG\nsVylqgHWw4xa0Z4HJIrLXhFtVQpPJHz5IiquBbFUrmLE5A1NLDXAulwQdKqys+1d\nWQCossX6j9YPdTw+0WgDpKfXCd2OAv8Z9aoYG6iYOI0GI0cKhrXX7lxJEO7oRZGZ\nRVudCIV/45EXnk02iL0du1yc+ZEy3lxqcIG07TkZaQKBgQDw1XazQeobx3QF03lA\n+Jgyrb6z5mU7ae11F4xsU5zF+DKFfalrk1/wJ5DV6gPD3Yz4VlIkTcZMKxxw93iq\nsnxrrneoG8oEVWPBZadWJOveVnQOOvOEnn+j9/qcq7C+NwQ8GwY1dQJrTrdiMU5w\nvk/17pXHumsiylTZgn1g+rgNeQKBgQDhHT3XecWFglE+62Dya9n3iTw2iGpIAUKk\ndot6kRkmBHhRKYxV8hNnvm1QfBr7+aj8E5n2CwNkxQrkJhNnLF5j2eo0a2g3IuIQ\nj8jvv22yICjqDh+8KPcED5dFI3VH/CjaOK9RlDcZRC/EXshdktWtavIQC6fnpWR3\nOocng9AtCQKBgHCmeMpql5X82sFq5LnGTnLOIHjH2SxMZR0zMaTuC1Pyv7b/S4Md\nQW/1IeNdfftdI3Z58hw3IP054SjaKOA3cslvp1rD/N/ADVRGN1qtFINAjzKk0omD\nFhNdiCVGjfq7g0iWH3Zb0BDflhnhFF7aNk7EFd2BzmFMoRnI1trJC9SJAoGAfHCx\nst95tOfpCaMMIHZGM3QFeQ/H0K4BrPBrAgIbqMxnxlX1Yb1DxOGbhBZWxFuqck5T\nmZNU+OuDrcLujuYT95aKxRdqsK/zz7vsE7v6Y7ErbNcJ6/WpNvF3aZzERFq8KoWT\nRMFuA+WRkjfjAvccb5Ti4sPOuVrQQqhz9gADoCECgYEA6SGq8yFcj0D/a2WfLgRd\nwv3wVa6KyPwF/76ap2GabwNFp/7a6GHnVHk+quLtPpV6hi7Bfo7m7AINRCiTpQh5\nu4evFiO9JRM/wOR6oepL67H+jNDvq4Ea9g7t7QPyy/92aGaNYlPYZAqEazIejD6P\ngo1rYlMIKdhVHrntqYUuxKc=\n-----END PRIVATE KEY-----\n"""
# --------------------------

# Nettoyage automatique pour virer les espaces et les erreurs de format
CLEAN_KEY = private_key_brute.strip()

SERVICE_ACCOUNT_INFO = {
    "type": "service_account",
    "project_id": "brainrot-project-491423",
    "private_key_id": "dd28909d6aaaaf314cc05b83ce8856ff9c9fe03e",
    "private_key": CLEAN_KEY,
    "client_email": "brainrot-bot@brainrot-project-491423.iam.gserviceaccount.com",
    "client_id": "107186528494643778636",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/brainrot-bot%40brainrot-project-491423.iam.gserviceaccount.com"
}

@st.cache_resource
def connect_to_gsheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    # On force le remplacement des \n s'ils sont restés en texte
    info = SERVICE_ACCOUNT_INFO.copy()
    info["private_key"] = info["private_key"].replace("\\n", "\n")
    
    creds = Credentials.from_service_account_info(info, scopes=scope)
    return gspread.authorize(creds)

try:
    gc = connect_to_gsheet()
    sh = gc.open_by_key("1QpDkvd06ZmAWbVmFvpOdFO0_Tb3UvNMVnPlSy3hPzwQ")
    worksheet = sh.get_worksheet(0)
    df = pd.DataFrame(worksheet.get_all_records())
except Exception as e:
    st.error(f"Erreur de connexion : {e}")
    st.stop()

st.title("💎 BRAINROT COLLECTOR")

if not df.empty:
    for index, row in df.iterrows():
        c1, c2 = st.columns([1, 9])
        with c1:
            # On vérifie la colonne 'possede' (colonne E)
            is_owned = str(row.get('possede', 0)) == "1"
            if st.button("✅" if is_owned else "⬜", key=f"btn_{index}"):
                new_val = 1 if not is_owned else 0
                worksheet.update_cell(index + 2, 5, new_val)
                st.rerun()
        with c2:
            st.write(f"**{row.get('nom', 'Inconnu')}**")
