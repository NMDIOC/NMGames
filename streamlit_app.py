import streamlit as st
import hashlib

# ------------------- Seguridad -------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Usuario y clave hasheada (la clave real es "admin", pero aquí solo se guarda el hash)
ADMIN_USER = "admin"
ADMIN_PASS_HASH = "8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918"

# Inicializar variables de sesión
if "reservas" not in st.session_state:
    st.session_state["reservas"] = []

if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False

# ------------------- UI -------------------
st.set_page_config(page_title="Reservas NM GAMES", page_icon="🎟️", layout="centered")

st.title("🎉 Reservas de Entradas - NM GAMES")
st.markdown("Bienvenido 👋 Reserva tus entradas para nuestros eventos de forma fácil y rápida.")

# ------------------- Formulario de reservas -------------------
st.header("📅 Haz tu Reserva")

with st.form("reserva_form", clear_on_submit=True):
    nombre = st.text_input("👤 Tu nombre")
    eventos = ["No hay eventos disponibles"]
    evento = st.selectbox("🎭 Selecciona el evento", eventos)
    cantidad = st.number_input("🎫 Número de entradas", min_value=1, max_value=10, value=1)
    confirmar = st.form_submit_button("✅ Confirmar Reserva")

    if confirmar:
        if nombre.strip() == "":
            st.warning("⚠️ Por favor ingresa tu nombre.")
        else:
            reserva = {"nombre": nombre, "evento": evento, "cantidad": cantidad}
            st.session_state["reservas"].append(reserva)
            st.success(f"🎉 ¡Reserva confirmada para **{nombre}**! ({cantidad} entrada(s) a {evento})")

st.markdown("---")

# ------------------- Panel Admin -------------------
st.sidebar.header("🔐 Panel de Administrador")

if not st.session_state["is_admin"]:
    usuario = st.sidebar.text_input("👤 Usuario")
    clave = st.sidebar.text_input("🔑 Contraseña", type="password")

    if st.sidebar.button("Iniciar sesión"):
        if usuario == ADMIN_USER and hash_password(clave) == ADMIN_PASS_HASH:
            st.session_state["is_admin"] = True
            st.sidebar.success("✅ Acceso concedido")
        else:
            st.sidebar.error("❌ Usuario o contraseña incorrectos")

else:
    st.sidebar.success("✅ Sesión iniciada como Admin")
    if st.sidebar.button("🚪 Cerrar sesión"):
        st.session_state["is_admin"] = False

# ------------------- Lista de reservas (solo admin) -------------------
if st.session_state["is_admin"]:
    st.header("📋 Lista de Reservas (Solo Admin)")

    if st.session_state["reservas"]:
        for i, r in enumerate(st.session_state["reservas"], start=1):
            st.write(f"**{i}. {r['nombre']}** → 🎫 {r['cantidad']} entrada(s) para *{r['evento']}*")
    else:
        st.info("ℹ️ Aún no hay reservas registradas.")
