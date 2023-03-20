import psycopg2
from configparser import ConfigParser
from os import listdir


def db_cur():
    try:
        # get db parameters
        params = config()
        # connect to db
        conn = psycopg2.connect(**params)
        # return db cursor
        cur = conn.cursor()
        return cur
    except (Exception, psycopg2.DatabaseError) as error:
        print('Connection to DB failed. Error message:')
        print(error)
        quit()

def create_tables():
    cur = db_cur()
    if not check_tables():
        for table in listdir('./db_model'):
            with open(f'./db_model/{table}')
                cur.execute(table.read())       
        if check_tables():
            print('DB tables were successfully created.')
        else:
            print('Failed to create DB tables.')
    else:
        print('Connected to DB with all needed tables.')
            
def check_tables():
    cur = db_cur()
    if set(cur.execute('SELECT * FROM information_schema.tables')) == set(listdir('./db_model')): 
        return True
    else:
        return False

def config(filename='database.ini', section='postgresql'):
    # parse db data
    parser = ConfigParser()
    parser.read(filename)
    # get section
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    
    return db

# check tables
if __name__ == '__main__':
    check_tables()