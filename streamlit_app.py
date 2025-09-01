import streamlit as st
import hashlib
import json
import os

# ========= Configuración ========= #
DB_FILE = "reservas.json"

# Hashear contraseña
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Usuario y contraseña cifrada
USERS = {
    "admin": hash_password("admin")  # 👈 nadie verá la clave real
}

# ========= Funciones de reservas ========= #
def cargar_reservas():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def guardar_reservas(reservas):
    with open(DB_FILE, "w") as f:
        json.dump(reservas, f, indent=4)

# ========= Inicializar estado ========= #
if "reservas" not in st.session_state:
    st.session_state["reservas"] = cargar_reservas()
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = None

# ========= Login ========= #
def login():
    st.subheader("🔑 Iniciar Sesión (Admin)")
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")
    if st.button("Iniciar Sesión"):
        if username in USERS and USERS[username] == hash_password(password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Bienvenido, {username}")
        else:
            st.error("❌ Usuario o contraseña incorrectos")

# ========= Logout ========= #
def logout():
    if st.button("Cerrar Sesión"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = None
        st.rerun()

# ========= App ========= #
st.title("🎟️ Sistema de Reservas de Entradas")

# Formulario de reserva
st.subheader("📌 Haz tu Reserva")
nombre = st.text_input("Nombre")
evento = st.text_input("Evento")
cantidad = st.number_input("Cantidad de entradas", min_value=1, step=1)

if st.button("Reservar"):
    nueva_reserva = {"nombre": nombre, "evento": evento, "cantidad": cantidad}
    st.session_state["reservas"].append(nueva_reserva)
    guardar_reservas(st.session_state["reservas"])  # Guardar en JSON
    st.success("✅ Reserva realizada con éxito")

# Zona de admin
st.divider()
if st.session_state["logged_in"]:
    st.subheader("👑 Panel de Administrador")
    st.write("📋 Lista de Reservas")
    st.table(st.session_state["reservas"])
    logout()
else:
    login()
