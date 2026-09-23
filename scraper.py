from datetime import datetime
import pandas as pd

print('--- INICIANDO VISUALIZACIÓN DE DATOS SEACE ---')

hoy = datetime.now().strftime('%Y-%m-%d')

# Estructura limpia simulando la tabla que procesará el scraper
registros = [
    {
        'Fecha': hoy,
        'Entidad': 'MUNICIPALIDAD EJEMPLO',
        'Nro_Proceso': 'LP-001-2026',
        'Objeto': 'Adquisición de bienes generales',
        'Estado': 'Publicado',
    },
    {
        'Fecha': hoy,
        'Entidad': 'MINISTERIO DE PRUEBA',
        'Nro_Proceso': 'AS-042-2026',
        'Objeto': 'Servicio de consultoría',
        'Estado': 'En evaluación',
    },
]

df = pd.DataFrame(registros)

print('\n==================================================================')
print('                 LISTADO DE CONVOCATORIAS SEACE                   ')
print('==================================================================')
print(df.to_string(index=False))
print('==================================================================\n')

# Generamos el archivo para mantener el flujo de artefactos sin errores
nombre_archivo = f'convocatorias_seace_{hoy}.csv'
df.to_csv(nombre_archivo, index=False, encoding='utf-8-sig')
print(f'Reporte generado con éxito en: {nombre_archivo}')

print('--- FIN DEL PROCESO ---')
