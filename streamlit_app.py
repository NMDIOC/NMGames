import streamlit as st
import hashlib
import json
import os

# ---------- CONFIGURACIÓN ----------
DB_FILE = "reservas.json"

# Usuario y contraseña cifrados
USUARIO_ADMIN = hashlib.sha256("admin".encode()).hexdigest()
CLAVE_ADMIN = hashlib.sha256("admin".encode()).hexdigest()

# ---------- FUNCIONES ----------
def cargar_reservas():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return []

def guardar_reservas(reservas):
    with open(DB_FILE, "w") as f:
        json.dump(reservas, f, indent=4)

def verificar_login(usuario, clave):
    return (hashlib.sha256(usuario.encode()).hexdigest() == USUARIO_ADMIN and
            hashlib.sha256(clave.encode()).hexdigest() == CLAVE_ADMIN)

# ---------- INICIO ----------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "reservas" not in st.session_state:
    st.session_state["reservas"] = cargar_reservas()

# ---------- INTERFAZ ----------
st.title("🎟️ Sistema de Reservas de Eventos")

menu = st.sidebar.radio("Navegación", ["Hacer Reserva", "Admin"])

# ---------- HACER RESERVA ----------
if menu == "Hacer Reserva":
    st.subheader("Reserva tu entrada 🎫")

    nombre = st.text_input("Nombre completo")
    evento = st.text_input("Evento")
    cantidad = st.number_input("Cantidad de entradas", min_value=1, step=1)

    if st.button("Reservar"):
        if nombre and evento and cantidad:
            reserva = {"nombre": nombre, "evento": evento, "cantidad": cantidad}
            st.session_state["reservas"].append(reserva)
            guardar_reservas(st.session_state["reservas"])
            st.success("✅ ¡Reserva realizada con éxito!")
        else:
            st.error("⚠️ Por favor completa todos los campos.")

# ---------- ADMINISTRACIÓN ----------
elif menu == "Admin":
    if not st.session_state["logged_in"]:
        st.subheader("🔑 Iniciar sesión como administrador")
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")

        if st.button("Ingresar"):
            if verificar_login(usuario, clave):
                st.session_state["logged_in"] = True
                st.success("✅ Sesión iniciada correctamente")
            else:
                st.error("❌ Usuario o contraseña incorrectos")
    else:
        st.subheader("📋 Lista de Reservas")
        if st.session_state["reservas"]:
            for i, reserva in enumerate(st.session_state["reservas"], 1):
                st.write(f"{i}. {reserva['nombre']} - {reserva['evento']} - {reserva['cantidad']} entradas")
        else:
            st.info("Aún no hay reservas registradas.")

        if st.button("Cerrar sesión"):
            st.session_state["logged_in"] = False
            st.success("🔒 Sesión cerrada correctamente")
