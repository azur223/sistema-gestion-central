import streamlit as st
import pandas as pd
import time

# Configuración de la pantalla
st.set_page_config(page_title="Rastreador OSINT Real", layout="wide", page_icon="🕵️‍♂️")

# Inicializar Base de Datos interna para guardar pistas reales
if "pistas_reales" not in st.session_state:
    st.session_state["pistas_reales"] = []

# Sistema de Seguridad Privado
if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False

if not st.session_state["autenticado"]:
    st.title("🔐 Acceso al Sistema OSINT de Localización")
    st.write("Introduce las credenciales de administrador para activar los rastreadores en vivo.")
    clave = st.text_input("Clave de Acceso Central:", type="password")
    if st.button("Iniciar Sistema"):
        if clave == "control2026":
            st.session_state["autenticado"] = True
            st.rerun()
        else:
            st.error("Clave incorrecta.")

# Panel de Control con Búsqueda Real
else:
    st.sidebar.title("🕹️ Panel de Control")
    st.sidebar.write("Estado del Bot: **Listo para Buscar** 🟢")
    
    opcion = st.sidebar.radio("Selecciona una opción:", ["🔍 Rastreador Web Real", "🗄️ Pistas Guardadas"])
    
    if st.sidebar.button("Cerrar Sistema"):
        st.session_state["autenticado"] = False
        st.rerun()

    # --- MÓDULO DE BÚSQUEDA REAL ---
    if opcion == "🔍 Rastreador Web Real":
        st.title("🕵️‍♂️ Buscador OSINT Automatizado en Internet")
        st.write("Este módulo realiza consultas **reales y en vivo** en toda la web abierta (redes, noticias, alertas) usando el motor de indexación.")

        # Cuadros de entrada de datos limpios
        nombre_buscar = st.text_input("Nombre completo de la persona a localizar:").strip()
        contexto_buscar = st.text_input("Datos adicionales obligatorios (Ej: país, ciudad, edad o año de desaparición):").strip()

        if st.button("🚀 Lanzar Agente de Buesqueda en Internet"):
            if nombre_buscar and contexto_buscar:
                # Mostrar animación de que está trabajando de verdad
                with st.spinner(f"El bot está navegando la web ahora mismo buscando coincidencias de '{nombre_buscar}'..."):
                    try:
                        # Llamamos a la herramienta de búsqueda real instalada
                        from duckduckgo_search import DDGS
                        
                        # Construcción del comando de búsqueda inteligente cruzando los datos
                        comando_busqueda = f'"{nombre_buscar}" {contexto_buscar} (desaparecido OR desaparecida OR missing OR busqueda)'
                        
                        # Ejecutar la consulta real en internet
                        with DDGS() as ddgs:
                            resultados_vivos = list(ddgs.text(comando_busqueda, max_results=8))
                        
                        if resultados_vivos:
                            st.success(f"⚠️ ¡Rastreo Completo! Se detectaron {len(resultados_vivos)} publicaciones o páginas reales en internet:")
                            
                            # Mostrar cada resultado real extraído de internet
                            for i, resultado in enumerate(resultados_vivos):
                                titulo = resultado.get("title", "Página sin título")
                                link = resultado.get("href", "#")
                                fragmento = resultado.get("body", "No hay fragmento de texto disponible.")
                                
                                # Tarjeta visual para cada hallazgo
                                with st.expander(f"📄 Coincidencia {i+1}: {titulo}"):
                                    st.write(f"🔗 **Dirección de la página:** {link}")
                                    st.write(f"📝 **Información hallada dentro de la web:** {fragmento}")
                                    
                                    # Guardar automáticamente este hallazgo en la base de datos
                                    registro_pista = {
                                        "Persona Buscada": nombre_buscar,
                                        "Pista / Título de la Web": titulo,
                                        "Texto Encontrado": fragmento,
                                        "Enlace de la Fuente": link,
                                        "Fecha del Hallazgo": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")
                                    }
                                    # Evitar duplicados simples
                                    if registro_pista not in st.session_state["pistas_reales"]:
                                        st.session_state["pistas_reales"].append(registro_pista)
                        else:
                            st.warning("El bot recorrió internet pero no detectó ninguna página pública reciente que combine ese nombre exacto con las palabras de desaparición. Intenta afinando el nombre o quitando palabras del segundo cuadro.")
                            
                    except Exception as error_motor:
                        st.error("Hubo un problema al conectar el buscador en vivo.")
                        st.info("Asegúrate de haber completado el Paso 1 (crear el archivo requirements.txt en GitHub) y espera 1 minuto a que Streamlit se reinicie por completo.")
                        st.caption(f"Detalle técnico del error: {error_motor}")
            else:
                st.warning("Por favor rellena tanto el Nombre como el Contexto (país/ciudad) para que la búsqueda sea precisa.")

    # --- MÓDULO DE BASE DE DATOS DE INFORMES REALES ---
    elif opcion == "🗄️ Pistas Guardadas":
        st.title("🗄️ Repositorio de Información y Evidencias Reales")
        st.write("Aquí se acumulan automáticamente los textos y enlaces reales que el bot rescató de internet durante tus búsquedas.")
        
        if st.session_state["pistas_reales"]:
            df = pd.DataFrame(st.session_state["pistas_reales"])
            st.dataframe(df, use_container_width=True)
            
            # Botón para descargar el reporte real al celular
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Guardar Reporte OSINT en el Celular (CSV)",
                data=csv,
                file_name="evidencias_localizacion_osint.csv",
                mime="text/csv",
            )
            
            if st.button("🗑️ Vaciar evidencias"):
                st.session_state["pistas_reales"] = []
                st.rerun()
        else:
            st.info("La base de datos está limpia. Las pistas reales aparecerán aquí una vez que el bot intercepte datos en la web.")
