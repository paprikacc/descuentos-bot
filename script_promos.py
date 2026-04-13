import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

# URL de la página a scrapear
url = 'https://promos.clash.com.ar/supermercados/'

try:
    # Obtener el contenido de la página
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    # Parsear el HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extraer datos simples
    descuentos = []
    
    # Buscar elementos con información de descuentos
    for elemento in soup.find_all(['div', 'tr', 'li']):
        texto = elemento.get_text(strip=True)
        if 'descuento' in texto.lower() or '%' in texto:
            descuentos.append({'Información': texto})
    
    # Si no encuentra datos, crear un registro vacío
    if not descuentos:
        descuentos.append({'Información': 'No se encontraron descuentos', 'Timestamp': datetime.now()})
    
    # Crear DataFrame
    df = pd.DataFrame(descuentos)
    
    # Guardar en Excel
    archivo_excel = 'promos_supermercados.xlsx'
    df.to_excel(archivo_excel, index=False)
    
    print(f'✅ Descuentos guardados en {archivo_excel}')
    print(f'Total de registros: {len(descuentos)}')
    
except Exception as e:
    print(f'❌ Error: {e}')
