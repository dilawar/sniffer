import sqlite3 as sql 
import os, errno
import time
import algorithm 
import sys
import re

inMemDb = sql.connect(":memory:")
dbName = 'sniffer.sqlite3'

def buildListingDb(config) :
    global dbName
    dbPath = config.get('database', 'path')
    iscomparing = True
    print("[I] Creating db in {0}".format(dbPath))
    try :
        os.makedirs(dbPath) 
    except OSError as exception :
        if exception.errno != errno.EEXIST :
            raise 
    if dbName != ":memory:" :
      dbfile = os.path.join(dbPath, dbName)
      if os.path.exists(dbfile) :
        if iscomparing: 
          os.rename(dbfile, dbfile+time.strftime("%Y%m%d%H%M%S"))
        else :
          pass 
      db = sql.connect(dbfile)
    else :
      db = sql.connect(dbName)

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
              , owner VARCHAR 
              , root VARCHAR NOT NULL 
              , type VARCHAR
              , size INT NOT NULL 
              , lines INT 
              , status VARCHAR
              , PRIMARY KEY(root, name))'''
    c.execute(query)
  
    query = '''CREATE TABLE IF NOT EXISTS match (
              userA VARCHAR NOT NULL 
              , fileA VARCHAR NOT NULL
              , userB VARCHAR NOT NULL
              , fileB VARCHAR NOT NULL 
              , match REAL NOT NULL 
              , algorithm VARCHAR 
              , result VARCHAR
              , PRIMARY KEY(fileA, fileB, algorithm))
              '''
    c.execute(query)
  
    c.execute('DROP TABLE IF EXISTS summary')
    
    query = '''CREATE TABLE IF NOT EXISTS summary (
      userA VARCHAR NOT NULL
      , userB VARCHAR NOT NULL 
      , num_matches INT default '1'
      , avg_index REAL default '0.0'
      , PRIMARY KEY(userA, userB) 
      ) '''
    c.execute(query)
    db.commit()
    return db


def populateDB(config, db) :
    c = db.cursor()
    dir = config.get('source', 'dir')
    extension = config.get('source', 'extension')
    if len(extension.strip()) == 0 :
        regex = ".*"
    else:
        extension = [x.strip() for x in extension.split(',')]
        regex = r".*?\.({})$".format('|'.join(extension))
    pat = re.compile(regex, re.IGNORECASE)
    if not os.path.exists(dir) :
      print("[E] source dir does not exists. Check config file.")
      sys.exit(0)
    countFile = 0
    for root, dirs, files in os.walk(dir) :
      for file in files :
        if pat.match(file) :
          countFile += 1
          fileName = file 
          filePath = os.path.join(root, file)
          if not os.path.exists(filePath) :
            print("[W] Something weired has happened. {0} does not \
                exists".format(filePath))
            return 
          sizeOfFile = os.path.getsize(filePath)
          owner = root.replace(dir, "")
          owner = owner.strip("/")
          owner = owner.split("/")[0]
          query = '''INSERT INTO listings (name, root, size, type, owner)
              VALUES (?, ?, ?, ?, ?)'''
          c.execute(query, (fileName, root, sizeOfFile, regex, owner))
    db.commit()
    print("[I] Total {0} programs".format(countFile))
    return db 

def writeContent(config, db):
    global dbName
    path = config.get('database', 'path')
    srcdir = config.get('source', 'dir')
    srcdir = srcdir.strip("/")
    srcdir += "/"
    name = dbName
    dbPath = os.path.join(path, dbName)
    db = sql.connect(dbPath)
    c = db.cursor()
    serverity = ["mild", "moderate", "high", "veryhigh", "identical"]
    for s in serverity :
      print("Fetching cases with serverity : {0}".format(s))
      query = '''SELECT userA, userB, fileA, fileB, match FROM match WHERE result=?'''
      with open(os.path.join(path, s+"_serverity.csv"), "w") as f :
        rows = c.execute(query, (s,)).fetchall()
        for row in rows :
          userA, userB, fileA, fileB, match = row 
          prefix = algorithm.commonPrefix(fileA, dbPath)
          outLevel = len(path.replace(prefix, "")) - 1
          prefixFile = ""
          for p in xrange(1, outLevel) :
            prefixFile += "../"
          fileA = prefixFile+fileA.replace(prefix, "")
          fileB = prefixFile+fileB.replace(prefix, "")
  
          #fileA = fileA.replace(srcdir, "").strip("/")
          #fileB = fileB.replace(srcdir, "").strip("/")
          f.write("\"{0}\",\"{1}\",\"{2}\"\n".format(match,fileA, fileB))
    generateSummary(config, db)

def generateSummary(config, db) :
  #global inMemDb
  #table_to_copy = "match" 
  #query = "".join(line for line in db.iterdump())
  #inMemDb.executescript(query)   # copies the table match.
  c = db.cursor()
  
  query = '''SELECT DISTINCT userA FROM match'''
  print("[DB] Fetching distinct first users ..."),
  userAs = c.execute(query).fetchall()
  print("done")
  
  print("[DB] Fetching distinct second users ..."),
  query = '''SELECT DISTINCT userB FROM match'''
  userBs = c.execute(query).fetchall()
  print("done")

  print("[DB] Populating table summary ... "),
  query = '''SELECT fileA, fileB, match FROM match WHERE userA=? AND
      userB=?'''
  nodes = list()
  summary = dict()
  for userA in userAs :
    userA = userA[0]
    for userB in userBs :
      userB = userB[0]
      num_matches = 0
      avg_index = 0.0
      rows = c.execute(query, (userA, userB,)).fetchall()
      for row in rows :
        fileA, fileB, match = row 
        avg_index = (match + num_matches * avg_index) / (num_matches+1)
        num_matches += 1
      if num_matches > 0 :
        summary[(userA, userB)] = (num_matches, avg_index)
  print("done")
  # Here is summary.
  for k in summary :
    userA, userB = k 
    num_matches, avg_index = summary[k]
    c.execute('''INSERT OR IGNORE INTO summary (userA, userB, num_matches
      , avg_index) VALUES (?, ?, ?, ?)''', (userA, userB, num_matches,
        avg_index,))
  db.commit()

def genrateDOT(config, db) : 
   #global inMemDb
   users = set()
   dotLines = []
   c = db.cursor()
   print("[STEP] %s" % "Generating graphs from summary ..."),
   summary = c.execute('SELECT * FROM summary').fetchall()
   for s in summary:
       userA, userB, num_matches, avg = s
       users.add(userA)
       users.add(userB)
       penwidth = (avg+0.5)*(avg+0.5)
       if avg > 0.0 :
         color = "#ffff00"
       if avg > 0.5 :
         color = "#ffa000" 
       if avg > 0.6 :
         color = "blue"
       if avg > 0.7 :
         color = "red"
       line = ("\n\t\"{0}\" -- \"{1}\" [penwidth={2} color=\"{4}\""+
             " label=\"{3}\" fontsize=7.0];").format(userA, userB, penwidth
                 , num_matches, color)
       dotLines.append((avg, line)) 
    
   [writeToGraphviz(config, x, users, dotLines, standAlone=True) 
            for x in ["summary", "convicted", "accused"]]


def writeToGraphviz(config, filename, users, dotLines, standAlone):
    global dbName
    dbPath = config.get("database", "path")
    path = os.path.join(dbPath, filename+".sh")
    with open(path, "w") as f:
        header = "#!/bin/bash\n"
        header += "\n# Bash script to generate graph\n"
        header += "\ngraph=$(cat <<GRAPHEND"
        header += "\ngraph match { \n\tnode[style=filled shape=point label= \"\"];"
        header += "\n\tsize=\"40.0,40.0\";"
        header += "\n\tfontsize=10.0;";
        header += "\n\toverlap=false ;\n\tspline=true; \n\tnodesep=4.0;\n\n"
        f.write(header)
        # Write names of all students as nodes.
        for user in users:
            f.write("\"{}\"\n".format(user))
        if "convicted" in filename:
            writeLines(f, dotLines, 0.60)
        elif "accused" in filename:
            writeLines(f, dotLines, 0.60)
        elif "summary" in filename:
            writeLines(f, dotLines, 0.10)
        else: pass
        endLine = "\n}\n"
        endLine += "GRAPHEND\n"
        endLine += ")\n"
        f.write(endLine)
        endLine = "echo $graph > .temp.dot \n"
        endLine += "neato -Tps -o{0} .temp.dot \n"
        endLine += "rm -f .temp.dot\n"
        f.write(endLine.format(filename+".ps"))

def writeLines(fileH, lines, threshold):
    """ Write given lines to file when avg is greater than threshold """
    for avg, line in lines:
        if avg >= threshold:
            fileH.write(line)
        else: pass
