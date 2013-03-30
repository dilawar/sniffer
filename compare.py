import sqlite3 as sql 
import re
import os
import algorithm
import database

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
    max_size = pow(2,32)
  else :
    max_size = max_size*1024
  
  min_words = int(config.get('filter', 'min_words'))
  max_words = int(config.get('filter', 'max_words'))
  regex = config.get('filter', 'regex')
  regex_flags = config.get('filter', 'regex_flags')
  if max_words == -1 :
    max_words = pow(2,32)
  ignorecase = False 
  dotall = False 
  if regex_flags.upper().find("IGNORECASE") != -1 :
    ignorecase = True
  if regex_flags.upper().find("DOTALL") != -1 :
    dotall = True 

  if dotall and ignorecase :
    pat = re.compile(regex, re.IGNORECASE | re.DOTALL)
  elif dotall and not ignorecase :
    pat = re.compile(regex, re.DOTALL)
  elif not dotall and ignorecase :
    pat = re.compile(regex, re.IGNORECASE)
  elif dotall and not ignorecase :
    pat = re.compile(regex, re.DOTALL)
  elif not dotall and not ignorecase :
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
      if size > max_size :
        print('[FILTER] Ignored due to large size : {0}'.format(name))
      elif len(txt.split()) < min_words :
        print('[FILTER] Ignored due to few words : {0}'.format(name))
      elif len(txt.split()) > max_words :
        print('[FILTER] Ignored due to too-many words : {0}'.format(name))
      elif pat.search(txt) : 
        print("[FILTER] Ignoring because regex is found : {0}.".format(name))
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
      (userA, fileA, userB, fileB, match, algorithm, result) 
      VALUES 
      (?, ?, ?, ?, ?, ?, ?)'''
  c = db.cursor()

  # for each user.
  i = 0
  totalUsers = len(listings)
  for userA in listings :
    i += 1
    print("\n\n== Comparing for userA : {0}".format(userA[0]))
    print("[I] Processing {0} out of {1}".format(i, totalUsers))
    userComparisons = 0
    filesA = listings[userA]
    if len(filesA) == 0 :
      print("[W] No files for user")
    # Delete this user from dictionary
    oldLength = sum([len(x) for x in tempListings.values()])
    tempListings.pop(userA, None)
    newLength = sum([len(x) for x in tempListings.values()])
    #print oldLength, newLength, len(filesA)
    assert oldLength == newLength + len(filesA), "More values are deleted"

    # compare each of his files with all other files.
    for fileA in filesA :
      nameA, rootA, sizeA = fileA
      for userB in tempListings :
        filesB = tempListings[userB]
        for fileB in filesB :
          nameB, rootB, sizeB = fileB
          # compare files here.
          msg = " # Processing user no {0} out of total {1} ".format(i, totalUsers)
          res, ratio = compareTwoFiles(config, db, userA, fileA, userB, fileB, msg)
          if res == "difflib" :
            result = ""
            if ratio > 0.3 :
              if ratio > 0.35 :
                result = "mild"
              if ratio > 0.45 :
                result = "moderate"
              if ratio > 0.55 :
                result = "high" 
              if ratio > 0.65 :
                result = "veryhigh" 
              if ratio > 0.80 :
                result = "identical"
              filePathA = os.path.join(rootA, nameA)
              filePathB = os.path.join(rootB, nameB)
              print("\n[Match] : {2} {3} \n\t|- {0} <--> {1}".format(userA[0]+" : "+nameA,
                userB[0]+" : "+nameB , ratio, msg))
              c.execute(query, (userA[0], filePathA, userB[0], filePathB, ratio,
                res, result))
          userComparisons += 1
    totalComparisions += userComparisons 
    print("[II] For user {0} : {1} comparisions".format(userA[0], userComparisons))
    db.commit()
  print("[I] Total {0} comparisions".format(totalComparisions))

def compareTwoFiles(config, db, userA, fileA, userB, fileB, msg) :
  language = config.get('source', 'language')
  algorithm = config.get('algorithm', 'name')
  textA = getText(fileA, language)
  textB = getText(fileB, language)
  textA = algorithm.formatText(textA, language)
  textB = algorithm.formatText(textB, language)
  return algorithm.compareAndReturnResult(textA, textB, algorithm=algorithm)

def getText(file, language) :
  name, root, size = file 
  filePath = os.path.join(root, name)
  if language != "pdf" : 
    with open(filePath, "r") as f :
      txt = f.read()
    return txt
  else :
    return filePath

