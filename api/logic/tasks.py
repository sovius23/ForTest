from artdate.celery import app
from random import randint


@app.task
def mailing_list():
    print("qqqqqqqqqqqqqqqqqqqqqwwwwwwwwwwwwwwwwwwwwwweeeeeeeeeeeeeeeeeeeeeeeeee")
    return randint(0, 10)
