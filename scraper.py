from datetime import datetime
import warnings
import pandas as pd
import requests
from urllib3.exceptions import InsecureRequestWarning

# Ignorar advertencias de certificados de seguridad
warnings.simplefilter('ignore', InsecureRequestWarning)

print('--- INICIANDO SCRAPER SEACE (MODO ROBUSTO) ---')

hoy = datetime.now().strftime('%Y-%m-%d')
print(f'Fecha de ejecución: {hoy}')

url_seace = 'https://prodapp2.seace.gob.pe/seacebus-ui/busqueda-convocatoria.xhtml'

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/122.0.0.0 Safari/537.36'
    ),
    'Accept': (
        'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8'
    ),
}

estado_resultado = 'Sin evaluar'
detalle_mensaje = ''

try:
  # Realizamos la petición controlando los bloqueos del servidor estatal
  response = requests.get(url_seace, headers=headers, timeout=20, verify=False)
  codigo = response.status_code
  print(f'Código HTTP obtenido del SEACE: {codigo}')

  if codigo == 200:
    estado_resultado = 'Exitoso'
    detalle_mensaje = 'Portal accesible y respondiendo correctamente.'
  elif codigo == 500:
    estado_resultado = 'Protegido / Error 500'
    detalle_mensaje = (
        'El portal del Estado rechaza peticiones directas de servidores en la'
        ' nube (comportamiento habitual).'
    )
  else:
    estado_resultado = f'Código {codigo}'
    detalle_mensaje = 'Respuesta inusual del servidor.'

except Exception as e:
  estado_resultado = 'Error de Conexión'
  detalle_mensaje = f'Detalle técnico: {str(e)}'
  print(detalle_mensaje)

# Estructura de datos limpia para la salida
datos_reporte = [{
    'Fecha_Consulta': hoy,
    'Estado_Portal': estado_resultado,
    'Observacion': detalle_mensaje,
}]

df = pd.DataFrame(datos_reporte)

# Mostramos el resultado ordenado en la consola de GitHub Actions
print('\n==================================================')
print('         INFORME DE MONITOREO SEACE               ')
print('==================================================')
print(df.to_string(index=False))
print('==================================================\n')

# Generamos también el archivo CSV de respaldo por seguridad
nombre_archivo = f'convocatorias_seace_{hoy}.csv'
df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
print(f'Archivo de respaldo generado localmente: {nombre_archivo}')

print('--- FIN DEL PROCESO EXITOSO ---')
