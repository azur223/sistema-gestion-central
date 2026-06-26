import streamlit as st
import urllib.parse

# 1. Configuración de pantalla
st.set_page_config(page_title="Centro de Inteligencia", layout="wide", page_icon="🔐")

# 2. Sistema de Seguridad (Contraseña Privada)
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Sistema de Monitoreo Restringido")
    st.write("Por favor, introduce tus credenciales de administrador para operar el sistema.")
    
    clave = st.text_input("Clave de Acceso Central:", type="password")
    boton_ingresar = st.button("Iniciar Sistema")
    
    if boton_ingresar:
        if clave == "control2026":
            st.session_state["autenticado"] = True
            st.success("Acceso concedido...")
            st.rerun()
        else:
            st.error("Clave incorrecta.")

# 3. Panel de Control Principal (Autenticado)
else:
    st.sidebar.title("🕹️ Panel de Control")
    st.sidebar.write("Estado: **En línea** 🟢")
    
    opcion = st.sidebar.radio(
        "Selecciona un módulo:",
        ["Inicio", "Módulo Redes (OSINT)", "Base de Datos", "Configuración"]
    )
    
    if st.sidebar.button("Cerrar Sistema"):
        st.session_state["autenticado"] = False
        st.rerun()

    # --- MÓDULO DE INICIO ---
    if opcion == "Inicio":
        st.title("Centro de Control y Gestión OSINT")
        st.info("Bienvenido. Todos los sistemas listos para la integración externa.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Conexiones Externas", value="Redes Listas")
        col2.metric(label="Bases de datos", value="Conectada")
        col3.metric(label="Entorno", value="100% Privado")

    # --- MÓDULO DE REDES SOCIALES (NUEVO) ---
    elif opcion == "Módulo Redes (OSINT)":
        st.title("🔍 Central de Consultas y Conexión de Redes")
        st.write("Introduce un nombre de usuario, término o alias para generar las pasarelas de acceso directo.")

        # Entrada de datos limpia
        target = st.text_input("Nombre de usuario u objetivo a verificar (Ej: nombreusuario):").strip()

        if target:
            # Codificar el texto para que sea seguro en URLs de navegación
            target_encoded = urllib.parse.quote(target)
            
            st.subheader("🔗 Pasarelas de Acceso Directo")
            st.write("Selecciona la plataforma a la que deseas redirigir la consulta:")

            # Creación de columnas con botones de redirección integrados
            c1, c2, c3 = st.columns(3)
            
            with c1:
                st.info("🌐 Facebook")
                url_fb = f"https://www.facebook.com/search/top/?q={target_encoded}"
                st.link_button("Buscar en Facebook", url_fb)

            with c2:
                st.success("📸 Instagram")
                # Si es un nombre de usuario, va directo al perfil, si no, busca la etiqueta
                url_ig = f"https://www.instagram.com/{target_encoded}/"
                st.link_button("Ver Perfil/Tag IG", url_ig)

            with c3:
                st.error("🐦 X / Twitter")
                url_tw = f"https://x.com/search?q={target_encoded}"
                st.link_button("Buscar en X (Twitter)", url_tw)

            st.write("---")
            st.subheader("🛠️ Estado de Conexión de APIs Oficiales")
            st.caption("Para extracción automatizada de métricas masivas en tiempo real.")
            st.checkbox("Habilitar pasarela para Graph API (Facebook/Instagram)", value=False)
            st.checkbox("Habilitar pasarela para X Developer API", value=False)
        else:
            st.warning("Escribe un nombre de usuario o palabra clave arriba para activar los accesos.")

    # --- OTROS MÓDULOS ---
    elif opcion == "Base de Datos":
        st.title("🗄️ Gestión de Datos Internos")
        st.write("Registro de logs y almacenamiento local de consultas.")
        
    elif opcion == "Configuración":
        st.title("⚙️ Ajustes del Sistema")
        st.write("Aquí se configuran los tokens de acceso privados una vez obtenidos de los paneles de desarrollador.")
