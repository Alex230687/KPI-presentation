from KPI.celery import app
from data_load_modul import complex_data_load_modul


@app.task
def beat_update_database_data():
    complex_data_load_modul()
