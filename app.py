import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Brainrot Collector - Custom Colors", layout="wide")

# --- 2. DESIGN & COULEURS (CSS PERSONNALISÉ) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    
    /* Style global des boutons */
    .stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    
    /* Boutons ➕ et ➖ */
    .btn-plus > div > button { 
        background-color: #00cc66 !important; /* Vert foncé pour le fond du bouton + */
        color: white !important; 
    }
    .btn-moins > div > button { 
        background-color: #ff4444 !important; /* Rouge foncé pour le fond du bouton - */
        color: white !important; 
    }

    /* Style pour le texte de rareté affiché sous le nom */
    .stCaption {
        font-size: 0.9rem;
        color: #888888;
    }

    /* --- NOUVELLES COULEURS DES NOMS (Comme demandé) --- */
    
    /* COMMON = Vert */
    .rare-common { color: #00ff00; font-weight: bold; }
    
    /* RARE = Bleu */
    .rare-rare { color: #0088ff; font-weight: bold; }
    
    /* EPIC = Mauve */
    .rare-epic { color: #cc00ff; font-weight: bold; }
    
    /* LEGENDARY = Jaune */
    .rare-legendaire { 
        color: #ffff00; 
        font-weight: bold; 
        text-shadow: 0px 0px 3px rgba(255, 255, 0, 0.5); /* Léger halo jaune */
    }
    
    /* MYTHIC = Rouge */
    .rare-mythic { 
        color: #ff0000; 
        font-weight: bold; 
        text-shadow: 0px 0px 5px rgba(255, 0, 0, 0.7); /* Halo rouge plus prononcé */
    }
    
    /* BRAINROTGOD = Rose */
    .rare-brainrotgod { 
        color: #ff007f; /* Rose vif */
        font-weight: bold; 
        text-shadow: 0px 0px 5px rgba(255, 0, 127, 0.7); /* Halo rose */
    }
    
    /* SECRET = Blanc */
    .rare-secret { 
        color: #ffffff; /* Blanc pur */
        font-weight: bold; 
        animation: blinker 2s linear infinite; /* Animation de clignotement lent */
        text-shadow: 0px 0px 10px rgba(255, 255, 255, 0.8); /* Halo blanc brillant */
    }
    
    /* Animation pour le Secret */
    @keyframes blinker { 50% { opacity: 0.2; } }
    
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONNEXION FIREBASE ---
if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

# --- 4. BARRE DE RECHERCHE ET TITRE ---
st.title("🧪 Brainrot Collector - Custom Colors")
st.write("Trouve tes items et gère tes doublons avec style !")
recherche = st.text_input("🔍 Recherche un item par son nom...", "").lower()

# --- 5. SYSTÈME D'ONGLETS ---
categories = ["TOUT", "COMMON", "RARE", "EPIC", "LEGENDAIRE", "MYTHIC", "BRAINROTGOD", "SECRET"]
onglets = st.tabs(categories)

# --- 6. FONCTION D'AFFICHAGE ---
def afficher_la_liste(filtre_cat, texte_recherche):
    items_ref = db.collection("items")
    docs = items_ref.stream() # On récupère tout
    
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
            
            # --- TITRE AVEC LA NOUVELLE COULEUR ---
            st.markdown(f"### <span class='rare-{rare_style}'>{item['nom']}</span>", unsafe_allow_html=True)
            
            # Autres infos
            st.caption(f"Rareté : {item['rarete']}")
            st.metric(label="Possédé", value=item['possede'])
            
            # Deux colonnes pour les boutons ➕ et ➖
            c1, c2 = st.columns(2)
            with c1:
                if st.button(f"➕", key=f"add_{filtre_cat}_{item['id']}", help="Ajouter 1"):
                    db.collection("items").document(item['id']).update({"possede": item['possede'] + 1})
                    st.rerun()
            with c2:
                # On s'assure de ne pas descendre en dessous de 0
                if st.button(f"➖", key=f"sub_{filtre_cat}_{item['id']}", help="Retirer 1"):
                    if item['possede'] > 0:
                        db.collection("items").document(item['id']).update({"possede": item['possede'] - 1})
                        st.rerun()
            st.divider()

# --- 7. GÉNÉRATION DES ONGLETS ---
for i, cat in enumerate(categories):
    with onglets[i]:
        afficher_la_liste(cat, recherche)
