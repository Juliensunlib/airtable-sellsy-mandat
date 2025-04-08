name: Run Mandate Request Script

on:
  schedule:
    - cron: '*/10 * * * *'  # Exécution toutes les 10 minutes
  workflow_dispatch:  # Permet l'exécution manuelle

jobs:
  run-script:
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
        
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
          
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests python-dotenv
          
      - name: Run script
        env:
          AIRTABLE_API_KEY: ${{ secrets.AIRTABLE_API_KEY }}
          AIRTABLE_BASE_ID: ${{ secrets.AIRTABLE_BASE_ID }}
          AIRTABLE_TABLE_NAME: ${{ secrets.AIRTABLE_TABLE_NAME }}
          AIRTABLE_INSTALLERS_BASE_ID: ${{ secrets.AIRTABLE_INSTALLERS_BASE_ID }}
          AIRTABLE_INSTALLATEURS_TABLE: ${{ secrets.AIRTABLE_INSTALLATEURS_TABLE }}
          SELLSY_CONSUMER_TOKEN: ${{ secrets.SELLSY_CONSUMER_TOKEN }}
          SELLSY_CONSUMER_SECRET: ${{ secrets.SELLSY_CONSUMER_SECRET }}
          SELLSY_USER_TOKEN: ${{ secrets.SELLSY_USER_TOKEN }}
          SELLSY_USER_SECRET: ${{ secrets.SELLSY_USER_SECRET }}
          GOCARDLESS_DIRECT_LINK: ${{ secrets.GOCARDLESS_DIRECT_LINK }}
          CHECK_INTERVAL: "300"
          LOG_DIR: "logs"
        run: python main.py
        
      - name: Upload logs
        uses: actions/upload-artifact@v3
        if: always()  # Exécuter même en cas d'échec
        with:
          name: execution-logs-${{ github.run_id }}
          path: logs/
          retention-days: 7  # Conserve les logs pendant 7 jours
