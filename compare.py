import sqlite3 as sql 
import re
import os

def findListingsToCompare(config, db) :
  listings = dict()
  c = db.cursor()
  query = '''SELECT DISTINCT owner FROM listings'''
  users = c.execute(query).fetchall()
  print("[I] Total {0} distint owner of files ".format(len(users)))
  # Now for each of these students fetch their files.
  for user in users :
    query = '''SELECT name, root, size FROM listings WHERE owner=? 
              ORDER BY owner DESC '''
    files = c.execute(query, (user)).fetchall()
    listings[user] = files 
  newListings = filterListing(config, listings)
  oldNum = sum([len(i) for i in listings.itervalues()])
  newNum = sum([len(i) for i in newListings.itervalues()])
  print("[I] Total {0} files filtered.".format(oldNum - newNum))
  return newListings 

def filterListing(config, listings) :
  max_size = int(config.get('filter', 'max_size'))
  if max_size == -1 :
    max_size = 10000000
  else :
    max_size = max_size*1024
  regex = config.get('filter', 'ignore_regex')
  pat = re.compile(regex)
  newListings = dict()
  for user in listings :
    newFiles = list()
    files = listings[user]
    for file in files :
      name, root, size = file 
      filePath = os.path.join(root, name)
      fileSize = int(size)
      with open(filePath, "r") as f :
        txt = f.read()
      if pat.search(txt) or size > max_size : 
        continue 
      else :
        newFiles.append(file)
    newListings[user] = newFiles
  return newListings


def compare(config, db) :
  listings = findListingsToCompare(config, db)
