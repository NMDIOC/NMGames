import streamlit as st
import hashlib

# Función para cifrar contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Guardamos usuario y contraseña hasheada
ADMIN_USER = "admin"
ADMIN_PASS_HASH = hash_password("admin")  # La clave es "admin", pero guardada en hash

# Recuperar reservas de sesión
reservas = st.session_state.get("reservas", [])

st.title("🎟️ Reservas de Entradas - NM GAMES")

eventos = ["Concierto de Rock", "Obra de Teatro", "Karaoke Cup", "Festival de Helados"]

st.header("Haz tu Reserva")

# Formulario de reserva
with st.form("reserva_form"):
    nombre = st.text_input("👤 Tu nombre")
    evento = st.selectbox("📅 Selecciona el evento", eventos)
    cantidad = st.number_input("🎫 Número de entradas", min_value=1, max_value=10, value=1)
    confirmar = st.form_submit_button("Reservar")

    if confirmar:
        if nombre.strip() == "":
            st.warning("⚠️ Por favor ingresa tu nombre.")
        else:
            reserva = {"nombre": nombre, "evento": evento, "cantidad": cantidad}
            reservas.append(reserva)
            st.session_state["reservas"] = reservas
            st.success(f"✅ ¡Reserva confirmada para {nombre}! ({cantidad} entrada(s) a {evento})")

# Sección de administrador
st.sidebar.header("🔐 Panel de Administrador")
usuario = st.sidebar.text_input("Usuario")
clave = st.sidebar.text_input("Contraseña", type="password")

if st.sidebar.button("Iniciar sesión"):
    if usuario == ADMIN_USER and hash_password(clave) == ADMIN_PASS_HASH:
        st.session_state["is_admin"] = True
        st.sidebar.success("✅ Acceso concedido")
    else:
        st.sidebar.error("❌ Usuario o contraseña incorrectos")

# Mostrar reservas solo al admin
if st.session_state.get("is_admin", False):
    st.header("📋 Lista de Reservas (Solo Admin)")
    if reservas:
        for i, r in enumerate(reservas, start=1):
            st.write(f"**{i}. {r['nombre']}** → {r['cantidad']} entrada(s) para *{r['evento']}*")
    else:
        st.info("Aún no hay reservas registradas.")
