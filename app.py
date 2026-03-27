import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Brainrot Collector Pro", layout="wide")

# --- 2. DESIGN & COULEURS (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    /* Style des boutons + et - */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    .btn-plus > div > button { background-color: #00cc66 !important; color: white !important; }
    .btn-moins > div > button { background-color: #ff4444 !important; color: white !important; }
    
    /* Styles pour les raretés */
    .rare-common { color: #ffffff; }
    .rare-rare { color: #3399ff; font-weight: bold; }
    .rare-epic { color: #bb66ff; font-weight: bold; }
    .rare-legendaire { color: #ffcc00; font-weight: bold; text-shadow: 0px 0px 5px gold; }
    .rare-mythic { color: #ff4444; font-weight: bold; text-shadow: 0px 0px 8px red; }
    .rare-brainrotgod { color: #00ffff; font-weight: bold; border: 1px solid #00ffff; padding: 2px; }
    .rare-secret { color: #ff00ff; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0.3; } }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONNEXION FIREBASE ---
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- 4. BARRE DE RECHERCHE ---
st.title("🧪 Brainrot Collector - 196 Items")
recherche = st.text_input("🔍 Recherche un item par son nom...", "").lower()

# --- 5. SYSTÈME D'ONGLETS ---
categories = ["TOUT", "COMMON", "RARE", "EPIC", "LEGENDAIRE", "MYTHIC", "BRAINROTGOD", "SECRET"]
onglets = st.tabs(categories)

# --- 6. FONCTION D'AFFICHAGE ---
def afficher_la_liste(filtre_cat, texte_recherche):
    items_ref = db.collection("items")
    
    # On récupère tout et on filtrera en Python pour plus de flexibilité
    docs = items_ref.stream()
    
    # Filtrage local
    items_filtres = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        # Filtre Catégorie
        if filtre_cat != "TOUT" and d['rarete'] != filtre_cat:
            continue
        # Filtre Recherche
        if texte_recherche and texte_recherche not in d['nom'].lower():
            continue
        items_filtres.append(d)

    if not items_filtres:
        st.info("Aucun item trouvé.")
        return

    # Grille de 4 colonnes
    cols = st.columns(4)
    for i, item in enumerate(items_filtres):
        with cols[i % 4]:
            rare_style = item['rarete'].lower()
            st.markdown(f"### <span class='rare-{rare_style}'>{item['nom']}</span>", unsafe_allow_html=True)
            st.caption(f"Rareté : {item['rarete']}")
            st.metric(label="Possédé", value=item['possede'])
            
            # Deux colonnes pour les boutons + et -
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"➕", key=f"add_{filtre_cat}_{item['id']}", help="Ajouter 1"):
                    db.collection("items").document(item['id']).update({"possede": item['possede'] + 1})
                    st.rerun()
            with c2:
                # On ne descend pas en dessous de 0
                if st.button(f"➖", key=f"sub_{filtre_cat}_{item['id']}", help="Retirer 1"):
                    if item['possede'] > 0:
                        db.collection("items").document(item['id']).update({"possede": item['possede'] - 1})
                        st.rerun()
            st.divider()

# --- 7. GÉNÉRATION DES ONGLETS ---
for i, cat in enumerate(categories):
    with onglets[i]:
        afficher_la_liste(cat, recherche)
