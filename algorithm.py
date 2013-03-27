import sqlite3 as sql 
import os
import difflib

def formatText(txt, lang) :
  return txt
  
def compareAndReturnResult(textA, textB, algorithm="subsequence" ) :
  if algorithm == "subsequence" :
    wordsA = textA.split()
    wordsB = textB.split()
    if len(wordsA) < 4 or len(wordsB) < 4 :
      return "\t|- [W] Less than four words", 0

    lR = float(len(wordsA)) / len(wordsB)
    if lR > 1.0 :
      lR = 1/lR 
    if lR < 0.2 :
      print("\t|- [W] Files differ in size by a factor of {0}".format(lR))
      return "Files differ in sizes", lR

    # check intersection of keywords 
    setA = set(wordsA)
    setB = set(wordsB)
      
    intersectionSize =  float(len(setA.intersection(setB))) / min(len(setA), len(setB)) 
    if intersectionSize < 0.35 :
      print("\t|- [W] Intersection of keywords are very small : {0}"\
          .format(intersectionSize))
      return "Small keyword intersection", intersectionSize 

    # if intersection of these two set is very small then there is little
    # maching in these two files. 
    s = difflib.SequenceMatcher(None, textA, textB)
    with file("set_sub.csv", "a") as f :
      f.write("{0}, {1}\n".format(s.ratio(), intersectionSize))
    return "difflib", s.ratio() 

  else :
    print("[E] Algorithm not specified")
    return 
