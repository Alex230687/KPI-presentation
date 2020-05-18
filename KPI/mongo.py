import mongoengine


mongoengine.connect('logdb')


class FormQueryLog(mongoengine.Document):
    """MongoDB model for logs."""
    user_id = mongoengine.IntField()
    log_time = mongoengine.DateTimeField()
    form_year = mongoengine.IntField()
    form_branch = mongoengine.IntField()
    form_forecast = mongoengine.IntField()
    form_totals = mongoengine.IntField()
