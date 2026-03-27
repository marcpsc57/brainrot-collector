import streamlit as st

st.set_page_config(page_title="TEST REBOOT", layout="wide")

# On crée une liste de test toute simple
if 'items' not in st.session_state:
    st.session_state.items = [
        {"nom": "TEST 1", "rarete": "COMMON", "base_page": "1", "possede": 0},
        {"nom": "TEST 2", "rarete": "RARE", "base_page": "1", "possede": 1}
    ]

st.title("🚀 TEST DE CONNEXION")

if st.button("NETTOYER LA MÉMOIRE ET RELANCER"):
    st.session_state.clear()
    st.rerun()

# Affichage simple
for i, item in enumerate(st.session_state.items):
    st.write(f"Item: {item['nom']} | Rareté: {item['rarete']}")
