import streamlit as st

# Título
st.title("🎟️ Reservas de Entradas - NM GAMES")

# Eventos disponibles
eventos = ["No hay eventos disponibles"]
reservas = st.session_state.get("reservas", [])

st.header("Haz tu Reserva")

# Formulario
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

# Mostrar reservas existentes
st.header("📋 Lista de Reservas")
if reservas:
    for i, r in enumerate(reservas, start=1):
        st.write(f"**{i}. {r['nombre']}** → {r['cantidad']} entrada(s) para *{r['evento']}*")
else:
    st.info("Aún no hay reservas registradas.")
