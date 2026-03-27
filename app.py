import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="MK-BRAINROT", layout="wide")

# --- 2. DESIGN & FLASH COLORS (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* TITRE RAINBOW FLASH */
    @keyframes rainbow {
        0% { color: #ff0000; text-shadow: 0 0 10px #ff0000; }
        20% { color: #ffff00; text-shadow: 0 0 10px #ffff00; }
        40% { color: #00ff00; text-shadow: 0 0 10px #00ff00; }
        60% { color: #00ffff; text-shadow: 0 0 10px #00ffff; }
        80% { color: #ff00ff; text-shadow: 0 0 10px #ff00ff; }
        100% { color: #ff0000; text-shadow: 0 0 10px #ff0000; }
    }
    .title-rainbow {
        font-size: 50px !important;
        font-weight: bold;
        animation: rainbow 3s linear infinite;
        text-align: center;
        display: block;
        margin-bottom: 20px;
    }

    /* Animation Flash / Pulsation */
    @keyframes flash-green { 0%, 100% { color: #00ff00; text-shadow: 0 0 5px #00ff00; } 50% { color: #008800; text-shadow: 0 0 20px #00ff00; } }
    @keyframes flash-blue { 0%, 100% { color: #0088ff; text-shadow: 0 0 5px #0088ff; } 50% { color: #0044bb; text-shadow: 0 0 20px #0088ff; } }
    @keyframes flash-purple { 0%, 100% { color: #cc00ff; text-shadow: 0 0 5px #cc00ff; } 50% { color: #770099; text-shadow: 0 0 20px #cc00ff; } }
    @keyframes flash-yellow { 0%, 100% { color: #ffff00; text-shadow: 0 0 5px #ffff00; } 50% { color: #aa8800; text-shadow: 0 0 25px #ffff00; } }
    @keyframes flash-red { 0%, 100% { color: #ff0000; text-shadow: 0 0 5px #ff0000; } 50% { color: #880000; text-shadow: 0 0 30px #ff0000; } }
    @keyframes flash-pink { 0%, 100% { color: #ff007f; text-shadow: 0 0 5px #ff007f; } 50% { color: #aa0055; text-shadow: 0 0 30px #ff007f; } }
    @keyframes flash-white { 0%, 100% { color: #ffffff; text-shadow: 0 0 5px #ffffff; } 50% { color: #888888; text-shadow: 0 0 20px #ffffff; } }

    .rare-common { animation: flash-green 2s infinite; font-weight: bold; }
    .rare-rare { animation: flash-blue 2s infinite; font-weight: bold; }
    .rare-epic { animation: flash-purple 1.8s infinite; font-weight: bold; }
    .rare-legendaire { animation: flash-yellow 1.5s infinite; font-weight: bold; }
    .rare-mythic { animation: flash-red 1.2s infinite; font-weight: bold; }
    .rare-brainrotgod { animation: flash-pink 1s infinite; font-weight: bold; }
    .rare-secret { animation: flash-white 1.5s infinite; font-weight: bold; } /* RALENTI ICI */

    .stButton > button { width: 100%; border-radius: 5px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONNEXION FIREBASE ---
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- 4. TITRE MK-BRAINROT ---
st.markdown('<h1 class="title-rainbow">MK-BRAINROT</h1>', unsafe_allow_html=True)
recherche = st.text_input("🔍 Trouve ton Brainrot...", "").lower()

# --- 5. SYSTÈME D'ONGLETS ---
categories = ["TOUT", "COMMON", "RARE", "EPIC", "LEGENDAIRE", "MYTHIC", "BRAINROTGOD", "SECRET"]
onglets = st.tabs(categories)

# --- 6. FONCTION D'AFFICHAGE ---
def afficher_la_liste(filtre_cat, texte_recherche):
    items_ref = db.collection("items")
    docs = items_ref.stream()
    items_filtres = []
    for doc in docs:
        d = doc.to_dict()
        d['id'] = doc.id
        if (filtre_cat == "TOUT" or d['rarete'] == filtre_cat) and (not texte_recherche or texte_recherche in d['nom'].lower()):
            items_filtres.append(d)

    if not items_filtres:
        st.info("Rien trouvé boss.")
        return

    cols = st.columns(4)
    for i, item in enumerate(items_filtres):
        with cols[i % 4]:
            rare_style = item['rarete'].lower()
            st.markdown(f"### <span class='rare-{rare_style}'>{item['nom']}</span>", unsafe_allow_html=True)
            st.metric(label=f"Rarete: {item['rarete']}", value=item['possede'])
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"➕", key=f"add_{filtre_cat}_{item['id']}"):
                    db.collection("items").document(item['id']).update({"possede": item['possede'] + 1})
                    st.rerun()
            with c2:
                if st.button(f"➖", key=f"sub_{filtre_cat}_{item['id']}"):
                    if item['possede'] > 0:
                        db.collection("items").document(item['id']).update({"possede": item['possede'] - 1})
                        st.rerun()
            st.divider()

for i, cat in enumerate(categories):
    with onglets[i]:
        afficher_la_liste(cat, recherche)

# --- 7. AJOUT DE NOUVEAUX ITEMS ---
st.write("---")
with st.expander("➕ AJOUTER UN NOUVEL ITEM"):
    new_nom = st.text_input("Nom de l'item")
    new_rarete = st.selectbox("Rareté", ["COMMON", "RARE", "EPIC", "LEGENDAIRE", "MYTHIC", "BRAINROTGOD", "SECRET"])
    if st.button("Enregistrer dans la base"):
        if new_nom:
            doc_id = new_nom.lower().replace(" ", "_").replace("'", "_")
            db.collection("items").document(doc_id).set({
                "nom": new_nom,
                "rarete": new_rarete,
                "possede": 0
            })
            st.success(f"{new_nom} a été ajouté !")
            st.rerun()
