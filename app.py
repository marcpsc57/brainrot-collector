import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- CONFIG PAGE ---
st.set_page_config(page_title="Ma Collection Légendaire", layout="wide")

# --- DESIGN (TES COULEURS) ---
st.markdown("""
    <style>
    .main { background-color: #1e1e1e; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #3e3e3e;
        color: white;
    }
    /* Couleurs par Rareté */
    .rare-common { color: #ffffff; }
    .rare-rare { color: #55ff55; font-weight: bold; }
    .rare-epic { color: #bb66ff; font-weight: bold; }
    .rare-legendaire { color: #ffcc00; font-weight: bold; text-shadow: 0px 0px 5px gold; }
    .rare-mythic { color: #ff4444; font-weight: bold; text-shadow: 0px 0px 8px red; }
    .rare-brainrotgod { color: #00ffff; font-weight: bold; }
    .rare-secret { color: #ff00ff; font-weight: bold; animation: blinker 1s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

# --- CONNEXION FIREBASE ---
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

st.title("🃏 Ma Collection de Cartes")

# --- SYSTÈME D'ONGLETS (CATÉGORIES) ---
categories = ["TOUT", "COMMON", "RARE", "EPIC", "LEGENDAIRE", "MYTHIC", "BRAINROTGOD", "SECRET"]
onglet_choisi = st.tabs(categories)

def afficher_items(filter_rarete=None):
    items_ref = db.collection("items")
    if filter_rarete and filter_rarete != "TOUT":
        docs = items_ref.where("rarete", "==", filter_rarete).stream()
    else:
        docs = items_ref.stream()

    cols = st.columns(4) # 4 items par ligne
    idx = 0
    for doc in docs:
        data = doc.to_dict()
        with cols[idx % 4]:
            st.markdown(f"### <span class='rare-{data['rarete'].lower()}'>{data['nom']}</span>", unsafe_allow_html=True)
            st.write(f"Rareté: {data['rarete']}")
            st.write(f"Possédé: **{data['possede']}**")
            if st.button(f"+1", key=doc.id):
                new_val = data['possede'] + 1
                db.collection("items").document(doc.id).update({"possede": new_val})
                st.rerun()
        idx += 1

# --- AFFICHAGE SELON L'ONGLET ---
for i, cat in enumerate(categories):
    with onglet_choisi[i]:
        afficher_items(cat)
