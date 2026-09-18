import requests
import streamlit as st

st.set_page_config(
    page_title="SPORTZONE - Performance Store",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS Avanzados: Se incluye estilizado oscuro completo para el sidebar
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,400;0,600;0,800;0,900;1,800&display=swap');

    /* Fondo general */
    html, body, [class*="css"] {
        font-family: 'Montserrat', sans-serif;
        background-color: #0B0F17 !important;
        color: #F3F4F6;
    }

    /* Estilo del Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0F172A !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] p {
        color: #F3F4F6 !important;
    }

    /* Campo de texto (Buscador) */
    section[data-testid="stSidebar"] .stTextInput input {
        background-color: #1E293B !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }

    /* FIX: Desplegable de Categorías (Selectbox) totalmente legible */
    div[data-baseweb="select"] {
        background-color: #1E293B !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
    }

    div[data-baseweb="select"] * {
        background-color: transparent !important;
        color: #FFFFFF !important;
    }

    /* Fondo oscuro para las opciones al desplegar la lista */
    ul[role="listbox"] {
        background-color: #1E293B !important;
    }

    ul[role="listbox"] li {
        color: #FFFFFF !important;
    }

    ul[role="listbox"] li:hover {
        background-color: #334155 !important;
    }

    /* Banner Hero */
    .sport-hero {
        background: linear-gradient(135deg, #111827 0%, #0F172A 50%, #020617 100%);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 0 35px rgba(16, 185, 129, 0.15);
    }

    .sport-title {
        font-size: 42px;
        font-weight: 900;
        font-style: italic;
        letter-spacing: -1px;
        background: linear-gradient(90deg, #10B981 0%, #06B6D4 50%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .sport-subtitle {
        color: #9CA3AF;
        font-size: 14px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* Tarjetas de Producto */
    .sport-card {
        background: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 22px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        height: 450px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }

    .sport-card:hover {
        transform: translateY(-8px);
        border-color: #10B981;
        box-shadow: 0 15px 35px -5px rgba(16, 185, 129, 0.3);
    }

    .sport-img-box {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        overflow: hidden;
    }

    .sport-img-box img {
        max-height: 100%;
        max-width: 100%;
        object-fit: contain;
    }

    .sport-badge {
        background: rgba(16, 185, 129, 0.15);
        color: #34D399 !important;
        border: 1px solid rgba(16, 185, 129, 0.4);
        border-radius: 30px;
        padding: 4px 12px;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        display: inline-block;
        margin-top: 10px;
    }

    .sport-name {
        font-size: 15px;
        font-weight: 700;
        color: #F9FAFB !important;
        margin-top: 10px;
        margin-bottom: 6px;
        height: 42px;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }

    .sport-price {
        font-size: 26px;
        font-weight: 900;
        color: #10B981 !important;
        margin-top: 4px;
    }

    .page-badge {
        background: rgba(31, 41, 55, 0.8);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 10px 20px;
        text-align: center;
        font-weight: 700;
        color: #E5E7EB;
    }
</style>
""", unsafe_allow_html=True)

# 1. Estados iniciales
if "cart" not in st.session_state:
    st.session_state.cart = []

if "page" not in st.session_state:
    st.session_state.page = 1

ITEMS_PER_PAGE = 6

# Diccionario de traducción básico para optimizar la búsqueda en español
TRADUCCIONES = {
    "pollo": "chicken",
    "carne": "meat",
    "aceite": "oil",
    "agua": "water",
    "leche": "milk",
    "pan": "bread",
    "manzana": "apple",
    "arroz": "rice",
    "camiseta": "shirt",
    "zapatos": "shoes",
    "tenis": "shoes"
}

# 2. Consumo de la API (DummyJSON)
@st.cache_data
def fetch_all_products():
    url = "https://dummyjson.com/products?limit=100"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("products", [])
    return []

@st.cache_data
def fetch_categories():
    url = "https://dummyjson.com/products/categories"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            return [cat.get("slug") for cat in data]
        return data
    return []

all_products = fetch_all_products()
categories = fetch_categories()

# 3. Sidebar (Panel Lateral)
st.sidebar.title("⚡ NAVEGACIÓN SPORTZONE")
st.sidebar.markdown("---")

search_query = st.sidebar.text_input("🔍 Buscar equipamiento...", value="")
selected_category = st.sidebar.selectbox("📂 Categoría:", ["Todas"] + list(categories))

max_price_val = float(max([p.get('price', 100) for p in all_products])) if all_products else 1000.0
price_limit = st.sidebar.slider("💰 Precio Máximo ($):", 0.0, max_price_val, max_price_val)

st.sidebar.markdown("---")

# Carrito en Sidebar
st.sidebar.header(f"🛒 Carrito ({len(st.session_state.cart)})")

if st.session_state.cart:
    total_price = 0
    for idx, item in enumerate(st.session_state.cart):
        col_i1, col_i2 = st.sidebar.columns([3, 1])
        with col_i1:
            st.caption(f"**{item['title']}**\n${item['price']}")
            total_price += item['price']
        with col_i2:
            if st.button("🗑️", key=f"del_{idx}"):
                st.session_state.cart.pop(idx)
                st.rerun()
    
    st.sidebar.markdown(f"### **Total: ${total_price:,.2f}**")
    if st.sidebar.button("⚡ PAGAR AHORA", type="primary", use_container_width=True):
        st.sidebar.success("¡Pedido procesado con éxito!")
        st.session_state.cart = []
else:
    st.sidebar.info("Tu carrito está vacío.")

# 4. Motor de Búsqueda Mejorado (Multilingüe y Multicampo)
filtered_products = all_products

if selected_category != "Todas":
    filtered_products = [p for p in filtered_products if p.get("category") == selected_category]

if search_query:
    query_clean = search_query.strip().lower()
    # Mapea palabras en español a inglés si existen en el diccionario
    query_translated = TRADUCCIONES.get(query_clean, query_clean)
    
    def coincide_producto(p):
        titulo = p.get("title", "").lower()
        descripcion = p.get("description", "").lower()
        categoria = p.get("category", "").lower()
        
        # Evalúa coincidencia tanto de la palabra original como la traducida
        return (query_clean in titulo or query_clean in descripcion or query_clean in categoria or
                query_translated in titulo or query_translated in descripcion or query_translated in categoria)

    filtered_products = [p for p in filtered_products if coincide_producto(p)]

filtered_products = [p for p in filtered_products if p.get("price", 0) <= price_limit]

# 5. Header Banner
st.markdown("""
    <div class="sport-hero">
        <div class="sport-title">⚡ SPORTZONE PERFORMANCE</div>
        <div class="sport-subtitle">Catálogo Oficial de Productos y Equipamiento</div>
    </div>
""", unsafe_allow_html=True)

# 6. Paginación
total_items = len(filtered_products)
total_pages = max(1, (total_items // ITEMS_PER_PAGE) + (1 if total_items % ITEMS_PER_PAGE > 0 else 0))

if st.session_state.page > total_pages:
    st.session_state.page = 1

col_p1, col_p2, col_p3 = st.columns([1, 2, 1])

def prev_page():
    if st.session_state.page > 1:
        st.session_state.page -= 1

def next_page():
    if st.session_state.page < total_pages:
        st.session_state.page += 1

with col_p1:
    st.button("⬅️ Anterior", on_click=prev_page, disabled=(st.session_state.page == 1), use_container_width=True)

with col_p2:
    st.markdown(f'<div class="page-badge">PÁGINA <b>{st.session_state.page}</b> DE <b>{total_pages}</b> ({total_items} ITEMS)</div>', unsafe_allow_html=True)

with col_p3:
    st.button("Siguiente ➡️", on_click=next_page, disabled=(st.session_state.page >= total_pages), use_container_width=True)

st.write("")

# 7. Cuadrícula de Productos (3 Columnas)
start_idx = (st.session_state.page - 1) * ITEMS_PER_PAGE
end_idx = start_idx + ITEMS_PER_PAGE
current_products = filtered_products[start_idx:end_idx]

if current_products:
    cols = st.columns(3)
    for i, prod in enumerate(current_products):
        col = cols[i % 3]
        with col:
            st.markdown(f"""
                <div class="sport-card">
                    <div class="sport-img-box">
                        <img src="{prod.get('thumbnail')}" alt="{prod.get('title')}">
                    </div>
                    <div>
                        <span class="sport-badge">{prod.get('category')}</span>
                        <div class="sport-name">{prod.get('title')}</div>
                        <div style="color: #FBBF24; font-weight:700;">★ {prod.get('rating', 'N/A')} / 5.0</div>
                        <div class="sport-price">${prod.get('price', 0.0):,.2f}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            btn_c1, btn_c2 = st.columns(2)
            with btn_c1:
                if st.button("🛒 Agregar", key=f"add_{prod['id']}", use_container_width=True):
                    st.session_state.cart.append(prod)
                    st.toast(f"¡{prod['title']} al carrito!", icon="⚡")
                    st.rerun()
            with btn_c2:
                with st.expander("ℹ️ Specs"):
                    st.write(f"**Stock:** {prod.get('stock')} disps.")
                    st.write(f"**Descuento:** {prod.get('discountPercentage')}%")
                    st.write(prod.get('description'))
else:
    st.warning("⚠️ No hay productos disponibles con esos filtros.")