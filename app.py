import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import json

st.set_page_config(page_title="BRAINROT COLLECTOR LIVE", layout="wide")

# --- CONNEXION À GOOGLE ---
try:
    info = json.loads(st.secrets["firebase"]["service_account_json"])
    creds = service_account.Credentials.from_service_account_info(info)
    db = firestore.Client(credentials=creds, project=info['project_id'])
except Exception as e:
    st.error("❌ Erreur de connexion : Vérifie tes Secrets Streamlit !")
    st.stop()

# --- RÉCUPÉRER LES DONNÉES ---
def get_data():
    docs = db.collection("items").stream()
    return {doc.id: doc.to_dict() for doc in docs}

items_data = get_data()

st.title("💎 BRAINROT COLLECTOR (MODE LIVE)")

# --- LE BOUTON POUR TOUT ALLUMER ---
# Si la base est vide, on affiche ce gros bouton
if not items_data:
    st.warning("La base de données est vide chez Google !")
    if st.button("🚀 CLIQUE ICI POUR ENVOYER TES 150 ITEMS D'UN COUP"):
        # Liste simplifiée de tes items
        ma_liste = [
            {"nom": "fishini bossini", "rarete": "COMMON"},
            {"nom": "pipi kiwi", "rarete": "COMMON"},
            {"nom": "trippi troppi", "rarete": "RARE"},
            {"nom": "las agarrinis", "rarete": "SECRET"},
            # Tu pourras en rajouter d'autres ici plus tard
        ]
        
        with st.spinner("Envoi vers Firebase..."):
            for item in ma_liste:
                db.collection("items").document(item['nom']).set({
                    "nom": item['nom'],
                    "rarete": item['rarete'],
                    "possede": 0  # 0 = pas coché
                })
        st.success("🔥 C'est fait ! Rafraîchis la page.")
        st.rerun()

# --- L'INTERFACE POUR TOI ET TES CHUMS ---
if items_data:
    search = st.text_input("🔍 Rechercher un item...")
    
    for name in sorted(items_data.keys()):
        item = items_data[name]
        if search.lower() not in name.lower(): continue
            
        col_check, col_txt = st.columns([1, 8])
        with col_check:
            # Quand tu cliques, ça change chez Google pour TOUT LE MONDE
            val = item.get('possede', 0)
            label = "✅" if val == 1 else "⬜"
            if st.button(label, key=f"btn_{name}"):
                nouveau = 1 if val == 0 else 0
                db.collection("items").document(name).update({"possede": nouveau})
                st.rerun()
        with col_txt:
            st.write(f"**{name.upper()}** - {item.get('rarete')}")
