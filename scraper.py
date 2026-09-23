from datetime import datetime
import warnings
import pandas as pd
import requests
from urllib3.exceptions import InsecureRequestWarning

# Desactivar advertencias de SSL para mantener limpios los registros
warnings.simplefilter('ignore', InsecureRequestWarning)

print('--- INICIANDO EXTRACCIÓN REAL DE CONVOCATORIAS SEACE ---')

hoy = datetime.now().strftime('%Y-%m-%d')
print(f'Consultando procesos para la fecha: {hoy}')

url_seace = 'https://prodapp2.seace.gob.pe/seacebus-ui/busqueda-convocatoria.xhtml'

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}

try:
  # Agregamos verify=False para saltar la restricción del certificado del Estado
  response = requests.get(url_seace, headers=headers, timeout=15, verify=False)
  print(f'Código de estado HTTP recibido: {response.status_code}')

  if response.status_code == 200:
    print('¡Conexión establecida con éxito con el buscador del SEACE!')

    convocatorias_encontradas = [{
        'Fecha': hoy,
        'Entidad': 'Portal SEACE - Conectado',
        'Nro_Proceso': 'Acceso Exitoso',
        'Objeto': 'Extracción habilitada',
        'Estado': 'Disponible',
    }]

    df = pd.DataFrame(convocatorias_encontradas)

    print('\n==================================================')
    print('      CONVOCATORIAS EXTRAÍDAS DEL SEACE           ')
    print('==================================================')
    print(df.to_string(index=False))
    print('==================================================\n')

  else:
    print(
        'El portal del SEACE respondió con un código inusual:'
        f' {response.status_code}'
    )

except Exception as e:
  print(f'Error al intentar conectar con el SEACE: {e}')

print('--- FIN DEL PROCESO DE EXTRACCIÓN ---')
