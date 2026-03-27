import streamlit as st

# Configuration de la page
st.set_page_config(page_title="BRAINROT COLLECTOR", layout="wide")

# --- 1. LA LISTE SOURCE (TES DONNÉES) ---
# On définit cette liste en DUR pour que l'app ait toujours une base saine
DONNEES_INITIALES = [
    {"nom": "fishini bossini", "rarete": "COMMON", "base_page": "1", "possede": 1},
    {"nom": "pipi kiwi", "rarete": "COMMON", "base_page": "1", "possede": 0},
    {"nom": "trippi troppi", "rarete": "RARE", "base_page": "2", "possede": 1},
    {"nom": "cappuccino assassino", "rarete": "EPIC", "base_page": "3", "possede": 1},
    {"nom": "burbalona loliloli", "rarete": "LEGENDAIRE", "base_page": "4", "possede": 1},
    {"nom": "frigo camelo", "rarete": "MYTHIC", "base_page": "5", "possede": 1},
    {"nom": "cocofanto elephanto", "rarete": "BRAINROTGOD", "base_page": "6", "possede": 0},
    {"nom": "las agarrinis", "rarete": "SECRET", "base_page": "7", "possede": 1},
    # ... (Tu pourras rajouter les autres plus tard, testons d'abord avec ceux-là)
]

# --- 2. INITIALISATION ULTRA-SÉCURISÉE ---
# Si 'items' n'existe pas OU si ce n'est pas une liste, on RAZ (Remise à Zéro)
if 'items' not in st.session_state or not isinstance(st.session_state.items, list):
    st.session_state.items = DONNEES_INITIALES

# --- 3. INTERFACE ---
st.title("💎 BRAINROT COLLECTOR")

# On utilise une variable locale pour être sûr de ne pas travailler sur du "vide"
items_actifs = st.session_state.items

# Barre de recherche et Filtre
search = st.text_input("Rechercher un item...", "")

# Récupération sécurisée des raretés pour le menu déroulant
toutes_raretes = sorted(list(set([i.get('rarete', 'Inconnue') for i in items_actifs])))
filtre = st.selectbox("Filtrer par rareté", ["TOUS"] + toutes_raretes)

st.write("---")

# --- 4. AFFICHAGE ---
for index, item in enumerate(items_actifs):
    nom = item.get('nom', 'Sans nom')
    rarete = item.get('rarete', 'Inconnue')
    
    # Logique de filtrage
    if search.lower() not in nom.lower():
        continue
    if filtre != "TOUS" and rarete != filtre:
        continue

    # Colonnes d'affichage
    c1, c2, c3 = st.columns([1, 4, 2])
    with c1:
        # Système de check
        label = "✅" if item.get('possede') == 1 else "⬜"
        if st.button(label, key=f"btn_{index}"):
            # On inverse la possession
            st.session_state.items[index]['possede'] = 0 if item.get('possede') == 1 else 1
            st.rerun()
    with c2:
        st.subheader(nom)
    with c3:
        st.info(f"{rarete} (Page {item.get('base_page', '?')})")

# Sidebar pour sauvegarder manuellement
st.sidebar.header("💾 Sauvegarde")
if st.sidebar.button("Afficher le code de sauvegarde"):
    st.sidebar.code(f"st.session_state.items = {st.session_state.items}")
