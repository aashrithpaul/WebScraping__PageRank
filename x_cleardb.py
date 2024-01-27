import sqlite3

conn = sqlite3.connect('page_rank.sqlite')
cur = conn.cursor()

cur.executescript(
    '''
    DROP TABLE IF EXISTS webpages;
    DROP TABLE IF EXISTS connections;
    DROP TABLE IF EXISTS hostnames;'''
)

