import sys
sys.path.append('../Lotto_scrapper')

from data_parser import scrap_results
from connect import db_cur


##############################################################################################
# url for updates
# lotto https://www.lotto.pl/lotto/wyniki-i-wygrane/date,2022-09-17,300
# multi-multi https://www.lotto.pl/multi-multi/wyniki-i-wygrane/date,2022-09-18,300
# super-szansa https://www.lotto.pl/super-szansa/wyniki-i-wygrane/date,2022-09-18,300
# ekstra-pensja https://www.lotto.pl/ekstra-pensja/wyniki-i-wygrane/date,2022-09-18,300
# eurojackpot https://www.lotto.pl/eurojackpot/wyniki-i-wygrane/date,2022-09-16,300
# mini-lotto https://www.lotto.pl/mini-lotto/wyniki-i-wygrane/date,2022-09-18,300
# kaskada https://www.lotto.pl/kaskada/wyniki-i-wygrane/date,2022-09-18,300
##############################################################################################

def check_missing_ids(game):
    db_ids = [0]
    cur = db_cur()
    for id in cur.execute('SELECT id FROM %s' % game.replace('-','')):
        db_ids.append(id[0])
    missing_ids = [x for x in range(db_ids[0], db_ids[-1]+1) if x not in db_ids]
    return missing_ids

def update_queue():
    cur = db_cur()
    update_last()   # this func should provide last records from lottery    
    games = ['lotto', 'multi-multi', 'super-szansa', 'ekstra-pensja', 'eurojackpot', 'mini-lotto', 'kaskada']
    for game in games:
        missing_ids = check_missing_ids(game)
        if missing_ids == []: # if there are no missing records, go to next game
            continue
        last_loop = None
        while last_loop != missing_ids and len(missing_ids) != 0:
            last_loop = missing_ids
            last_date = str(cur.execute('SELECT date FROM %s WHERE id = %d' % (game.replace('-',''), missing_ids[-1]+1)).fetchone()[0])
            scrap_results(f"https://www.lotto.pl/{game}/wyniki-i-wygrane/date,{last_date[0:4]}-{last_date[4:6]}-{last_date[6:8]},300")
            missing_ids = check_missing_ids(game)
        print(f'UPDATER - update_queue - {game} has {len(missing_ids)} missing records.')
    print('UPDATER - update_queue - ended.')
 
def update_last(): # getting last records for all games
    url = "https://www.lotto.pl/wyniki"
    scrap_results(url)