import streamlit as st

# 1. Configuración de pantalla
st.set_page_config(page_title="Centro de Inteligencia", layout="wide", page_icon="🔐")

# 2. Sistema de Seguridad (Contraseña Privada)
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Sistema de Monitoreo Restringido")
    st.write("Por favor, introduce tus credenciales de administrador para operar el sistema.")
    
    # Formulario de entrada
    clave = st.text_input("Clave de Acceso Central:", type="password")
    boton_ingresar = st.button("Iniciar Sistema")
    
    # Cambia "control2026" por la contraseña que tú quieras
    if boton_ingresar:
        if clave == "control2026":
            st.session_state["autenticado"] = True
            st.success("Acceso concedido. Iniciando módulos...")
            st.rerun()
        else:
            st.error("Clave incorrecta. Intento de acceso registrado.")

# 3. Panel de Control Principal (Solo visible si pasas la contraseña)
else:
    # Barra lateral de navegación
    st.sidebar.title("🕹️ Panel de Control")
    st.sidebar.write("Estado: **En línea** 🟢")
    
    # Menú de opciones
    opcion = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Inicio / Estado", "Módulo OSINT (Rastreo)", "Base de Datos", "Configuración"]
    )
    
    # Botón para cerrar sesión
    if st.sidebar.button("Cerrar Sistema (Log out)"):
        st.session_state["autenticado"] = False
        st.rerun()

    # --- CONTENIDO DE LAS PÁGINAS ---
    if opcion == "Inicio / Estado":
        st.title("Centro de Control y Gestión OSINT")
        st.info("Bienvenido, Administrador. Todos los sistemas operativos.")
        
        # Cuadros de métricas visuales
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Consultas de IA hoy", value="0 / Ilimitado")
        col2.metric(label="Bases de datos activas", value="Conectada")
        col3.metric(label="Seguridad del Entorno", value="100% Privado")

    elif opcion == "Módulo OSINT (Rastreo)":
        st.title("🔍 Módulo OSINT y Rastreo")
        st.write("Este espacio estará dedicado a los motores de búsqueda automática y análisis de datos de internet.")
        st.text_input("Introduce un objetivo, palabra clave o usuario a analizar:")
        st.button("Iniciar Rastreo")

    elif opcion == "Base de Datos":
        st.title("🗄️ Gestión de Datos Internos")
        st.write("Aquí podrás ver, organizar y descargar los reportes generados por la aplicación.")
        
    elif opcion == "Configuración":
        st.title("⚙️ Ajustes del Sistema")
        st.write("Configuración avanzada de las conexiones de Inteligencia Artificial.")
