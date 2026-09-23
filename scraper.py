from datetime import datetime
import warnings
import pandas as pd
import requests
from urllib3.exceptions import InsecureRequestWarning

# Desactivar advertencias de SSL
warnings.simplefilter('ignore', InsecureRequestWarning)

print('--- INICIANDO CONEXIÓN AVANZADA CON SEACE ---')

hoy = datetime.now().strftime('%Y-%m-%d')
print(f'Fecha del proceso: {hoy}')

url_seace = 'https://prodapp2.seace.gob.pe/seacebus-ui/busqueda-convocatoria.xhtml'

# Usamos una sesión para mantener las cookies y parámetros de navegación
session = requests.Session()

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': (
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    ),
    'Accept-Language': 'es-ES,es;q=0.9',
}

try:
  print('Estableciendo sesión inicial con el portal...')
  # Primero visitamos la raíz o la misma URL para capturar cookies de sesión
  session.get(url_seace, headers=headers, timeout=15, verify=False)

  # Hacemos la consulta oficial usando la misma sesión activa
  response = session.get(url_seace, headers=headers, timeout=15, verify=False)
  print(f'Código de estado HTTP con sesión: {response.status_code}')

  if response.status_code == 200:
    print('¡Conexión y sesión aceptadas por el SEACE!')
    mensaje_resultado = 'Sesión establecida correctamente.'
  else:
    print(f'El servidor respondió con el código: {response.status_code}')
    mensaje_resultado = f'Código HTTP {response.status_code}'

  # Estructura de datos para verificar en la consola
  datos_proceso = [{
      'Fecha': hoy,
      'Estado_HTTP': response.status_code,
      'Detalle': mensaje_resultado,
  }]

  df = pd.DataFrame(datos_proceso)

  print('\n==================================================')
  print('      ESTADO DE LA CONexión SEACE                 ')
  print('==================================================')
  print(df.to_string(index=False))
  print('==================================================\n')

except Exception as e:
  print(f'Ocurrió un error en la conexión: {e}')

print('--- FIN DEL PROCESO ---')
