from datetime import datetime
import pandas as pd
import requests

print('--- INICIANDO SCRAPER DE CONVOCATORIAS SEACE ---')

# Generamos la fecha actual
hoy = datetime.now().strftime('%Y-%m-%d')
print(f'Consultando convocatorias para la fecha: {hoy}')

url_seace = 'https://prodapp2.seace.gob.pe/seacebus-ui/busqueda-convocatoria.xhtml'

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}

try:
  response = requests.get(url_seace, headers=headers, timeout=15)
  print(f'Estado de conexión con SEACE: {response.status_code}')

  if response.status_code == 200:
    print('Conexión exitosa con el portal de convocatorias.')

    # Datos de estructura base para la prueba
    datos_ejemplo = [{
        'Fecha_Consulta': hoy,
        'Estado_Sistema': 'Operativo',
        'Mensaje': 'Convocatorias obtenidas correctamente desde GitHub Actions.',
    }]

    df = pd.DataFrame(datos_ejemplo)

    # Nombre exacto que coincidirá con el artefacto
    nombre_archivo = f'convocatorias_seace_{hoy}.csv'
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f'Archivo generado con éxito: {nombre_archivo}')

  else:
    print('El servidor respondió con un código distinto a 200.')

except Exception as e:
  print(f'Ocurrió un error: {e}')

print('--- FIN DEL PROCESO ---')
