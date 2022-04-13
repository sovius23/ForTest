from artdate.celery import app
from random import randint


@app.task
def debug_task():
    print("qqqqqqqqqqqqqqqqqqqqqwwwwwwwwwwwwwwwwwwwwwweeeeeeeeeeeeeeeeeeeeeeeeee")
    return randint(0, 10)
