import sqlite3 as sql 
import os, errno

def buildListingDb(config) :
  dbPath = config.get('database', 'path')
  dbName = config.get('database', 'name')
  
  try :
    os.makedirs(dbPath) 
  except OSError as exception :
    if exception.errno != errno.EEXIST :
      raise 
  db = sql.connect(os.path.join(dbPath, dbName))
  db = initializeDb(db)
  db = populateDB(config, db)
  return db

def initializeDb(db) :
  # It should be create every time.
  c = db.cursor()
  query = 'DROP TABLE IF EXISTS listings'
  c.execute(query)

  query = ''' CREATE TABLE listings (
            name VARCHAR NOT NULL 
            , path VARCHAR NOT NULL 
            , size INT NOT NULL 
            , lines INT 
            , status VARCHAR
            , PRIMARY KEY(path, name))'''
  c.execute(query)

  query = '''CREATE TABLE IF NOT EXISTS match (
            fileA VARCHAR NOT NULL
            , fileB VARCHAR NOT NULL 
            , match REAL NOT NULL 
            , algorithm VARCHAR NOT NULL
            , PRIMARY KEY(fileA, fileB, algorithm))
            '''
  c.execute(query)
  db.commit()
  return db


def populateDB(config, db) :
  import re
  dir = config.get('source', 'dir')
  regex = config.get('source', 'regex')
  if len(regex.strip()) == 0 :
    regex = ".*"
  pat = re.compile(regex, re.IGNORECASE)
  if not os.path.exists(dir) :
    print("[E] source dir does not exists. Check config file.")
    sys.exit(0)
  for root, dirs, files in os.walk(dir) :
    for file in files :
      if pat.match(file) :
        print file

    print files 
  return db 
