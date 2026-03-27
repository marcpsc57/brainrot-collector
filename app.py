import streamlit as st
from donnees import ITEMS_DEFAUT

st.set_page_config(page_title="BRAINROT COLLECTOR", layout="wide")

# Initialisation de la liste dans la session
if 'items' not in st.session_state:
    st.session_state.items = ITEMS_DEFAUT

st.title("💎 BRAINROT COLLECTOR")
st.write(f"Total d'items : {len(st.session_state.items)}")

# Filtrage par rareté (Optionnel)
rarete_unique = sorted(list(set([i['rarete'] for i in st.session_state.items])))
choix = st.selectbox("Filtrer par rareté", ["TOUS"] + rarete_unique)

# Affichage
for index, item in enumerate(st.session_state.items):
    if choix != "TOUS" and item['rarete'] != choix:
        continue
        
    c1, c2, c3 = st.columns([1, 6, 3])
    with c1:
        is_owned = item['possede'] == 1
        if st.button("✅" if is_owned else "⬜", key=f"btn_{index}"):
            st.session_state.items[index]['possede'] = 0 if is_owned else 1
            st.rerun()
    with c2:
        st.write(f"**{item['nom']}**")
    with c3:
        st.caption(f"Rareté: {item['rarete']} | Page: {item['base_page']}")

# Bouton de sauvegarde (génère le code à copier dans donnees.py pour garder tes changements)
if st.sidebar.button("💾 Sauvegarder mes coches"):
    st.sidebar.code(f"ITEMS_DEFAUT = {st.session_state.items}")
