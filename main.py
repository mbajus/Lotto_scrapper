import sys, sched, time
from datetime import datetime, timedelta
sys.path.append('../Lotto_scrapper')
  
from connect import create_tables, check_tables
from scrapper.data_parser import scrap_results
from connect import db_cur

##############################################################################################
# url for updates
# lotto https://www.lotto.pl/lotto/wyniki-i-wygrane/date,2022-09-17,300
# multi-multi https://www.lotto.pl/multi-multi/wyniki-i-wygrane/date,2022-09-18,300
# ekstra-pensja https://www.lotto.pl/ekstra-pensja/wyniki-i-wygrane/date,2022-09-18,300
# eurojackpot https://www.lotto.pl/eurojackpot/wyniki-i-wygrane/date,2022-09-16,300
# mini-lotto https://www.lotto.pl/mini-lotto/wyniki-i-wygrane/date,2022-09-18,300
# kaskada https://www.lotto.pl/kaskada/wyniki-i-wygrane/date,2022-09-18,300
##############################################################################################
# There are two way to scrap:
#   a) last results for all games, url = https://www.lotto.pl/wyniki
#   b) for each game with max ~300 records at once, with url from above. Given date is the latest for the records.
#
# Initialy this app will start with collecting last results (a), and then check for missing
# IDs in each game and then will try to collect missing data.
# A schudeler will check for new records.
##############################################################################################

def check_db():
    #create tables if doesnt exists
    create_tables()
    #check if created or exists
    if check_tables():
        print('DB ok!')
    else:
        print('Error - tables doesnt exists!')
        exit


def check_missing_ids(table):
    #this query retrives the last date of highest ID, for which previous ID is missing
    query = f'''
        SELECT t1.date
        FROM {table} AS t1
        LEFT JOIN {table} AS t2 ON t1.id = t2.id + 1
        WHERE t2.id IS NULL AND t1.id > 1
        ORDER BY t1.id DESC
        LIMIT 1
    '''
    #get cursor and fetch
    cur = db_cur()
    cur.execute(query)
    date = cur.fetchone()
    cur.close()
    #return date as a tuple, if there is no missing id the date will be empty
    return date[0] if date else None

def update_queue():
    #check for each game
    for game in ('lotto', 'multimulti', 'ekstrapensja', 'eurojackpot', 'minilotto', 'kaskada'):
        missingdate = check_missing_ids(game)
        while missingdate :
            date = str(missingdate)
            results = scrap_results(f"https://www.lotto.pl/{game}/wyniki-i-wygrane/date,{date[0:4]}-{date[4:6]}-{date[6:8]},300")
            cur = db_cur()
            results.insert_multiple_records(cur)
            missingdate = check_missing_ids(game)
            if date == str(missingdate):
                #skip scrapping, if driver gets banned, server is down or something..
                print(f'UPDATE for {game} - ended not successfully.')
                break
        print(f'UPDATE for {game} - ended successfully.')
    print('UPDATE - update_queue - ended.')
 
def update_last():
    # getting last records for all games
    url = "https://www.lotto.pl/wyniki"
    results = scrap_results(url)
    cur = db_cur()
    results.insert_multiple_records(cur)

#function to schedule the runs at the specified time
def schedule_run(scheduler, interval):
    now = datetime.now()
    next_run = now.replace(hour=interval.hour, minute=interval.minute, second=0, microsecond=0)
    if next_run <= now:
        next_run += timedelta(days=1) #schedule for next day 
    scheduler.enterabs(next_run.timestamp(), 1, update_queue, ())
    print("Next run scheduled for:", next_run)

def start_scheduler():
    #create and start the scheduler
    scheduler = sched.scheduler(time.time, time.sleep)

    #run times 14:30 and 22:40, after games are presented on web
    run_times = [
        datetime.now().replace(hour=14, minute=30, second=0, microsecond=0),
        datetime.now().replace(hour=22, minute=40, second=0, microsecond=0)
    ]

    #schedule the runs
    for run_time in run_times:
        schedule_run(scheduler, run_time)

    #start the scheduler
    scheduler.run()

if __name__ == "__main__":
    check_db()
    update_last()
    update_queue()
    start_scheduler()