import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

st.set_page_config(page_title="BRAINROT LIVE", layout="wide")

# 1. CONNEXION SÉCURISÉE (Via les Secrets de Streamlit)
try:
    info = json.loads(st.secrets["firebase"]["service_account_json"])
    creds = service_account.Credentials.from_service_account_info(info)
    db = firestore.Client(credentials=creds, project=info['project_id'])
except Exception as e:
    st.error("❌ Erreur de connexion : Vérifie tes Secrets sur Streamlit Cloud !")
    st.stop()

# 2. FONCTION POUR RÉCUPÉRER LES ITEMS
def get_data():
    docs = db.collection("items").stream()
    return {doc.id: doc.to_dict() for doc in docs}

items_data = get_data()

st.title("🌐 BRAINROT COLLECTOR (MODE PARTAGÉ)")

# 3. INITIALISATION (Si la base est vide)
if not items_data:
    if st.button("🚀 CHARGER TOUS LES ITEMS DANS LA BASE"):
        # Voici ta liste complète
        full_list = [
            {"nom": "fishini bossini", "rarete": "COMMON", "possede": 0},
            {"nom": "pipi kiwi", "rarete": "COMMON", "possede": 0},
            {"nom": "trippi troppi", "rarete": "RARE", "possede": 0},
            {"nom": "cappuccino assassino", "rarete": "EPIC", "possede": 0},
            {"nom": "burbalona loliloli", "rarete": "LEGENDAIRE", "possede": 0},
            {"nom": "frigo camelo", "rarete": "MYTHIC", "possede": 0},
            {"nom": "cocofanto elephanto", "rarete": "BRAINROTGOD", "possede": 0},
            {"nom": "las agarrinis", "rarete": "SECRET", "possede": 0}
            # Ajoute les autres noms ici sur le même modèle !
        ]
        for item in full_list:
            db.collection("items").document(item['nom']).set(item)
        st.success("C'est fait ! Rafraîchis la page.")
        st.rerun()

# 4. RECHERCHE ET FILTRE
search = st.text_input("🔍 Rechercher un Brainrot...", "")

# 5. AFFICHAGE EN DIRECT
names = sorted(items_data.keys())
for name in names:
    item = items_data[name]
    if search.lower() not in name.lower():
        continue
        
    c1, c2 = st.columns([1, 8])
    with c1:
        # Quand tu cliques ICI, ça change pour TOUT LE MONDE
        val = item.get('possede', 0)
        label = "✅" if val == 1 else "⬜"
        if st.button(label, key=f"btn_{name}"):
            new_val = 0 if val == 1 else 1
            db.collection("items").document(name).update({"possede": new_val})
            st.rerun()
    with c2:
        st.write(f"**{name.upper()}** ({item.get('rarete')})")
