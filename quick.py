import re 

def subsequence(startA, s1, s2) :
  ''' returns list of tuples of indices (len, a1, b1) where len is the length of
  subsequence while a1 and b1 are starting index in first and second string
  respecitvely. 
  '''
  subsequences = list()
  aI = startA
  bI = 0 
  matchBegin = False
  matchEnd = False 
  while(aI < len(s1) and bI < len(s2)) :
    #if aI > len(s1) :
    #  print("A", aI, len(s1))
    #if bI > len(s2) :
    #  print("B", bI, len(s2))
    if s1[aI] == s2[bI] :
      matchBegin = True 
      matchEnd = False 
      aI += 1
      bI += 1
    else :
      if matchBegin :
        matchBegin = False 
        matchEnd = True 
      else :
        bI += 1 
    if not matchBegin and matchEnd :
      lenOfSubSeq = aI - startA 
      aI = startA
      if lenOfSubSeq > 0 :
        match = (lenOfSubSeq, startA, bI-lenOfSubSeq)
        subsequences.append(match)
  return subsequences

def quickMatch(textA, textB) :
  matchSequences = dict()
  loopLength = len(textA)
  for i in xrange(0, loopLength-1) :
    startA = i 
    endA = i
    subsequence(i, textA, textB)

if __name__ == "__main__" :
  import cProfile as profile 
  import string, random
  import time 
  text1 = "abcdefg"
  text2 = "xyababcdg"
  textA = "".join([random.choice(string.letters) for i in xrange(10000)])
  textB = "".join([random.choice(string.letters) for i in xrange(10000)])
  #print textA
  
  t1 = time.clock()
  quickMatch(textA, textB)
  print("A: ", time.clock() - t1)
  
  import difflib 
  t1 = time.clock()
  x = difflib.SequenceMatcher(None, textA, textB)
  print("B: ", time.clock() - t1)
