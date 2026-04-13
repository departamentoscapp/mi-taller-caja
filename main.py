import streamlit as st
import pandas as pd
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Caja Taller", layout="wide")

st.title("🛠️ Gestión de Caja - Taller")

# Simulación de Base de Datos (en un caso real usarías st.connection o un CSV en la nube)
if 'datos' not in st.session_state:
    st.session_state.datos = pd.DataFrame(columns=["Fecha", "Tipo", "Metodo", "Monto"])

# --- FORMULARIO DE CARGA ---
with st.sidebar:
    st.header("Registrar Movimiento")
    fecha = st.date_input("Fecha", datetime.now())
    tipo = st.selectbox("Tipo", ["Ingreso", "Egreso"])
    metodo = st.selectbox("Método", ["Efectivo", "Banco", "PayMovil", "Merc Pago", "Dólar"])
    monto = st.number_input("Monto ($)", min_value=0.0, step=100.0)
    
    if st.button("Guardar"):
        nuevo_dato = pd.DataFrame([[fecha, tipo, metodo, monto]], 
                                  columns=["Fecha", "Tipo", "Metodo", "Monto"])
        st.session_state.datos = pd.concat([st.session_state.datos, nuevo_dato], ignore_index=True)
        st.success("¡Guardado!")

# --- VISUALIZACIÓN ---
col1, col2, col3 = st.columns(3)

# Cálculos rápidos
ingresos = st.session_state.datos[st.session_state.datos['Tipo'] == 'Ingreso']['Monto'].sum()
egresos = st.session_state.datos[st.session_state.datos['Tipo'] == 'Egreso']['Monto'].sum()
balance = ingresos - egresos

col1.metric("Ingresos Totales", f"${ingresos:,.0f}")
col2.metric("Egresos Totales", f"${egresos:,.0f}")
col3.metric("Balance Caja", f"${balance:,.0f}", delta=float(balance))

st.divider()

# Tabla de movimientos
st.subheader("Historial de Movimientos")
st.dataframe(st.session_state.datos, use_container_width=True)

# Botón para descargar reporte
csv = st.session_state.datos.to_csv(index=False).encode('utf-8')
st.download_button("Descargar Reporte Excel/CSV", data=csv, file_name="caja_taller.csv")
