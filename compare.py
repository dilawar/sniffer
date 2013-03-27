import sqlite3 as sql 
import re
import os
import algorithm

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

  query = '''REPLACE INTO match 
      (fileA, fileB, match, algorithm, result) VALUES 
      (?, ?, ?, ?, ?)'''
  c = db.cursor()
  # for each user.
  i = 0
  totalUsers = len(listings)
  for userA in listings :
    i += 1
    print("[I] Processing {0} out of {1}".format(i, totalUsers))
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
          msg = "{0}/{1} : ".format(i, totalUsers)
          res, ratio = compareTwoFiles(config, db, userA, fileA, userB, fileB, msg)
          if res == "difflib" or res == "custom" :
            if ratio > 0.3 :
              filePathA = os.path.join(rootA, nameA)
              filePathB = os.path.join(rootB, nameB)
              print("\n[Match] : {2}\n\t|- {0} <--> {1}".format(userA[0]+" : "+nameA,
                userB[0]+" : "+nameB , ratio))
              c.execute(query, (filePathA, filePathB, ratio, res, ratio))
          userComparisons += 1
    totalComparisions += userComparisons 
    print("[II] For user {0} : {1} comparisions".format(userA[0], userComparisons))
    db.commit()
  print("[I] Total {0} comparisions".format(totalComparisions))


def compareTwoFiles(config, db, userA, fileA, userB, fileB, msg) :
  textA = getText(fileA)
  textB = getText(fileB)
  language = config.get('source', 'language')
  textA = algorithm.formatText(textA, language)
  textB = algorithm.formatText(textB, language)
  return algorithm.compareAndReturnResult(textA, textB, algorithm="subsequence")

def getText(file) :
  name, root, size = file 
  filePath = os.path.join(root, name)
  with open(filePath, "r") as f :
    txt = f.read()
  return txt
