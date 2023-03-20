from apscheduler.schedulers.blocking import BlockingScheduler
from connect import create_tables

def hourly_update():
    return

def last_update():
    return

def init_update():
    return


if __name__ == "__main__":
    create_tables()
    sched = BlockingScheduler(timezone='Europe/Warsaw')

    sched.add_job(hourly_update, 'interval', minutes=60, id='hourly_update')
    sched.add_job(last_update, 'cron', hour=22, minute=10, id='night_draw')
    sched.add_job(last_update, 'cron', hour=15, minute=10, id='afternoon_draw')