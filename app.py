import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="BRAINROT COLLECTOR", page_icon="💎", layout="wide")

# 2. STYLE NÉON PERSONNALISÉ (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    div[data-testid="stExpander"] { border: 1px solid #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ÉTABLIR LA CONNEXION
# Assure-toi que tes Secrets commencent par [connections.gsheets]
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. FONCTION POUR SAUVEGARDER (Avec gestion d'erreur)
def save_data(dataframe):
    try:
        conn.update(data=dataframe)
        st.success("✅ Synchronisé avec Google Sheets !")
        st.rerun()
    except Exception as e:
        st.error(f"Erreur de sauvegarde : {e}")
        st.info("Vérifie que l'e-mail du robot est bien 'Éditeur' sur ton Google Sheet.")

# 5. CHARGEMENT DES DONNÉES
try:
    df = conn.read(ttl="0")
except Exception as e:
    st.error(f"Impossible de lire le fichier : {e}")
    st.stop()

# 6. PARAMÈTRES DES RARETÉS
RARITIES = {
    "COMMON": "#2ECC71",
    "RARE": "#3498DB",
    "EPIC": "#9B59B6",
    "LEGENDAIRE": "#F1C40F",
    "MYTHIC": "#E74C3C",
    "BRAINROTGOD": "#FF69B4",
    "SECRET": "#FFFFFF"
}

# --- BARRE LATÉRALE ---
with st.sidebar:
    st.header("➕ AJOUTER")
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nom")
        r = st.selectbox("Rareté", list(RARITIES.keys()))
        b = st.text_input("Base")
        p = st.text_input("Page")
        if st.form_submit_button("AJOUTER AU GROUPE"):
            if n:
                new_row = pd.DataFrame([{"nom": n, "rarete": r, "base": b, "page": p, "possede": 0}])
                df = pd.concat([df, new_row], ignore_index=True)
                save_data(df)

# --- CORPS PRINCIPAL ---
st.title("💎 BRAINROT COLLECTOR")

# Stats rapides
total = len(df)
possedes = df[df['possede'] == 1].shape[0]
st.subheader(f"PROGRESSION : {possedes} / {total}")

# Recherche
search = st.text_input("🔍 Recherche rapide...", "").lower()

# Onglets
tabs = st.tabs([f"{r}" for r in RARITIES.keys()])

for i, rarity in enumerate(RARITIES.keys()):
    with tabs[i]:
        # Filtrage par rareté ou recherche
        if search:
            display_df = df[df.apply(lambda row: search in str(row).lower(), axis=1)]
        else:
            display_df = df[df['rarete'] == rarity]

        if display_df.empty:
            st.write("Rien ici...")
        
        for index, row in display_df.iterrows():
            color = RARITIES.get(row['rarete'], "#FFFFFF")
            
            with st.container():
                col_btn, col_txt, col_del = st.columns([1, 5, 1])
                
                with col_btn:
                    # Bouton d'état
                    label = "✅" if row['possede'] == 1 else "⬜"
                    if st.button(label, key=f"check_{index}"):
                        df.at[index, 'possede'] = 1 if row['possede'] == 0 else 0
                        save_data(df)
                
                with col_txt:
                    st.markdown(f"<span style='color:{color}; font-size:20px; font-weight:bold;'>{row['nom'].upper()}</span>", unsafe_allow_html=True)
                    st.caption(f"Base: {row['base']} | Page: {row['page']}")
                
                with col_del:
                    if st.button("🗑️", key=f"del_{index}"):
                        df = df.drop(index)
                        save_data(df)
                st.divider()
