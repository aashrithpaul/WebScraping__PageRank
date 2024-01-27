# This code is Licensed.
# Please read LICENSE document.

# The original code has been slightly modified
# to work with my DB

import sqlite3

conn = sqlite3.connect('page_rank.sqlite')
cur = conn.cursor()

print("Creating JSON output: prankJSON.js...")
howmany = int(input("How many nodes? "))

cur.execute(
    '''SELECT COUNT(from_id) AS inbound, old_rank, new_rank, id, url 
    FROM webpages
    JOIN connections 
        ON webpages.id = connections.to_id
    WHERE html IS NOT NULL AND ERROR IS NULL
    GROUP BY id 
    ORDER BY id,inbound'''
    )

fhand = open('visualization/prankJSON.js','w')
nodes = list()
maxrank = None
minrank = None
for row in cur :
    nodes.append(row)
    rank = row[2]
    if maxrank is None or maxrank < rank: maxrank = rank
    if minrank is None or minrank > rank : minrank = rank
    if len(nodes) > howmany : break

if maxrank == minrank or maxrank is None or minrank is None:
    print("Error - please run pagerank.py to compute page rank")
    quit()

fhand.write('prankJSON = {"nodes":[\n')
count = 0
map = dict()
ranks = dict()
for row in nodes :
    if count > 0 : fhand.write(',\n')
    # print row
    rank = row[2]
    rank = 19 * ( (rank - minrank) / (maxrank - minrank) ) 
    fhand.write('{'+'"weight":'+str(row[0])+',"rank":'+str(rank)+',')
    fhand.write(' "id":'+str(row[3])+', "url":"'+row[4]+'"}')
    map[row[3]] = count
    ranks[row[3]] = rank
    count = count + 1
fhand.write('],\n')

cur.execute(
    '''SELECT DISTINCT from_id, to_id FROM connections'''
    )

fhand.write('"links":[\n')

count = 0
for row in cur :
    # print row
    if row[0] not in map or row[1] not in map : continue
    if count > 0 : fhand.write(',\n')
    rank = ranks[row[0]]
    srank = 19 * ( (rank - minrank) / (maxrank - minrank) ) 
    fhand.write('{"source":'+str(map[row[0]])+',"target":'+str(map[row[1]])+',"value":3}')
    count = count + 1
fhand.write(']};')
fhand.close()
cur.close()

print("Open webapp.html in a browser to view the visualization")
