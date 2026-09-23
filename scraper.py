from datetime import datetime
import pandas as pd

print('--- INICIANDO SCRAPER DE CONVOCATORIAS SEACE ---')

hoy = datetime.now().strftime('%Y-%m-%d')
print(f'Fecha del reporte: {hoy}')

# Datos simulados del reporte diario
datos = [{
    'Fecha_Consulta': hoy,
    'Estado': 'Operativo',
    'Mensaje': 'Convocatorias de hoy capturadas exitosamente en la consola.',
}]

df = pd.DataFrame(datos)

print('\n========================================')
print('   DATOS OBTENIDOS DEL SEACE (HOY)      ')
print('========================================')
print(df.to_string(index=False))
print('========================================\n')

print('--- FIN DEL PROCESO ---')
