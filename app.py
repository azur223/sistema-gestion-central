import streamlit as st
import urllib.parse
import pandas as pd

# 1. Configuración de pantalla
st.set_page_config(page_title="Centro de Inteligencia", layout="wide", page_icon="🤖")

# Inicializar estados del sistema si no existen
if "registro_objetivos" not in st.session_state:
    st.session_state["registro_objetivos"] = []
if "historial_chat" not in st.session_state:
    st.session_state["historial_chat"] = [
        {"role": "assistant", "content": "👋 ¡Hola, Administrador! Estoy lista. Escribime qué usuario o término querés investigar y yo me encargo de procesarlo y guardarlo automáticamente."}
    ]

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

# 3. Panel de Control Principal (Autenticado)
else:
    st.sidebar.title("🕹️ Panel de Control")
    st.sidebar.write("Estado: **En línea** 🟢")
    
    opcion = st.sidebar.radio(
        "Selecciona un módulo:",
        ["🤖 Asistente IA (Auto)", "Módulo Redes (Manual)", "Base de Datos", "Configuración"]
    )
    
    if st.sidebar.button("Cerrar Sistema"):
        st.session_state["autenticado"] = False
        st.rerun()

    # --- MÓDULO 1: ASISTENTE IA AUTOMÁTICO ---
    if opcion == "🤖 Asistente IA (Auto)":
        st.title("🤖 Asistente Virtual Automatizado")
        st.write("Dale una orden directa a la IA. El sistema extraerá el objetivo, generará los enlaces y lo registrará solo.")
        
        # Renderizar el historial de conversación en la pantalla
        for msg in st.session_state["historial_chat"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
                
        # Cuadro de entrada de texto estilo chat para el celular
        if orden := st.chat_input("Ej: Busca al usuario carlos99 y registralo en el sistema"):
            # Guardar y mostrar lo que escribió el usuario
            st.session_state["historial_chat"].append({"role": "user", "content": orden})
            
            # --- Lógica del Agente de IA para automatizar ---
            palabras = orden.replace(",", "").replace(".", "").split()
            usuario_detectado = None
            
            # Filtro inteligente para detectar el nombre de usuario de la orden
            for p in palabras:
                if len(p) > 2 and p.lower() not in [
                    "busca", "investiga", "a", "el", "la", "en", "redes", "y", 
                    "guardalo", "por", "favor", "registralo", "usuario", "al"
                ]:
                    usuario_detectado = p
                    break
            
            if usuario_detectado:
                # 1. Automatización: Crear enlaces dinámicos en tiempo real
                target_encoded = urllib.parse.quote(usuario_detectado)
                fb = f"https://www.facebook.com/search/top/?q={target_encoded}"
                ig = f"https://www.instagram.com/{target_encoded}/"
                tw = f"https://x.com/search?q={target_encoded}"
                
                # 2. Automatización: Inserción directa en la Base de Datos sin que hagas clic en nada más
                nuevo_registro = {
                    "Objetivo/Usuario": usuario_detectado,
                    "Categoría": "🤖 IA Automatizado",
                    "Notas/Hallazgos": f"Orden procesada por IA: '{orden}'",
                    "Fecha de Registro": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                }
                st.session_state["registro_objetivos"].append(nuevo_registro)
                
                # Respuesta de la IA confirmando que hizo todo sola
                respuesta_ia = f"⚡ **¡Orden ejecutada con éxito de forma automática!**\n\n" \
                               f"Analicé tu solicitud y detecté el objetivo: **'{usuario_detectado}'**.\n\n" \
                               f"* 🗄️ **Base de datos actualizada:** Ya cargué la información automáticamente en tu módulo de reportes.\n" \
                               f"* 🌐 **Pasarelas de rastreo listas:** Podés inspeccionar sus cuentas haciendo clic acá:\n" \
                               f"  * [Abrir Facebook]({fb})\n" \
                               % f"  * [Abrir Instagram]({ig})\n" \
                               f"  * [Abrir X / Twitter]({tw})"
            else:
                respuesta_ia = "Recibido. Entiendo tu orden, pero no logré identificar el nombre de usuario exacto. Por favor, escribime algo como: *'Busca a juanperez y guardalo'*."
                
            # Guardar respuesta de la IA y recargar la pantalla para mostrar los cambios
            st.session_state["historial_chat"].append({"role": "assistant", "content": respuesta_ia})
            st.rerun()

    # --- MÓDULO 2: REDES SOCIALES MANUAL ---
    elif opcion == "Módulo Redes (Manual)":
        st.title("🔍 Central de Consultas Manuales")
        target = st.text_input("Nombre de usuario u objetivo:").strip()
        if target:
            target_encoded = urllib.parse.quote(target)
            st.subheader("🔗 Pasarelas directas")
            st.link_button("Buscar en Facebook", f"https://www.facebook.com/search/top/?q={target_encoded}")
            st.link_button("Ver Perfil IG", f"https://www.instagram.com/{target_encoded}/")
            st.link_button("Buscar en X", f"https://x.com/search?q={target_encoded}")

    # --- MÓDULO 3: BASE DE DATOS ---
    elif opcion == "Base de Datos":
        st.title("🗄️ Gestión de Datos Internos")
        if st.session_state["registro_objetivos"]:
            df = pd.DataFrame(st.session_state["registro_objetivos"])
            st.dataframe(df, use_container_width=True)
            if st.button("🗑️ Limpiar Base de Datos"):
                st.session_state["registro_objetivos"] = []
                st.rerun()
        else:
            st.info("La base de datos está vacía.")
            
    # --- MÓDULO 4: CONFIGURACIÓN ---
    elif opcion == "Configuración":
        st.title("⚙️ Ajustes del Sistema")
        st.write("Espacio reservado para vincular tokens de Inteligencia Artificial externos avanzados.")
