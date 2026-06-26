import streamlit as st
import urllib.parse
import pandas as pd

# 1. Configuración de pantalla
st.set_page_config(page_title="Centro de Inteligencia", layout="wide", page_icon="🔐")

# Inicializar la base de datos en memoria si no existe
if "registro_objetivos" not in st.session_state:
    st.session_state["registro_objetivos"] = []

# 2. Sistema de Seguridad
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

# 3. Panel de Control Principal
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
        col1.metric(label="Registros Guardados", value=len(st.session_state["registro_objetivos"]))
        col2.metric(label="Bases de datos", value="Conectada (Local)")
        col3.metric(label="Entorno", value="100% Privado")

    # --- MÓDULO DE REDES SOCIALES ---
    elif opcion == "Módulo Redes (OSINT)":
        st.title("🔍 Central de Consultas y Conexión de Redes")
        st.write("Introduce un nombre de usuario, término o alias para generar las pasarelas de acceso directo.")

        target = st.text_input("Nombre de usuario u objetivo a verificar:").strip()

        if target:
            target_encoded = urllib.parse.quote(target)
            
            st.subheader("🔗 Pasarelas de Acceso Directo")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.info("🌐 Facebook")
                st.link_button("Buscar en Facebook", f"https://www.facebook.com/search/top/?q={target_encoded}")
            with c2:
                st.success("📸 Instagram")
                st.link_button("Ver Perfil/Tag IG", f"https://www.instagram.com/{target_encoded}/")
            with c3:
                st.error("🐦 X / Twitter")
                st.link_button("Buscar en X (Twitter)", f"https://x.com/search?q={target_encoded}")

            st.write("---")
            st.subheader("📝 Registrar Hallazgo")
            nota = st.text_area("Añade notas o detalles sobre este objetivo:")
            categoria = st.selectbox("Categoría:", ["Investigación Activa", "Sospechoso", "Validado", "Archivo"])
            
            if st.button("💾 Guardar en Base de Datos"):
                nuevo_registro = {
                    "Objetivo/Usuario": target,
                    "Categoría": categoria,
                    "Notas/Hallazgos": nota if nota else "Sin notas adicionales",
                    "Fecha de Registro": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state["registro_objetivos"].append(nuevo_registro)
                st.success(f"¡Objetivo '{target}' registrado con éxito!")
        else:
            st.warning("Escribe un nombre de usuario o palabra clave arriba para activar los accesos.")

    # --- MÓDULO BASE DE DATOS (NUEVO Y FUNCIONAL) ---
    elif opcion == "Base de Datos":
        st.title("🗄️ Gestión de Datos Internos")
        st.write("Aquí puedes revisar, filtrar y descargar los reportes guardados durante la sesión.")
        
        if st.session_state["registro_objetivos"]:
            # Convertir la lista en un cuadro de datos visual (DataFrame)
            df = pd.DataFrame(st.session_state["registro_objetivos"])
            
            # Mostrar la tabla interactiva
            st.dataframe(df, use_container_width=True)
            
            # Botón para borrar el historial si lo deseas
            if st.button("🗑️ Limpiar Base de Datos"):
                st.session_state["registro_objetivos"] = []
                st.success("Base de datos despejada.")
                st.rerun()
        else:
            st.info("La base de datos está vacía. Registra objetivos desde el 'Módulo Redes (OSINT)'.")
        
    elif opcion == "Configuración":
        st.title("⚙️ Ajustes del Sistema")
        st.write("Módulo de configuración avanzada.")
