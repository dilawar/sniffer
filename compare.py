import sqlite3 as sql 
import re
import os

def findListingsToCompare(config, db) :
  listings = dict()
  c = db.cursor()
  query = '''SELECT DISTINCT owner FROM listings '''
  users = c.execute(query).fetchall()
  print("[I] Total {0} distint owner of files ".format(len(users)))
  # Now for each of these students fetch their files.
  for user in users :
    query = '''SELECT name, root, size FROM listings WHERE owner=? 
              ORDER BY name DESC '''
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
  totalComparisions = 0
  listings = findListingsToCompare(config, db)
  # Make a copy for local modification.
  tempListings = listings.copy()

  # for each user.
  for userA in listings :
    print("Comparing for userA : {0}".format(userA))
    userComparisons = 0
    filesA = listings[userA]
    if len(filesA) == 0 :
      print("[W] No files for user")
    # Delete this user from dictionary
    oldLength = sum([len(x) for x in tempListings.values()])
    tempListings.pop(userA, None)
    newLength = sum([len(x) for x in tempListings.values()])
    print oldLength, newLength, len(filesA)
    assert oldLength == newLength + len(filesA), "More values are deleted"

    # compare each of his files with all other files.
    for fileA in filesA :
      nameA, rootA, sizeA = fileA
      for userB in tempListings :
        filesB = tempListings[userB]
        for fileB in filesB :
          nameB, rootB, sizeB = fileB
          # compare files here.
          compareTwoFiles(config, db, userA, fileA, userB, fileB)
          userComparisons += 1
    totalComparisions += userComparisons 
    print("[II] For user {0} : {1} comparisions".format(userA[0], userComparisons))
  print("[I] Total {0} comparisions".format(totalComparisions))


def compareTwoFiles(config, db, userA, fileA, userB, fileB) :
  nameA, rootA, sizeA = fileA 
  nameB, rootB, sizeB = fileB 
  print("Comparing {0} : {1}".format(userA, userB))
