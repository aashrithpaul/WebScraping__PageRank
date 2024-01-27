import sqlite3
import time

# start = time.time()

conn = sqlite3.connect('page_rank.sqlite')
cur =  conn.cursor()

cur.execute(
    '''SELECT DISTINCT from_id
    FROM connections'''
)

fromIds = list()
for row in cur:
    fromIds.append(row[0])

toIds = list()
connections = list()

cur.execute(
    '''SELECT DISTINCT from_id, to_id 
    FROM connections'''
)
for row in cur:
    from_id, to_id = row[0], row[1]
    if to_id not in fromIds: continue
    if from_id == to_id: continue
    if from_id not in fromIds: continue
    if to_id not in toIds:
        toIds.append(to_id)
    connections.append(row)

prevRanks = dict()
for id in fromIds:
    cur.execute(
        '''SELECT new_rank 
        FROM webpages
        WHERE id = ?''', (id,)
    )
    for row in cur: prevRanks[id] = row[0]

count = int(input("How many iterations: "))
if count < 1: 
    print("exiting program...")
    quit()

if len(prevRanks) < 1:
    print("no data to rank. Exiting program...")
    quit()

for i in range(count):
    nextRanks = dict()

    total = 0
    for (id, oldRank) in prevRanks.items():
        nextRanks[id] = 0
        total += oldRank
    for (id, oldRank) in prevRanks.items():
        outIds = list()
        for (from_id, to_id) in connections:
            if from_id != id: continue
            if to_id not in toIds: continue
            outIds.append(to_id)
        
        if len(outIds) < 1: continue
        amt = oldRank / len(outIds)
    
        for el in outIds:
            nextRanks[el] = nextRanks[el] + amt
    
    newTotal = 0
    for id, newRank in nextRanks.items():
        newTotal += newRank
    
    evap = (total - newTotal) / len(nextRanks)
    for id in nextRanks:
        nextRanks[id] += evap
    
    prevRanks = nextRanks

cur.execute(
    '''UPDATE webpages
    SET old_rank = new_rank'''
)

for id, rank in nextRanks.items():
    cur.execute(
        '''UPDATE webpages
        SET new_rank = ?
        WHERE id = ?''', (rank, id)
    )

conn.commit()
    
# end = time.time()
# print((end - start)/count, end-start)
    
cur.close()




