import streamlit as st
import random
import requests

# 1. Configuración de pantalla ancha
st.set_page_config(page_title="Scrydex TCG Engine", page_icon="🃏", layout="wide")

# 2. Estilos CSS (Carta en 3D con efecto hover y modo oscuro)
st.markdown("""
    <style>
    .stApp { background-color: #0b0c10; color: #e0e0e0; }
    
    .tcg-card-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }
    
    .tcg-card-img {
        width: 100%;
        max-width: 340px;
        border-radius: 16px;
        box-shadow: 0px 8px 25px rgba(102, 252, 241, 0.3);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .tcg-card-img:hover {
        transform: scale(1.05);
        box-shadow: 0px 12px 35px rgba(102, 252, 241, 0.6);
    }

    .console-box {
        background-color: #12131a;
        border-left: 4px solid #66fcf1;
        padding: 10px;
        font-family: monospace;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Manejo de Estado en Streamlit (para que el aleatorio cambie SIEMPRE)
if "current_pokemon" not in st.session_state:
    st.session_state.current_pokemon = "gengar"

# Funciones de consulta a APIs con respaldo
def get_pokemon_data(query):
    # Consulta a PokéAPI para datos exactos de stats/movimientos
    try:
        res = requests.get(f"https://pokeapi.co/api/v2/pokemon/{query}")
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

def get_tcg_image(name):
    # Obtiene la carta coleccionable oficial de la TCG API
    try:
        res = requests.get(f"https://api.pokemontcg.io/v2/cards?q=name:\"{name}\"", headers={"User-Agent": "Mozilla/5.0"}, timeout=4)
        if res.status_code == 200:
            data = res.json()
            if data['data']:
                return data['data'][0]['images']['large']
    except:
        pass
    return None

# Encabezado
st.title("⚡ Scrydex Digital - Visor TCG & API")

# Buscador y Botón Aleatorio
col_input, col_rand = st.columns([2, 1])

with col_input:
    pokemon_search = st.text_input("Ingresa el nombre o ID:", value=st.session_state.current_pokemon)
    if st.button("Buscar Carta 🔍", use_container_width=True):
        if pokemon_search:
            st.session_state.current_pokemon = pokemon_search.lower().strip()

with col_rand:
    st.write("¿Probar suerte?")
    if st.button("Generar Pokémon Aleatorio 🎲", use_container_width=True):
        # Genera ID aleatorio de la Gen 1 a la 9 (1 a 1025)
        st.session_state.current_pokemon = str(random.randint(1, 1025))
        st.rerun()

# Cargar Datos según la sesión actual
poke_data = get_pokemon_data(st.session_state.current_pokemon)

if poke_data:
    st.divider()
    col_card, col_details = st.columns([1.1, 1.9])

    # INTENTO DE CARGAR CARTA TCG (Si falla, usa la ilustración oficial)
    tcg_img = get_tcg_image(poke_data['name'])
    final_img = tcg_img if tcg_img else poke_data['sprites']['other']['official-artwork']['front_default']

    # COLUMNA IZQUIERDA: Carta
    with col_card:
        st.header(f"#{poke_data['id']} - {poke_data['name'].upper()}")
        st.markdown(f"""
            <div class="tcg-card-container">
                <img src="{final_img}" class="tcg-card-img" alt="Carta">
            </div>
        """, unsafe_allow_html=True)
        
        if 'cries' in poke_data and 'latest' in poke_data['cries']:
            st.audio(poke_data['cries']['latest'], format="audio/ogg")

    # COLUMNA DERECHA: Consola y Estadísticas
    with col_details:
        tab1, tab2, tab3 = st.tabs(["💻 API Response (JSON)", "📊 Estadísticas Base", "🥋 Movimientos"])

        with tab1:
            st.markdown(f"<div class='console-box'>-> GET /api/v2/pokemon/{poke_data['name']}</div>", unsafe_allow_html=True)
            st.json({
                "id": poke_data["id"],
                "name": poke_data["name"],
                "types": [t['type']['name'] for t in poke_data["types"]],
                "height_m": poke_data["height"] / 10,
                "weight_kg": poke_data["weight"] / 10,
                "stats": {s['stat']['name']: s['base_stat'] for s in poke_data["stats"]}
            })

        with tab2:
            st.subheader("Nivel de Poder")
            MAX_STAT = 255
            for stat in poke_data['stats']:
                val = stat['base_stat']
                st.markdown(f"**{stat['stat']['name'].upper()}:** `{val}`")
                st.progress(min(val / MAX_STAT, 1.0))

        with tab3:
            st.subheader("Movimientos Principales")
            movs = [m['move']['name'].capitalize() for m in poke_data['moves'][:12]]
            st.write(", ".join(movs))

else:
    st.error("❌ No se encontró el Pokémon. Intenta con otro nombre o ID numérico.")