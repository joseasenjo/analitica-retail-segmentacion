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
    .etl-status {
        background-color: #f1f5f9;
        border-left: 4px solid #3b82f6;
        padding: 10px;
        border-radius: 4px;
        margin-top: 15px;
        font-size: 13px;
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
    st.info("La base de datos está inicializándose. Por favor, espera a la primera ejecución del pipeline.")
else:
    # --- BARRA LATERAL (SIDEBAR) ---
    st.sidebar.header("Filtros de Búsqueda")
    tiendas_disponibles = df["tienda"].unique().tolist()
    tienda_sel = st.sidebar.multiselect("Selecciona Tiendas", tiendas_disponibles, default=tiendas_disponibles)
    
    df_filtrado = df[df["tienda"].isin(tienda_sel)]

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📘 Documentación Estratégica")
    st.sidebar.link_button("Ver Presentación (Pitch Deck) ↗", "https://eduard289.github.io/analitica-retail-segmentacion/presentacion.html")
    
    # NUEVO: ETIQUETA DE AUTOMATIZACIÓN ETL PARA EL PORTFOLIO
    st.sidebar.markdown("""
        <div class="etl-status">
            <strong>⚙️ Estado del Pipeline (ETL)</strong><br>
            Sistema de extracción 100% automatizado mediante <em>GitHub Actions</em>. Base de datos actualizada diariamente a las 07:00 AM (UTC) sin intervención manual.
        </div>
    """, unsafe_allow_html=True)

    # --- ENCABEZADO PRINCIPAL ---
    st.title("📊 Retail Price & Stock Intelligence System")
    
    st.markdown('<div class="live-badge">🟢 Datos Reales • Actualizados en Tiempo Real</div>', unsafe_allow_html=True)
    st.caption("Plataforma de Inteligencia Competitiva para la Optimización de Márgenes y Análisis de Surtido")

    with st.popover("📖 Glosario Retail Data Strategic"):
        st.markdown("### Conceptos y Métricas Clave de Negocio")
        st.markdown("""
        * **Price Index (Índice de Precios):** Mide el posicionamiento relativo de los precios.
        * **Price Elasticity Gap:** Brecha analítica calculada mediante la diferencia entre la media y la mediana.
        * **Inventory Valuation:** Valor monetario total de las existencias actuales.
        * **Markdown Opportunity:** Algoritmo de detección de ineficiencias para rebajas quirúrgicas.
        """)

    # --- ARQUITECTURA DE PESTAÑAS (TABS) ---
    tab_global, tab_spf, tab_renatta, tab_comparativa = st.tabs([
        "🌐 Visión Global", 
        "👕 Análisis Springfield", 
        "👗 Análisis Renatta & Go", 
        "⚔️ Comparativa de Posicionamiento"
    ])

    bins_precio = [0, 10, 15, 20, 30, 50, 100]
    labels_precio = ['0-10€', '10-15€', '15-20€', '20-30€', '30-50€', '50€+']

    # ==========================================
    # PESTAÑA 1: VISIÓN GLOBAL (HEAD-TO-HEAD)
    # ==========================================
    with tab_global:
        st.markdown("### 📈 Resumen Ejecutivo Omnicanal")
        
        media_global = df['precio'].mean()
        df_spf_all = df[df['tienda'] == 'Springfield']
        df_ren_all = df[df['tienda'] == 'Renatta & Go']
        
        media_spf = df_spf_all['precio'].mean() if not df_spf_all.empty else 0
        media_ren = df_ren_all['precio'].mean() if not df_ren_all.empty else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(label="Media Springfield", value=f"{media_spf:.2f} €", delta=f"{(media_spf/media_global-1)*100:+.1f}% vs General" if media_global else None, delta_color="inverse")
        with col2:
            st.metric(label="Media Renatta & Go", value=f"{media_ren:.2f} €", delta=f"{(media_ren/media_global-1)*100:+.1f}% vs General" if media_global else None, delta_color="inverse")
        with col3:
            st.metric(label="Capital Inmovilizado Global", value=f"{df_filtrado['valor_inventario'].sum():,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
        with col4:
            st.metric(label="Precio Mediano de Mercado", value=f"{df_filtrado['precio'].median():.2f} €")

        st.markdown("---")
        st.markdown("### 📊 Surtido Actual en Paralelo")
        
        col_izq, col_der = st.columns(2)
        with col_izq:
            st.subheader("Catálogo Springfield")
            st.dataframe(df_filtrado[df_filtrado["tienda"] == "Springfield"][["producto", "precio", "fecha"]], use_container_width=True, hide_index=True)
        with col_der:
            st.subheader("Catálogo Renatta & Go")
            st.dataframe(df_filtrado[df_filtrado["tienda"] == "Renatta & Go"][["producto", "precio", "unidades_stock", "fecha"]], use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("### 📜 Histórico de Registros Transaccionales")
        st.write("Evolución temporal completa y auditoría de todos los registros indexados en la base de datos:")
        
        df_historico_limpio = df_filtrado[["fecha", "tienda", "producto", "precio"]].sort_values(by="fecha", ascending=False)
        st.dataframe(df_historico_limpio, use_container_width=True, hide_index=True)

        # PANEL DE ACCIONES OPERATIVAS Y NUEVO RADAR DE PRECIOS
        st.markdown("#### 💼 Centro de Informes y KPIs Ejecutivos")
        st.write("Interactúa con los datos históricos para generar métricas avanzadas y detectar alertas de mercado:")
        
        btn_col1, btn_col2 = st.columns(2)
        btn_col3, btn_col4 = st.columns(2)
        
        with btn_col1:
            csv_data = df_historico_limpio.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Descargar Informe Ejecutivo (CSV)", data=csv_data, file_name="informe_ejecutivo.csv", mime="text/csv", use_container_width=True)
            
        with btn_col2:
            if st.button("📊 Calcular Pricing Drift (Volatilidad)", use_container_width=True):
                for t in df_filtrado['tienda'].unique():
                    desviacion = df_filtrado[df_filtrado['tienda'] == t]['precio'].std()
                    st.info(f"• **{t}**: Desviación estándar de {desviacion:.2f} €.")
                    
        with btn_col3:
            if st.button("📊 Analizar Share of Voice (Mix)", use_container_width=True):
                total_skus = len(df_filtrado)
                if total_skus > 0:
                    for t in df_filtrado['tienda'].unique():
                        porcentaje = (len(df_filtrado[df_filtrado['tienda'] == t]) / total_skus) * 100
                        st.success(f"• **{t}**: Representa el **{porcentaje:.1f}%** del mix total de productos.")

        # NUEVA FUNCIÓN: RADAR DE VARIACIONES
        with btn_col4:
            if st.button("🚨 Radar de Variaciones (Últimas 24h)", use_container_width=True):
                st.markdown("**Detectando fluctuaciones de precio respecto a la última extracción...**")
                fechas = sorted(df_filtrado['fecha'].unique(), reverse=True)
                
                if len(fechas) >= 2:
                    fecha_hoy = fechas[0]
                    fecha_ayer = fechas[1]
                    
                    df_hoy = df_filtrado[df_filtrado['fecha'] == fecha_hoy][['tienda', 'producto', 'precio']]
                    df_ayer = df_filtrado[df_filtrado['fecha'] == fecha_ayer][['tienda', 'producto', 'precio']]
                    
                    # Cruzar datos por producto para aislar las diferencias de precio
                    df_cambios = pd.merge(df_hoy, df_ayer, on=['tienda', 'producto'], suffixes=(' Actual', ' Anterior'))
                    df_alertas = df_cambios[df_cambios['precio Actual'] != df_cambios['precio Anterior']].copy()
                    
                    if not df_alertas.empty:
                        df_alertas['Variación (€)'] = df_alertas['precio Actual'] - df_alertas['precio Anterior']
                        st.dataframe(df_alertas, use_container_width=True, hide_index=True)
                    else:
                        st.success("✅ Estabilidad de mercado: No se han detectado subidas ni bajadas de precio en el último ciclo.")
                else:
                    st.warning("⚠️ Se necesitan al menos dos días de registros históricos para activar el radar comparativo.")

        # FICHA DE PRODUCTO INDIVIDUAL
        st.markdown("---")
        st.markdown("### 🔍 Ficha de Producto: Análisis Evolutivo Individual")
        st.write("Escribe o selecciona un artículo específico para auditar su histórico transaccional y su curva de precios:")
        
        lista_productos = sorted(df_filtrado["producto"].unique().tolist())
        
        if lista_productos:
            prod_seleccionado = st.selectbox("Buscar o seleccionar un producto del catálogo:", lista_productos)
            df_individual = df_filtrado[df_filtrado["producto"] == prod_seleccionado].sort_values(by="fecha")
            
            if not df_individual.empty:
                f_col1, f_col2 = st.columns([1, 2])
                
                with f_col1:
                    st.markdown(f"**Métricas de Ciclo de Vida**")
                    ultimo_p = df_individual["precio"].iloc[-1]
                    min_p = df_individual["precio"].min()
                    max_p = df_individual["precio"].max()
                    medio_p = df_individual["precio"].mean()
                    marca_p = df_individual["tienda"].iloc[0]
                    
                    st.metric("Último Precio Registrado", f"{ultimo_p:.2f} €")
                    st.metric("Mínimo Histórico Detectado", f"{min_p:.2f} €")
                    st.metric("Máximo Histórico de Salida", f"{max_p:.2f} €")
                    st.caption(f"• **Firma Comercial**: {marca_p}")
                    st.caption(f"• **Precio Medio de Campaña**: {medio_p:.2f} €")
                    
                with f_col2:
                    st.markdown("**Curva Temporal de Posicionamiento de Precio**")
                    df_grafico_ind = df_individual.set_index("fecha")[["precio"]]
                    if len(df_grafico_ind) > 1:
                        st.line_chart(df_grafico_ind)
                    else:
                        st.info("📌 Registro base inicial capturado. La gráfica de tendencia se trazará dinámicamente con la próxima extracción.")

    # ==========================================
    # PESTAÑA 2, 3 Y 4 (SPRINGFIELD, RENATTA Y COMPARATIVA MANTIENEN SU ESTRUCTURA)
    # ==========================================
    with tab_spf:
        st.markdown("### 🎯 Métricas de Pricing: Springfield")
        df_spf_f = df_filtrado[df_filtrado["tienda"] == "Springfield"]
        if not df_spf_f.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Precio Entrada", f"{df_spf_f['precio'].min():.2f} €")
            c2.metric("Precio Medio", f"{df_spf_f['precio'].mean():.2f} €")
            c3.metric("Precio Mediano", f"{df_spf_f['precio'].median():.2f} €")
            c4.metric("Precio Salida", f"{df_spf_f['precio'].max():.2f} €")
            counts_spf = pd.cut(df_spf_f['precio'], bins=bins_precio, labels=labels_precio).value_counts().sort_index()
            st.bar_chart(counts_spf)

    with tab_renatta:
        st.markdown("### 💎 Análisis de Inventario: Renatta & Go")
        df_ren_f = df_filtrado[df_filtrado["tienda"] == "Renatta & Go"]
        if not df_ren_f.empty:
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Precio Mediano", f"{df_ren_f['precio'].median():.2f} €")
            c2.metric("Stock Rastreado", f"{int(df_ren_f['unidades_stock'].sum())} uds")
            c3.metric("Valor Inventario", f"{df_ren_f['valor_inventario'].sum():,.2f} €".replace(",", "X").replace(".", ",").replace("X", "."))
            c4.metric("Amplitud Gama", len(df_ren_f))

            col_g1, col_g2 = st.columns(2)
            with col_g1:
                st.markdown("#### 🔥 Rotura de Stock (Críticos)")
                df_alertas = df_ren_f[df_ren_f['unidades_stock'] > 0].nsmallest(5, 'unidades_stock')
                st.dataframe(df_alertas[['producto', 'unidades_stock']], use_container_width=True, hide_index=True)
            with col_g2:
                st.markdown("#### 📦 Concentración por Precios")
                counts_ren = pd.cut(df_ren_f['precio'], bins=bins_precio, labels=labels_precio).value_counts().sort_index()
                st.bar_chart(counts_ren)

    with tab_comparativa:
        st.markdown("### ⚔️ Matriz Avanzada de Competitividad")
        if len(tienda_sel) >= 2:
            resumen_comp = df_filtrado.groupby('tienda')['precio'].agg(['min', 'median', 'mean', 'max']).rename(columns={'min': 'Mínimo', 'median': 'Mediano', 'mean': 'Promedio', 'max': 'Máximo'})
            st.table(resumen_comp)
            st.markdown("#### 🕒 Variación Temporal por Fecha")
            df_evolucion = df_filtrado.groupby(["fecha", "tienda"])["precio"].mean().unstack().fillna(0)
            if len(df_evolucion) > 1:
                st.line_chart(df_evolucion)
