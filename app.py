import streamlit as st
import sqlite3
import pandas as pd
import numpy as np

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Retail Intelligence System", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. INYECCIÓN DE ESTILO GLOBAL (FUENTE CARDO Y FOOTER)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cardo:ital,wght@0,400;0,700;1,400&display=swap');
    
    /* Aplicación de la fuente Cardo a toda la interfaz */
    html, body, [data-testid="stMarkdownContainer"], .stMetric, .stTabs, button, blockquote {
        font-family: 'Cardo', serif !important;
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #ffffff;
        color: #6b7280;
        text-align: center;
        padding: 10px;
        font-size: 14px;
        border-top: 1px solid #e5e7eb;
        z-index: 999;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        font-weight: 600;
    }
    .live-badge {
        background-color: #e6f4ea;
        color: #137333;
        padding: 4px 12px;
        border-radius: 16px;
        font-size: 14px;
        font-weight: bold;
        display: inline-block;
        margin-bottom: 15px;
        border: 1px solid #ceead6;
    }
    </style>
    <div class="footer">
        Creado por Jose Luis Asenjo • Retail Data Strategist
    </div>
    """, unsafe_allow_html=True)

# 3. FUNCIONES DE PROCESAMIENTO DE DATOS EN MEMORIA (RAM)
def calcular_unidades_stock(stock_str):
    if not stock_str or pd.isna(stock_str) or stock_str == "N/A":
        return 0
    total_unidades = 0
    try:
        partes = str(stock_str).split(',')
        for parte in partes:
            if '|' in parte:
                subpartes = parte.split('|')
                if len(subpartes) == 2:
                    total_unidades += int(subpartes[1])
            elif parte.isdigit():
                total_unidades += int(parte)
    except Exception:
        return 0
    return total_unidades

def cargar_datos_analiticos():
    try:
        conn = sqlite3.connect('retail_history.db')
        df = pd.read_sql_query("SELECT * FROM historico_precios", conn)
        conn.close()
        
        # Transformaciones dinámicas eficientes
        df['unidades_stock'] = df['stock'].apply(calcular_unidades_stock)
        df['valor_inventario'] = df['precio'] * df['unidades_stock']
        return df
    except Exception:
        return pd.DataFrame(columns=["fecha", "tienda", "producto", "precio", "stock", "unidades_stock", "valor_inventario"])

# 4. CARGA DE DATOS
df = cargar_datos_analiticos()

# 5. RENDERIZADO DE LA INTERFAZ DE USUARIO
if df.empty:
    st.title("📊 Retail Price & Stock Intelligence System")
    st.info("La base de datos está inicializándose. Por favor, ejecuta 'extractor.py' primero para capturar los primeros datos de mercado.")
else:
    # --- BARRA LATERAL (SIDEBAR) ---
    st.sidebar.header("Filtros de Búsqueda")
    tiendas_disponibles = df["tienda"].unique().tolist()
    tienda_sel = st.sidebar.multiselect("Selecciona Tiendas", tiendas_disponibles, default=tiendas_disponibles)
    
    # Filtrado del DataFrame principal según la selección del usuario
    df_filtrado = df[df["tienda"].isin(tienda_sel)]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📘 Documentación Estratégica")
    st.sidebar.info("Info sobre arquitectura técnica y el modelo de negocio detrás de este cuadro de mando.")
    
    st.sidebar.link_button("Ver Presentación (Pitch Deck) ↗", "https://eduard289.github.io/analitica-retail-segmentacion/presentacion.html")

    # --- ENCABEZADO PRINCIPAL ---
    st.title("📊 Retail Price & Stock Intelligence System")
    
    # Indicador de datos reales en tiempo real
    st.markdown('<div class="live-badge">🟢 Datos Reales • Actualizados en Tiempo Real</div>', unsafe_allow_html=True)
    st.caption("Plataforma de Inteligencia Competitiva para la Optimización de Márgenes y Análisis de Surtido")

    # POP-UP MODERNO (GLOSARIO ESTRATÉGICO)
    with st.popover("📖 Glosario Retail Data Strategic"):
        st.markdown("### Conceptos y Métricas Clave de Negocio")
        st.markdown("""
        * **Price Index (Índice de Precios):** Mide el posicionamiento relativo de los precios de una firma frente al promedio ponderado del mercado. Permite detectar estrategias de volumen o de margen.
        * **Price Elasticity Gap:** Brecha analítica calculada mediante la diferencia entre la media y la mediana del surtido. Indica la sensibilidad y tolerancia del consumidor a precios extremos en el catálogo.
        * **Inventory Valuation (Capital Inmovilizado):** Valor monetario total de las existencias actuales calculado a precio de venta al público (PVP). Representa el potencial de facturación retenido en stock.
        * **Markdown Opportunity:** Algoritmo de detección de ineficiencias que aísla SKUs con altos volúmenes de inventario y bajo rendimiento de salida, candidatos idóneos para promociones quirúrgicas.
        """)

    # --- ARQUITECTURA DE PESTAÑAS (TABS) ---
    tab_global, tab_spf, tab_renatta, tab_comparativa = st.tabs([
        "🌐 Visión Global", 
        "👕 Análisis Springfield", 
        "👗 Análisis Renatta & Go", 
        "⚔️ Comparativa de Posicionamiento"
    ])

    # Bins de precio estándar para los histogramas de distribución
    bins_precio = [0, 10, 15, 20, 30, 50, 100]
    labels_precio = ['0-10€', '10-15€', '15-20€', '20-30€', '30-50€', '50€+']

    # ==========================================
    # PESTAÑA 1: VISIÓN GLOBAL (HEAD-TO-HEAD)
    # ==========================================
    with tab_global:
        st.markdown("### 📈 Resumen Ejecutivo Omnicanal")
        
        # Cálculos de medias estratégicas
        media_global = df['precio'].mean()
        df_spf_all = df[df['tienda'] == 'Springfield']
        df_ren_all = df[df['tienda'] == 'Renatta & Go']
        
        media_spf = df_spf_all['precio'].mean() if not df_spf_all.empty else 0
        media_ren = df_ren_all['precio'].mean() if not df_ren_all.empty else 0

        # Bloque de KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(
                label="Media Springfield", 
                value=f"{media_spf:.2f} €", 
                delta=f"{(media_spf/media_global-1)*100:+.1f}% vs General" if media_global else None,
                delta_color="inverse"
            )
        with col2:
            st.metric(
                label="Media Renatta & Go", 
                value=f"{media_ren:.2f} €", 
                delta=f"{(media_ren/media_global-1)*100:+.1f}% vs General" if media_global else None,
                delta_color="inverse"
            )
        with col3:
            st.metric(
                label="Capital Inmovilizado Global", 
                value=f"{df_filtrado['valor_inventario'].sum():,.2f} €".replace(",", "X").replace(".", ",").replace("X", ".")
            )
        with col4:
            st.metric(
                label="Precio Mediano de Mercado", 
                value=f"{df_filtrado['precio'].median():.2f} €"
            )

        st.markdown("---")
        st.markdown("### 📊 Surtido Actual en Paralelo")
        
        col_izq, col_der = st.columns(2)
        with col_izq:
            st.subheader("Catálogo Springfield")
            st.dataframe(
                df_filtrado[df_filtrado["tienda"] == "Springfield"][["producto", "precio", "fecha"]], 
                use_container_width=True, 
                hide_index=True
            )
        with col_der:
            st.subheader("Catálogo Renatta & Go")
            st.dataframe(
                df_filtrado[df_filtrado["tienda"] == "Renatta & Go"][["producto", "precio", "unidades_stock", "fecha"]], 
                use_container_width=True, 
                hide_index=True
            )

        # SECCIÓN OPTIMIZADA: HISTÓRICO SIN RUIDO VISUAL
        st.markdown("---")
        st.markdown("### 📜 Histórico de Registros Transaccionales")
        st.write("Evolución temporal completa y auditoría de todos los registros indexados en la base de datos:")
        
        df_historico_limpio = df_filtrado[["fecha", "tienda", "producto", "precio"]].sort_values(by="fecha", ascending=False)
        st.dataframe(df_historico_limpio, use_container_width=True, hide_index=True)

        # PANEL DE ACCIONES OPERATIVAS E INFORMES EJECUTIVOS
        st.markdown("#### 💼 Centro de Informes y KPIs Ejecutivos")
        st.write("Interactúa con los datos históricos para generar métricas avanzadas bajo demanda u obtener reportes exportables:")
        
        btn_col1, btn_col2, btn_col3 = st.columns(3)
        
        with btn_col1:
            csv_data = df_historico_limpio.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Descargar Informe Ejecutivo (CSV)",
                data=csv_data,
                file_name="informe_ejecutivo_retail.csv",
                mime="text/csv",
                use_container_width=True
            )
            
        with btn_col2:
            if st.button("📊 Calcular Pricing Drift (Volatilidad)", use_container_width=True):
                st.markdown("**Análisis de Estabilidad de Precios:**")
                for t in df_filtrado['tienda'].unique():
                    sub_df = df_filtrado[df_filtrado['tienda'] == t]
                    desviacion = sub_df['precio'].std()
                    st.info(f"• **{t}**: Desviación estándar de {desviacion:.2f} €. Un valor bajo indica precios estables y consolidados.")
                    
        with btn_col3:
            if st.button("📊 Analizar Share of Voice (Mix de Catálogo)", use_container_width=True):
                st.markdown("**Distribución de Cuota de Mercado por SKUs:**")
                total_skus = len(df_filtrado)
                if total_skus > 0:
                    for t in df_filtrado['tienda'].unique():
                        sub_df = df_filtrado[df_filtrado['tienda'] == t]
                        porcentaje = (len(sub_df) / total_skus) * 100
                        st.success(f"• **{t}**: Representa el **{porcentaje:.1f}%** del mix total de productos detectados.")

    # ==========================================
    # PESTAÑA 2: SPRINGFIELD
    # ==========================================
    with tab_spf:
        st.markdown("### 🎯 Métricas de Pricing: Springfield")
        df_spf_f = df_filtrado[df_filtrado["tienda"] == "Springfield"]
        
        if df_spf_f.empty:
            st.warning("Selecciona Springfield en los filtros de la barra lateral.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Precio Entrada (Mínimo)", f"{df_spf_f['precio'].min():.2f} €")
            c2.metric("Precio Medio Calculado", f"{df_spf_f['precio'].mean():.2f} €")
            c3.metric("Precio Mediano", f"{df_spf_f['precio'].median():.2f} €")
            c4.metric("Precio Salida (Máximo)", f"{df_spf_f['precio'].max():.2f} €")

            st.markdown("#### 📦 Distribución de Oferta por Tramos de Precio")
            st.write("Análisis de frecuencias cuantitativas para identificar el núcleo del surtido comercial.")
            counts_spf = pd.cut(df_spf_f['precio'], bins=bins_precio, labels=labels_precio).value_counts().sort_index()
            st.bar_chart(counts_spf)

    # ==========================================
    # PESTAÑA 3: RENATTA & GO
    # ==========================================
    with tab_renatta:
        st.markdown("### 💎 Análisis de Inventario y Posicionamiento: Renatta & Go")
        df_ren_f = df_filtrado[df_filtrado["tienda"] == "Renatta & Go"]
        
        if df_ren_f.empty:
            st.warning("Selecciona Renatta & Go en los filtros de la barra lateral.")
        else:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Precio Mediano", f"{df_ren_f['precio'].median():.2f} €")
            c2.metric("Volumen de Stock Rastreado", f"{int(df_ren_f['unidades_stock'].sum())} uds")
            c3.metric("Valor Total del Inventario", f"{df_ren_f['valor_inventario'].sum():,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
            c4.metric("Amplitud de Gama (SKUs)", len(df_ren_f))

            st.markdown("---")
            col_g1, col_g2 = st.columns(2)
            
            with col_g1:
                st.markdown("#### 🔥 Alertas de Rotura de Stock (Top 5 Críticos)")
                st.write("Productos con existencias críticas en el almacén digital (excluyendo sin stock).")
                df_alertas = df_ren_f[df_ren_f['unidades_stock'] > 0].nsmallest(5, 'unidades_stock')
                st.dataframe(df_alertas[['producto', 'unidades_stock']], use_container_width=True, hide_index=True)
                
            with col_g2:
                st.markdown("#### 📦 Concentración de Surtido por Escala de Precios")
                st.write("Volumen de SKUs posicionados según su nivel de elasticidad de precio.")
                counts_ren = pd.cut(df_ren_f['precio'], bins=bins_precio, labels=labels_precio).value_counts().sort_index()
                st.bar_chart(counts_ren)

    # ==========================================
    # PESTAÑA 4: COMPARATIVA DE PRECIOS
    # ==========================================
    with tab_comparativa:
        st.markdown("### ⚔️ Matriz Avanzada de Competitividad Cruzada")
        
        if len(tienda_sel) < 2:
            st.info("Selecciona ambas marcas en la barra lateral para activar la matriz comparativa de posicionamiento.")
        else:
            resumen_comp = df_filtrado.groupby('tienda')['precio'].agg(['min', 'median', 'mean', 'max', 'std']).rename(
                columns={
                    'min': 'Precio Entrada (Min)', 
                    'median': 'Precio Mediano', 
                    'mean': 'Precio Promedio', 
                    'max': 'Precio Premium (Max)', 
                    'std': 'Desviación Estándar'
                }
            )
            st.table(resumen_comp)
            
            st.markdown("#### 📈 Evolución Histórica / Comparativa Directa de Precios Medios")
            df_comp_pivot = df_filtrado.groupby('tienda')['precio'].mean()
            st.bar_chart(df_comp_pivot)
            
            st.markdown("#### 🕒 Variación Temporal de Precios por Fecha")
            df_evolucion = df_filtrado.groupby(["fecha", "tienda"])["precio"].mean().unstack().fillna(0)
            if len(df_evolucion) > 1:
                st.line_chart(df_evolucion)
            else:
                st.caption("Nota: El gráfico temporal se trazará dinámicamente a medida que el pipeline acumule capturas en diferentes fechas de ejecución.")
