name: SEACE Scraper Automatico

on:
  workflow_dispatch: # Permite ejecutarlo manualmente cuando quieras
  schedule:
    - cron: '0 8 * * *' # Se ejecutará automáticamente todos los días a las 8:00 a.m.

jobs:
  run-scraper:
    runs-on: ubuntu-latest
    steps:
      - name: Clonar repositorio
        uses: actions/checkout@v4

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.10'

      - name: Instalar dependencias
        run: |
          pip install requests beautifulsoup4 pandas
          # Agrega aquí más librerías si tu código usa otras (por ejemplo, selenium, etc.)

      - name: Ejecutar el script
        run: python scraper.py
