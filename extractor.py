import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import re

# 1. Configuración de la Base de Datos Ligera
def inicializar_db():
    conn = sqlite3.connect('retail_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico_precios (
            fecha TEXT,
            tienda TEXT,
            producto TEXT,
            precio REAL,
            stock TEXT
        )
    ''')
    conn.commit()
    conn.close()

# 2. Extractor de Springfield
def extraer_springfield():
    url = "https://myspringfield.com/es/es/hombre/camisetas"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    datos = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        contenedores = soup.find_all('div', class_=lambda x: x and 'product' in x.lower())
        productos_vistos = set()

        for c in contenedores:
            nombre_tag = c.find(['a', 'h3'], class_=lambda x: x and 'name' in str(x).lower())
            precio_tag = c.find(class_=lambda x: x and 'price' in str(x).lower())
            
            if nombre_tag and precio_tag:
                nombre = nombre_tag.get_text(strip=True)
                precio_raw = precio_tag.get_text(strip=True)
                
                if nombre not in productos_vistos:
                    match = re.search(r'Desde([\d,]+)\s?€', precio_raw)
                    if match:
                        precio_float = float(match.group(1).replace(',', '.'))
                        datos.append((datetime.now().strftime('%Y-%m-%d'), "Springfield", nombre, precio_float, "N/A"))
                        productos_vistos.add(nombre)
    except Exception as e:
        print(f"Error en Springfield: {e}")
    return datos

# 3. Extractor de Renatta & Go
def extraer_renatta():
    url = "https://www.renattandgo.com/collections/camisas-blusas"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    datos = []
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('li', attrs={'data-product-title': True})

        for p in productos:
            nombre = p['data-product-title']
            precio_raw = p['data-product-price']
            stock = p.get('data-product-score-stock', 'U|0')
            
            precio_float = float(precio_raw) / 100
            datos.append((datetime.now().strftime('%Y-%m-%d'), "Renatta & Go", nombre, precio_float, stock))
    except Exception as e:
        print(f"Error en Renatta: {e}")
    return datos

# 4. Orquestador de Carga (Pipeline ETL)
def ejecutar_pipeline():
    inicializar_db()
    print("Iniciando extracción diaria...")
    
    datos_totales = extraer_springfield() + extraer_renatta()
    
    if datos_totales:
        conn = sqlite3.connect('retail_history.db')
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO historico_precios VALUES (?, ?, ?, ?, ?)', datos_totales)
        conn.commit()
        conn.close()
        print(f"¡Éxito! Se han guardado {len(datos_totales)} registros en el histórico.")
    else:
        print("No se pudieron recolectar datos hoy.")

if __name__ == "__main__":
    ejecutar_pipeline()