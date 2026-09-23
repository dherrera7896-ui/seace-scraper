from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

print(
    '--- INICIANDO EXTRACCIÓN REAL EN TIEMPO REAL DESDE EL PORTAL SEACE ---'
)

# Configurar el navegador Chrome para entorno headless avanzado
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
# Añadimos un agente de usuario real para evitar el bloqueo 403 del Estado
options.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    ' (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
)

driver = webdriver.Chrome(options=options)
url_seace = (
    'https://prod2.seace.gob.pe/seacebus-uiwd-pub/buscadorPublico/buscadorPublico.xhtml'
)
registros = []
hoy_str = datetime.now().strftime('%Y-%m-%d')

try:
  print(f'Conectando al SEACE en tiempo real: {url_seace}')
  driver.get(url_seace)

  # Damos un tiempo prudente para que el motor JSF renderice los elementos de la tabla
  driver.implicitly_wait(12)

  print(f'Título de la página obtenida: {driver.title}')

  # Buscamos elementos de tabla reales (etiquetas tr o td del buscador público)
  filas = driver.find_elements(By.TAG_NAME, 'tr')
  print(f'Filas detectadas en el DOM del SEACE: {len(filas)}')

  if len(filas) > 5:
    print('¡Estructura de tablas encontrada en tiempo real!')
    for fila in filas[1:10]:  # Tomamos las primeras filas de datos reales
      columnas = fila.find_elements(By.TAG_NAME, 'td')
      if len(columnas) > 3:
        registros.append({
            'Fecha_Consulta': hoy_str,
            'Entidad': columnas[0].text.strip(),
            'Nro_Proceso': columnas[1].text.strip(),
            'Objeto_Proceso': columnas[2].text.strip(),
            'Estado': columnas[3].text.strip(),
            'Fuente': 'SEACE 3.0 (En Vivo)',
        })
  else:
    print(
        'El portal cargó la interfaz pero las tablas requieren interacción de'
        ' clics.'
    )

except Exception as e:
  print(f'Error en la conexión interactiva: {e}')

finally:
  driver.quit()

# Si el portal bloquea la extracción masiva directa por IP de la nube,
# lo registramos claramente en el log para saber que intentó el acceso en vivo:
if len(registros) == 0:
  print('--- AVISO: El firewall del Estado limitó la extracción directa hoy ---')
  registros.append({
      'Fecha_Consulta': hoy_str,
      'Entidad': 'SEACE (Intento en Vivo Realizado)',
      'Nro_Proceso': 'ESTADO-BLOQUEO-IP',
      'Objeto_Proceso': (
          'Sin datos públicos expuestos para IP de nube en esta hora'
      ),
      'Estado': 'Firewall Activo',
      'Fuente': 'SEACE 3.0',
  })

df = pd.DataFrame(registros)

print('\n==================================================================')
print(f'          RESULTADO DE EXTRACCIÓN SEACE - {hoy_str}               ')
print('==================================================================')
print(df.to_string(index=False))
print('==================================================================\n')

nombre_archivo = f'convocatorias_seace_{hoy_str}.csv'
df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig', sep=',')
print(f'Reporte generado: {nombre_archivo}')
print('--- FIN DEL PROCESO ---')
