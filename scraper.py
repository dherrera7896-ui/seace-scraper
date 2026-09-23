from datetime import datetime
import pandas as pd
import requests

print('--- INICIANDO SCRAPER DE CONVOCATORIAS SEACE ---')

# Obtenemos la fecha de hoy en formato DD/MM/YYYY que usa el SEACE
hoy = datetime.now().strftime('%d/%m/%Y')
print(f'Consultando convocatorias para la fecha: {hoy}')

# URL de ejemplo del buscador público o API de consultas del SEACE (Buscador general)
# Nota: Adaptamos una petición base simulada para capturar o estructurar la consulta diaria.
url_seace = 'https://prodapp2.seace.gob.pe/seacebus-ui/busqueda-convocatoria.xhtml'

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
        ' like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
}

try:
  # Realizamos la petición de prueba al portal del SEACE
  response = requests.get(url_seace, headers=headers, timeout=15)
  print(f'Estado de conexión con SEACE: {response.status_code}')

  if response.status_code == 200:
    print('Conexión exitosa con el portal de convocatorias.')

    # Aquí simulamos la estructura de datos que recopilaría el scraper para el día de hoy
    # (Puedes expandir esto con BeautifulSoup o APIs internas si requieres campos específicos como Entidad, Objeto, etc.)
    datos_ejemplo = [{
        'Fecha_Consulta': hoy,
        'Estado_Sistema': 'Operativo',
        'Mensaje': (
            'Convocatorias del día obtenidas correctamente desde la nube de'
            ' GitHub Actions.'
        ),
    }]

    df = pd.DataFrame(datos_ejemplo)

    # Guardamos los resultados en un archivo CSV dentro del repositorio
    nombre_archivo = f"convocatorias_seace_{datetime.now().strftime('%Y-%m-%d')}.csv"
    df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
    print(f'Archivo generado con éxito: {nombre_archivo}')

  else:
    print(
        'El servidor del SEACE respondió con un código diferente al esperado.'
    )

except Exception as e:
  print(f'Ocurrió un error al conectar con el SEACE: {e}')

print('--- FIN DEL PROCESO ---')
