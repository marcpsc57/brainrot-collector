import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Brainrot Collector v1", layout="wide")

# --- 2. DESIGN & COULEURS (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div.stButton > button:first-child {
        background-color: #00cc66;
        color: white;
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
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
    try:
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Erreur de clé JSON : {e}")

db = firestore.client()

# --- 4. TITRE ---
st.title("🧪 Brainrot Collector - 196 Items")
st.write("Gère ta collection en temps réel !")

# --- 5. SYSTÈME D'ONGLETS ---
categories = ["TOUT", "COMMON", "RARE", "EPIC", "LEGENDAIRE", "MYTHIC", "BRAINROTGOD", "SECRET"]
onglets = st.tabs(categories)

# --- 6. FONCTION D'AFFICHAGE ---
def afficher_la_liste(filtre):
    items_ref = db.collection("items")
    
    # Filtrer si on n'est pas sur l'onglet "TOUT"
    if filtre != "TOUT":
        docs = items_ref.where("rarete", "==", filtre).stream()
    else:
        docs = items_ref.stream()

    # Création d'une grille de 4 colonnes
    cols = st.columns(4)
    compteur = 0
    
    for doc in docs:
        item = doc.to_dict()
        with cols[compteur % 4]:
            # Design de la carte
            rare_style = item['rarete'].lower()
            st.markdown(f"### <span class='rare-{rare_style}'>{item['nom']}</span>", unsafe_allow_html=True)
            st.caption(f"Rareté : {item['rarete']}")
            st.metric(label="Possédé", value=item['possede'])
            
            # Bouton +1 avec clé UNIQUE pour éviter le bug
            if st.button(f"Ajouter +1", key=f"btn_{filtre}_{doc.id}"):
                nouvelle_valeur = item['possede'] + 1
                db.collection("items").document(doc.id).update({"possede": nouvelle_valeur})
                st.rerun()
            
            st.divider()
        compteur += 1

# --- 7. GÉNÉRATION DES ONGLETS ---
for i, cat in enumerate(categories):
    with onglets[i]:
        afficher_la_liste(cat)
