import sqlite3

conn = sqlite3.connect('page_rank.sqlite')
cur =  conn.cursor()

cur.execute(
    '''UPDATE webpages
    SET old_rank = 0.0, new_rank = 1.0'''
)
conn.commit()
cur.close()