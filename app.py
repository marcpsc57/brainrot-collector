import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuration de la page (Titre et icône)
st.set_page_config(page_title="BRAINROT COLLECTOR", page_icon="💎", layout="wide")

# STYLE CSS POUR LE LOOK NÉON
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { border-radius: 10px; font-weight: bold; transition: 0.3s; }
    div[data-testid="stExpander"] { border: 1px solid #333; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Connexion au Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Tes 7 raretés avec leurs couleurs
RARITIES = {
    "COMMON": "#2ECC71",
    "RARE": "#3498DB",
    "EPIC": "#9B59B6",
    "LEGENDAIRE": "#F1C40F",
    "MYTHIC": "#E74C3C",
    "BRAINROTGOD": "#FF69B4",
    "SECRET": "#FFFFFF"
}

# Chargement des 196 items (ttl=0 pour que ce soit instantané)
df = conn.read(ttl="0")

# --- BARRE LATERALE (AJOUTER) ---
with st.sidebar:
    st.header("➕ AJOUTER")
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nom")
        r = st.selectbox("Rareté", list(RARITIES.keys()))
        b = st.text_input("Base")
        p = st.text_input("Page")
        if st.form_submit_button("SAUVEGARDER"):
            if n:
                new_row = pd.DataFrame([{"nom": n, "rarete": r, "base": b, "page": p, "possede": 0}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Ajouté au groupe !")
                st.rerun()

# --- HEADER PRINCIPAL ---
st.title("💎 BRAINROT GROUP COLLECTOR")
total = len(df)
possedes = df[df['possede'] == 1].shape[0]
st.write(f"### GLOBAL : {possedes} / {total} COLLECTÉS")

# RECHERCHE GLOBALE (Recherche partout comme tu l'as demandé)
search = st.text_input("🔍 Rechercher un nom, une base ou une page...", "").lower()

# ONGLETS PAR RARETE
tab_titles = []
for r in RARITIES.keys():
    count_t = len(df[df['rarete'] == r])
    count_p = len(df[(df['rarete'] == r) & (df['possede'] == 1)])
    tab_titles.append(f"{r} ({count_p}/{count_t})")

tabs = st.tabs(tab_titles)

for i, rarity in enumerate(RARITIES.keys()):
    with tabs[i]:
        # Filtrage intelligent
        if search:
            display_df = df[df.apply(lambda row: search in str(row).lower(), axis=1)]
        else:
            display_df = df[df['rarete'] == rarity]

        if display_df.empty:
            st.info("Aucun résultat.")
        
        for index, row in display_df.iterrows():
            # Style de la bordure selon la rareté
            color = RARITIES[row['rarete']]
            txt_color = "black" if row['rarete'] in ["SECRET", "LEGENDAIRE", "COMMON"] else "white"
            
            with st.container():
                col_chk, col_txt, col_del = st.columns([1, 6, 1])
                
                with col_chk:
                    # Case à cocher pour tout le groupe
                    is_owned = st.checkbox("✔", value=bool(row['possede']), key=f"check_{index}")
                    if is_owned != bool(row['possede']):
                        df.at[index, 'possede'] = int(is_owned)
                        conn.update(data=df)
                        st.rerun()
                
                with col_txt:
                    st.markdown(f"<h3 style='color:{color}; margin-bottom:0;'>{row['nom'].upper()}</h3>", unsafe_allow_html=True)
                    st.caption(f"BASE: {row['base']} | PAGE: {row['page']} | RARETÉ: {row['rarete']}")
                
                with col_del:
                    if st.button("🗑️", key=f"del_{index}"):
                        df = df.drop(index)
                        conn.update(data=df)
                        st.rerun()
                st.divider()