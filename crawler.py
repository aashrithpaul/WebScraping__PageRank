from bs4 import BeautifulSoup
import urllib.parse, urllib.request, urllib.error
import sqlite3
import time
import ssl
import random

# Ignore website certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('page_rank.sqlite')
cur = conn.cursor()

cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS webpages (
    id INTEGER PRIMARY KEY NOT NULL,
    url TEXT UNIQUE,
    html TEXT,
    error INTEGER,
    old_rank REAL,
    new_rank REAL
    )'''
)

cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS connections (
    from_id INTEGER,
    to_id INTEGER,
    UNIQUE (from_id, to_id)
    )'''
)

cur.execute(
    '''
    CREATE TABLE IF NOT EXISTS hostnames (
    url TEXT UNIQUE
    )'''
)

cur.execute(
    '''
    SELECT id, url 
    FROM webpages 
    WHERE html IS NULL
        AND error IS NULL
    ORDER BY RANDOM()
    LIMIT 1
    '''
)

row = cur.fetchone()

if row is not None:
    print("restarting existing crawl...")
else:
    start_url = input("Enter web url and/or press enter:")
    if len(start_url) < 1: 
        start_url = 'http://www.dr-chuck.com/'
    
    if start_url.endswith('/'):
        start_url = start_url[:-1]
    host_name = start_url
    
    if start_url.endswith('.htm') or start_url.endswith('.html'):
        loc = start_url.rfind('/')
        host_name = start_url[:loc]
        
    
    if len(host_name) > 1:
        cur.execute('''
            INSERT OR IGNORE INTO hostnames (url) 
            VALUES (?)''', (host_name, ))
        
        cur.execute('''
            INSERT OR IGNORE INTO webpages (url, html, new_rank)
            VALUES (? , NULL, 1.0)''', (start_url, ))
        conn.commit()

cur.execute('''SELECT url FROM hostnames''')
host_names = list()
for row in cur:
    host_names.append(str(row[0]))

print(host_names)


count = int(input("enter the number of pages to crawl: "))
while count > -1:
    if count < 1:
        print("...exiting crawl")
        break
    count -= 1

    cur.execute('''
        SELECT id, url FROM webpages
        WHERE html IS NULL AND error IS NULL
        ORDER BY RANDOM()
        LIMIT 1''')

    try:
        row = cur.fetchone()
        from_id = row[0]
        url = row[1]
    except:
        print("no unretrieved html pages found")
        count = 0
        break

    print(from_id, url)

    cur.execute('''
        DELETE FROM connections 
        WHERE from_id = (?)''', (from_id, ))
    
    try:
        doc = urllib.request.urlopen(url, context = ctx)
        html = doc.read()
        if doc.getcode() != 200:
            print("Error on page: ", doc.getcode())
            cur.execute(
                '''UPDATE webpages
                SET error = ? 
                WHERE url = ?''', (doc.getcode(), url)
            )
        if doc.info().get_content_type() != 'text/html':
            print("Does not contain html/text data. Ignoring page...")
            cur.execute(
                '''UPDATE webpages
                SET error = -1 
                WHERE url = ?''', (url, ))
            conn.commit()
            continue

        print('('+str(len(html))+')')
        
        soup = BeautifulSoup(html, 'html.parser')

    except KeyboardInterrupt:
        print("interrupted by user...ending crawl")
        break 
    except:
        print("unble to retrieve or parse page")
        cur.execute(
            '''UPDATE webpages
            SET error = -1 
            WHERE url = ?''', (url, )
        )
        conn.commit()
        continue

    cur.execute(
        '''INSERT OR IGNORE INTO webpages (url, html, new_rank)
        VALUES (?, NULL, 1.0)''', (url, )
    )
    cur.execute(
        '''UPDATE webpages 
        SET html = ? 
        WHERE url = ?''', (memoryview(html), url)
    )
    conn.commit()

    tags = soup('a')
    total = 0
    start = time.time()
    for tag in tags:
        href = tag.get('href', None)
        if href is None: continue

        link = urllib.parse.urlparse(href)

        if len(link.scheme) < 1: 
            href = urllib.parse.urljoin(url, href)
        
        secIndex = href.find('#')
        if secIndex > 1: href = href[ : secIndex]

        if href.endswith('.png') or href.endswith('.jpg') or href.endswith('.gif') : continue

        if href.endswith('/') : href = href[:-1]
        
        if len(href) < 1 : continue

        found = False
        for name in host_names: 
            if href.startswith(name):
                found = True
                break
        if not found: continue

        cur.execute(
            '''INSERT OR IGNORE INTO webpages (url, error, new_rank)
            VALUES (?, NULL, 1.0)''', (href, )
        )
        total += 1
        conn.commit()

        cur.execute(
            '''SELECT id
            FROM webpages 
            WHERE url = ? LIMIT 1''', (href, )
        )
        try:
            row = cur.fetchone()
            to_id = row[0]
        except:
            print("Could not retrieve id")
            continue

        cur.execute(
            '''INSERT OR IGNORE INTO connections (from_id, to_id)
            VALUES (?, ?)''', (from_id, to_id)
        )

        time.sleep(random.randint(1,3))

    end = time.time()
    print(count, end-start)

cur.close()

        



    