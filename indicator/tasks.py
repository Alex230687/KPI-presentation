from KPI.celery import app
from KPI.mongo import FormQueryLog


@app.task
def write_form_query_log(data_dict):
    """Simple task that write users post form queries to MongoDB."""
    FormQueryLog(**data_dict).save()
