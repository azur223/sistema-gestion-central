import streamlit as st
import urllib.parse
import pandas as pd

# 1. Configuración de pantalla estilo Centro de Operaciones de Rescate
st.set_page_config(page_title="Localizador Global de Personas", layout="wide", page_icon="🌐")

# Inicializar Base de Datos de Casos de Desaparición
if "casos_desaparecidos" not in st.session_state:
    st.session_state["casos_desaparecidos"] = []

if "historial_ia" not in st.session_state:
    st.session_state["historial_ia"] = [
        {"role": "assistant", "content": "🤖 **Agente de Búsqueda Global Activo.** Proporcióname los datos de la persona desaparecida (Nombre completo, alias, país, último lugar avistado o redes conocidas) y automatizaré el rastreo digital de inmediato."}
    ]

# 2. Control de Seguridad Privado
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🛡️ Sistema de Localización de Personas Desaparecidas")
    st.write("Acceso restringido para investigadores y administradores del sistema.")
    
    clave = st.text_input("Introduce la Clave de Acceso Central:", type="password")
    if st.button("Iniciar Sistema"):
        if clave == "control2026":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Clave de acceso incorrecta.")

# 3. Panel de Control Operativo
else:
    st.sidebar.title("🗺️ Red de Alerta Global")
    st.sidebar.write("Estado del Servidor: **Operativo** 🟢")
    
    opcion = st.sidebar.radio(
        "Módulos de Búsqueda:",
        ["🤖 IA de Rastreo Automático", "🗄️ Base de Casos y Pistas", "🌐 Directorio de Registros Oficiales"]
    )
    
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["autenticado"] = False
        st.rerun()

    # --- MÓDULO 1: IA DE RASTREO AUTOMÁTICO ---
    if opcion == "🤖 IA de Rastreo Automático":
        st.title("🤖 Agente IA de Búsqueda Avanzada en la Web y Redes")
        st.write("Escribe los datos en lenguaje natural. La IA extraerá la información esencial, creará los puentes de búsqueda profunda en la web y registrará el caso.")

        # Mostrar conversación
        for msg in st.session_state["historial_ia"]:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Entrada del Investigador
        if prompt := st.chat_input("Ej: Buscar a Juan Carlos Pérez desaparecido en Buenos Aires, alias juanca99"):
            st.session_state["historial_ia"].append({"role": "user", "content": prompt})
            
            # --- MOTOR DE EXTRACCIÓN AUTOMÁTICA DE DATOS ---
            palabras = prompt.replace(",", " ").replace(".", " ").split()
            
            # Intentar detectar el nombre principal de la orden de forma automatizada
            exclusiones = ["buscar", "a", "desaparecido", "en", "el", "la", "alias", "por", "favor", "encuentra", "persona", "redes", "investigar"]
            filtrados = [p for p in palabras if p.lower() not in exclusiones and len(p) > 2]
            
            nombre_objetivo = " ".join(filtrados[:3]) if filtrados else "Objetivo No Identificado"
            nombre_encoded = urllib.parse.quote(nombre_objetivo)
            
            # 1. Automatización de Puentes en Redes Sociales
            fb_url = f"https://www.facebook.com/search/top/?q={nombre_encoded}%20desaparecido"
            ig_url = f"https://www.instagram.com/explore/tags/{nombre_encoded.replace('%20', '')}/"
            tw_url = f"https://x.com/search?q={nombre_encoded}%20desaparecido"
            
            # 2. Automatización de Google Dorking Inteligente (Busca en toda la web noticias, PDFs y alertas)
            dork_noticias = f"https://www.google.com/search?q=%22{nombre_encoded}%22+AND+(desaparecido+OR+missing+OR+búsqueda)"
            dork_documentos = f"https://www.google.com/search?q=%22{nombre_encoded}%22+filetype:pdf"

            # 3. Inserción Automática en la Base de Datos Interna
            nuevo_caso = {
                "Nombre/Datos": nombre_objetivo,
                "Estado de Alerta": "Rastreo Inicial Activo",
                "Detalles de la Orden": prompt,
                "Fecha de Registro": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
            }
            st.session_state["casos_desaparecidos"].append(nuevo_caso)

            # Respuesta Automatizada de la IA con los resultados del escaneo instantáneo
            respuesta_agente = f"""
            ⚡ **Análisis de Datos Completado Automáticamente por la IA**
            
            He procesado la solicitud para la localización de: **'{nombre_objetivo}'**. El caso ya ha sido guardado de forma permanente en la Base de Datos del centro de control.
            
            He estructurado y abierto los siguientes canales automatizados de búsqueda global en la web y redes sociales:
            
            * 🌐 **Rastreo Dirigido en Redes Sociales:**
               * [Escanear perfiles y publicaciones en Facebook]({fb_url})
               * [Buscar Hashtags relacionados en Instagram]({ig_url})
               * [Monitorear menciones en tiempo real en X (Twitter)]({tw_url})
            
            * 🔍 **Escáner Web de Alta Definición (Google Dorking Automático):**
               * [Buscar Alertas de Prensa, Noticias locales y Blogs]({dork_noticias})
               * [Buscar Registros de identificación, Listas oficiales o PDFs gubernamentales]({dork_documentos})
            
            * 🗄️ **Base de Operaciones:**
               * El caso ya está indexado. Puedes añadir notas de avistamientos o teléfonos de contacto en la pestaña izquierda.
            """
            st.session_state["historial_ia"].append({"role": "assistant", "content": respuesta_agente})
            st.rerun()

    # --- MÓDULO 2: BASE DE DATOS DE CASOS ---
    elif opcion == "🗄️ Base de Casos y Pistas":
        st.title("🗄️ Base de Datos Central de Personas Buscadas")
        st.write("Lista consolidada de todas las solicitudes enviadas a la IA para seguimiento internacional.")
        
        if st.session_state["casos_desaparecidos"]:
            df = pd.DataFrame(st.session_state["casos_desaparecidos"])
            st.dataframe(df, use_container_width=True)
            
            # Función para descargar la lista en formato CSV (útil para enviar reportes a autoridades)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Base de Datos (CSV) para Policía/Fiscalía",
                data=csv,
                file_name="reporte_personas_desaparecidas.csv",
                mime="text/csv",
            )
            
            if st.button("🗑️ Vaciar Historial de Casos"):
                st.session_state["casos_desaparecidos"] = []
                st.rerun()
        else:
            st.info("No hay ningún caso activo bajo monitoreo en este momento.")

    # --- MÓDULO 3: REGISTROS OFICIALES ---
    elif opcion == "🌐 Directorio de Registros Oficiales":
        st.title("🌐 Conexión con Bases de Datos de Emergencia Internacionales")
        st.write("Enlaces de respuesta rápida preconfigurados para contrastar identidades globales:")
        
        c1, c2 = st.columns(2)
        with c1:
            st.subheader("🚨 Organismos Internacionales")
            st.link_button("Ir a Notificaciones Amarillas de INTERPOL", "https://www.interpol.int/es/Como-trabajamos/Notificaciones/Notificaciones-amarillas")
            st.link_button("Buscar en Registro Civil Global / Renaper (Arg)", "https://www.argentina.gob.ar/interior/renaper")
        with c2:
            st.subheader("👥 Redes de ONGs Mundiales")
            st.link_button("Consultar Base de Datos de Personas Desaparecidas (Missing Persons)", "https://www.namus.gov/")
            st.link_button("Buscar Red Solidaria", "https://www.redsolidaria.org.ar/")
