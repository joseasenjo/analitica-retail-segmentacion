
#  Analítica Retail: Segmentación Internacional

He creado un ecosistema RETRAIL DATA STRATEGIC integral de Inteligencia Competitiva (ETL + BI) diseñado para monitorizar el posicionamiento de precios, la profundidad de catálogo y la disponibilidad de inventario de competidores en el sector retail de moda. 

Este proyecto resuelve el problema de la asimetría de información comercial, transformando código HTML desestructurado en un panel de decisiones estratégicas en tiempo real.

---

##  Arquitectura del Sistema

La infraestructura ha sido diseñada bajo un paradigma de **máxima eficiencia computacional y privacidad de ejecución**. 

* **Procesamiento en Memoria (RAM):** A diferencia de los scrapers tradicionales que abusan de operaciones I/O en disco duro o levantan instancias pesadas de navegadores (Selenium), este motor ejecuta la extracción, limpieza y transformación de las matrices de datos dinámicamente en la memoria RAM del servidor virtual (VPS). 
* **Persistencia Ligera:** Los datos limpios se inyectan en una base de datos `SQLite` (`retail_history.db`), garantizando un registro histórico robusto sin el consumo en segundo plano de gestores de bases de datos pesados.
* **Pipeline ETL Optimizado:** El scraper interactúa directamente con los nodos estructurales del DOM y los atributos transaccionales (`data-product-*` en plataformas como Shopify) para extraer métricas de negocio con un consumo mínimo de ancho de banda.

---

##  Lógica de Negocio y Métricas Estratégicas

El sistema no se limita a mostrar precios; calcula KPIs fundamentales para la toma de decisiones comerciales:

* **Price Index (Índice de Precios):** Benchmarking cruzado para determinar el posicionamiento exacto de una firma (volumen vs. margen) respecto a la media del mercado.
* **Capital Inmovilizado (Inventory Valuation):** Decodificación en tiempo real de las cadenas de stock por talla para calcular el *Revenue Potencial* retenido en los almacenes del competidor.
* **Markdown Opportunity:** Algoritmo conceptualizado para identificar SKUs con alta retención de inventario y baja rotación, ideales para campañas de rebajas quirúrgicas.
* **Price Elasticity Gap:** Contraste dinámico entre la media y la mediana estadística del catálogo para limpiar el "ruido" de productos *Outliers* y entender la tolerancia real de precios del consumidor.

---

##  Stack Tecnológico

El proyecto está construido íntegramente en **Python**, priorizando librerías estándar y analíticas de alta velocidad:

* **Data Extraction:** `requests`, `BeautifulSoup4` (BS4), `re` (Expresiones regulares).
* **Data Transformation:** `pandas`, `numpy` (operaciones vectorizadas en RAM).
* **Data Load (Persistencia):** `sqlite3` (Base de datos relacional autocontenida).
* **Data Visualization (BI):** `streamlit` (Renderizado interactivo, reactivo y cloud-ready).

---

##  Roadmap y Escalabilidad Técnica (Fase SaaS)

El diseño modular actual sienta las bases para una futura migración hacia una arquitectura orientada a servicios (SaaS) con un modelo de monetización limpio y sin publicidad. Las siguientes implementaciones están en fase de diseño:

1. **API REST de Alto Rendimiento:** Transición del enrutamiento web básico a **FastAPI** para la entrega de datos procesados mediante endpoints asíncronos.
2. **Autenticación y Seguridad:** Implementación de **JWT (JSON Web Tokens)** para gestionar sesiones de usuarios empresariales y limitar accesos.
3. **Gestión de Tráfico (Rate Limiting):** Creación de un algoritmo de asignación de cuotas para el modelo Freemium (ej. límite de 5 peticiones por IP cada 24 horas, con escalado ilimitado para cuentas de pago).
4. **Contenerización:** Empaquetado completo del ecosistema ETL y BI mediante **Docker** para despliegues agnósticos y replicables en cualquier infraestructura cloud.

---

##  Instalación y Despliegue Local

Para ejecutar este entorno de inteligencia retail en tu propia máquina:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/tu-usuario/analitica-retail-segmentacion.git](https://github.com/tu-usuario/analitica-retail-segmentacion.git)
   cd analitica-retail-segmentacion

   Instalar dependencias:
Se recomienda usar un entorno virtual (venv o conda)

pip install -r requirements.txt

Ejecutar el motor ETL (Captura de datos diarios):

Bash
python extractor.py
nota: Esto generará y poblará la base de datos local retail_history.db.

Lanzar el Panel de Visualización (BI):

Bash
streamlit run app.py

Desarrollado por Jose Luis Asenjo | Retail Data Strategist
