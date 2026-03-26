import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="BRAINROT COLLECTOR", page_icon="💎", layout="wide")

# 2. STYLE NÉON (CSS)
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 20px;
        border-radius: 10px;
        background-color: #1a1c24;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. CONNEXION AU GOOGLE SHEET (Utilise tes Secrets)
conn = st.connection("gsheets", type=GSheetsConnection)

# 4. CHARGEMENT DES DONNÉES
try:
    # On force la lecture en temps réel (ttl=0)
    df = conn.read(ttl="0")
except Exception as e:
    st.error(f"Erreur de connexion au Google Sheet : {e}")
    st.stop()

# 5. COULEURS DES RARETÉS
RARITIES = {
    "COMMON": "#2ECC71",
    "RARE": "#3498DB",
    "EPIC": "#9B59B6",
    "LEGENDAIRE": "#F1C40F",
    "MYTHIC": "#E74C3C",
    "BRAINROTGOD": "#FF69B4",
    "SECRET": "#FFFFFF"
}

# --- BARRE LATÉRALE : AJOUTER ---
with st.sidebar:
    st.header("➕ AJOUTER")
    with st.form("add_form", clear_on_submit=True):
        n = st.text_input("Nom du Brainrot")
        r = st.selectbox("Rareté", list(RARITIES.keys()))
        b = st.text_input("Base")
        p = st.text_input("Page")
        if st.form_submit_button("SAUVEGARDER"):
            if n:
                new_data = pd.DataFrame([{"nom": n, "rarete": r, "base": b, "page": p, "possede": 0}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                conn.update(data=updated_df)
                st.success("Ajouté avec succès !")
                st.rerun()

# --- HEADER ET STATS ---
st.title("💎 BRAINROT GROUP COLLECTOR")
total = len(df)
possedes = df[df['possede'] == 1].shape[0]
st.subheader(f"GLOBAL : {possedes} / {total} COLLECTÉS")

# RECHERCHE
search = st.text_input("🔍 Rechercher un nom, une base ou une page...", "").lower()

# --- ONGLETS PAR RARETÉ ---
tab_titles = []
for r in RARITIES.keys():
    count_t = len(df[df['rarete'] == r])
    count_p = len(df[(df['rarete'] == r) & (df['possede'] == 1)])
    tab_titles.append(f"{r} ({count_p}/{count_t})")

tabs = st.tabs(tab_titles)

for i, rarity in enumerate(RARITIES.keys()):
    with tabs[i]:
        # Filtrage
        if search:
            display_df = df[df.apply(lambda row: search in str(row).lower(), axis=1)]
        else:
            display_df = df[df['rarete'] == rarity]

        if display_df.empty:
            st.info("Aucun item ici pour le moment.")
        
        for index, row in display_df.iterrows():
            color = RARITIES.get(row['rarete'], "#FFFFFF")
            
            with st.container():
                c1, c2, c3 = st.columns([1, 6, 1])
                
                with c1:
                    # Bouton pour cocher
                    label = "✅" if row['possede'] == 1 else "⬜"
                    if st.button(label, key=f"btn_{index}"):
                        # On inverse la valeur (0 devient 1, 1 devient 0)
                        df.at[index, 'possede'] = 1 if row['possede'] == 0 else 0
                        conn.update(data=df)
                        st.rerun()
                
                with c2:
                    st.markdown(f"<h3 style='color:{color}; margin:0;'>{row['nom'].upper()}</h3>", unsafe_allow_html=True)
                    st.caption(f"BASE: {row['base']} | PAGE: {row['page']}")
                
                with c3:
                    if st.button("🗑️", key=f"del_{index}"):
                        df = df.drop(index)
                        conn.update(data=df)
                        st.rerun()
                st.divider()
