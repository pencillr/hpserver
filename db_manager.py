import sqlite3

Writer = 0
Reader = 0

def init_db(dbname):
    conn = sqlite3.connect(dbname, isolation_level=None)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE WIZ(
        ID INT PRIMARY KEY,
        USER TEXT,
        HEALTH INT,
        LUMOS INT,
        STUPOR INT,
        ALOHO INT
    )''')
    cursor.execute('''CREATE TABLE CAST(
        ID INT,
        CASTD TEXT,
        TIME INT
    )''')
    conn.commit()
    conn.close()
    start_db_agent(dbname)


def start_db_agent(dbname):
    global Writer
    global Reader
    Writer = sqlite3.connect(dbname, isolation_level=None)
    Writer.execute('pragma journal_mode=wal;')
    Reader = sqlite3.connect(dbname, isolation_level=None)
    Reader.execute('pragma journal_mode=wal;')

def get_writer():
    return Writer;

def get_writer():
    return Reader;

def post_cast(id, spell, time):
    pass

def fetch_cast(id, time=0):
    if Reader:
        c = Reader.cursor()
        c.execute("SELECT CASTD FROM CAST where ID=?;", (id,))
        row = c.fetchone()
        print row[0]

def modify_health(mod):
    pass

def is_dead(id):
    pass

def store_cast(id, spell, timeframe):
    c = Writer.cursor()
    c.execute("INSERT INTO CAST VALUES (?,?,?);", (id,spell,timeframe))

def fetch_cast(id):
    c = Reader.cursor()
    c.execute("SELECT CASTD FROM CAST where ID=?;", (id,))
    row = c.fetchone()
    return row[0]

def register_wiz(id, name, health=20, l=0, s=0, a=0,):
    # handle if returns registered user!
    c = Writer.cursor()
    t = (id, name, health, l, s, a)
    c.execute("INSERT INTO WIZ VALUES (?,?,?,?,?,?);", t)
    return t

def fetch_wiz(id):
    #if Reader:
    c = Reader.cursor()
    c.execute("SELECT USER FROM WIZ where ID=?;", (id,))
    row = c.fetchone()
    return row[0]

def close_all():
    Writer.close()
    Reader.close()

if __name__ == '__main__':
    #init_db("testDB.db")
    start_db_agent("testDB.db")
    store_cast(4, 'aloho', 123456)
    fetch_cast(4)
    register_wiz(3, 'david', 20, 1, 0, 1)
    print(fetch_wiz(3))
    close_all()
