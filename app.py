import streamlit as st

st.set_page_config(page_title="BRAINROT FIX", layout="wide")

# --- LE FORCEUR ---
# Si la variable n'est pas une LISTE (ou si elle n'existe pas), on l'écrase par du propre
if 'items' not in st.session_state or not isinstance(st.session_state['items'], list):
    st.session_state['items'] = [
        {"nom": "fishini bossini", "rarete": "COMMON", "base_page": "1", "possede": 1},
        {"nom": "pipi kiwi", "rarete": "COMMON", "base_page": "1", "possede": 0},
        {"nom": "trippi troppi", "rarete": "RARE", "base_page": "2", "possede": 1}
    ]

st.title("💎 BRAINROT COLLECTOR (Version Safe)")

# On crée une copie locale pour être sûr que Python travaille sur une liste
liste_propre = st.session_state['items']

# Affichage ultra-simple pour tester si ça débloque
for i, item in enumerate(liste_propre):
    st.write(f"N°{i} : **{item['nom']}** ({item['rarete']})")

if st.button("🔄 RÉINITIALISER TOUT (BOUTON DE SECOURS)"):
    st.session_state.clear()
    st.rerun()
