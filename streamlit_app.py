import streamlit as st
import hashlib
import json
import os

# ========= Configuración ========= #
DB_FILE = "reservas.json"
EVENTS_FILE = "eventos.json"

# Hashear contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Usuario y contraseña cifrada
USERS = {
    "admin": hash_password("admin")  # 👈 cifrada
}

# ========= Funciones de base de datos ========= #
def cargar_reservas():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def guardar_reservas(reservas):
    with open(DB_FILE, "w") as f:
        json.dump(reservas, f, indent=4)

def cargar_eventos():
    if os.path.exists(EVENTS_FILE):
        with open(EVENTS_FILE, "r") as f:
            return json.load(f)
    return ["Concierto de Rock", "Obra de Teatro", "Festival de Cine", "Conferencia", "Karaoke Cup"]

def guardar_eventos(eventos):
    with open(EVENTS_FILE, "w") as f:
        json.dump(eventos, f, indent=4)

# ========= Inicializar estado ========= #
if "reservas" not in st.session_state:
    st.session_state["reservas"] = cargar_reservas()
if "eventos" not in st.session_state:
    st.session_state["eventos"] = cargar_eventos()
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# ========= Login ========= #
def login():
    st.markdown("### 🔑 Iniciar Sesión (Admin)")
    username = st.text_input("👤 Usuario")
    password = st.text_input("🔒 Contraseña", type="password")
    if st.button("Iniciar Sesión", use_container_width=True):
        if username in USERS and USERS[username] == hash_password(password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"✅ Bienvenido, {username}")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

# ========= Logout ========= #
def logout():
    if st.button("🚪 Cerrar Sesión", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.rerun()

# ========= App ========= #
st.title("🎟️ Sistema de Reservas de Entradas")

# Formulario de reservas
with st.container():
    st.markdown("## 📌 Haz tu Reserva")
    nombre = st.text_input("👤 Nombre completo")
    evento = st.selectbox("🎭 Selecciona un evento", st.session_state["eventos"])
    cantidad = st.number_input("🎫 Cantidad de entradas", min_value=1, step=1)

    if st.button("✅ Reservar", use_container_width=True):
        if nombre.strip() == "":
            st.warning("⚠️ Ingresa tu nombre antes de reservar.")
        else:
            nueva_reserva = {"nombre": nombre, "evento": evento, "cantidad": cantidad}
            st.session_state["reservas"].append(nueva_reserva)
            guardar_reservas(st.session_state["reservas"])
            st.success("🎉 Reserva realizada con éxito")

st.divider()

# ========= Zona de admin ========= #
if st.session_state["logged_in"]:
    st.markdown("## 👑 Panel de Administrador")

    # Mostrar reservas
    if len(st.session_state["reservas"]) > 0:
        st.subheader("📋 Lista de Reservas")
        for i, r in enumerate(st.session_state["reservas"]):
            st.write(f"**{i+1}.** {r['nombre']} - {r['evento']} ({r['cantidad']} entradas)")
            if st.button(f"🗑️ Eliminar {i+1}", key=f"del_{i}"):
                st.session_state["reservas"].pop(i)
                guardar_reservas(st.session_state["reservas"])
                st.rerun()
    else:
        st.info("📭 No hay reservas registradas aún.")

    st.divider()

    # Gestión de eventos
    st.subheader("🎭 Gestión de Eventos")
    st.write("Eventos actuales:", ", ".join(st.session_state["eventos"]))

    nuevo_evento = st.text_input("➕ Añadir nuevo evento")
    if st.button("Añadir Evento"):
        if nuevo_evento.strip() != "":
            st.session_state["eventos"].append(nuevo_evento.strip())
            guardar_eventos(st.session_state["eventos"])
            st.success(f"Evento '{nuevo_evento}' añadido.")
            st.rerun()

    evento_borrar = st.selectbox("🗑️ Eliminar un evento", st.session_state["eventos"])
    if st.button("Eliminar Evento"):
        if evento_borrar in st.session_state["eventos"]:
            st.session_state["eventos"].remove(evento_borrar)
            guardar_eventos(st.session_state["eventos"])
            st.warning(f"Evento '{evento_borrar}' eliminado.")
            st.rerun()

    if st.button("🔄 Resetear eventos por defecto"):
        st.session_state["eventos"] = ["Concierto de Rock", "Obra de Teatro", "Festival de Cine", "Conferencia", "Karaoke Cup"]
        guardar_eventos(st.session_state["eventos"])
        st.success("Eventos reseteados.")
        st.rerun()

    st.divider()
    logout()

else:
    login()
