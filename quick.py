import re 

def subsequence(startA, s1, s2) :
  ''' returns list of tuples of indices (len, a1, b1) where len is the length of
  subsequence while a1 and b1 are starting index in first and second string
  respecitvely. 
  '''
  aI = startA
  bI = 0 
  matchBegin = False
  matchEnd = False 
  maxlength = 0
  index = (-1, -1)
  while(aI < s1.__len__() and bI < s2.__len__()) :
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
        lenOfSubSeq = aI - startA 
        aI = startA 
        if lenOfSubSeq > 0 :
          if lenOfSubSeq > maxlength :
            maxlength = lenOfSubSeq 
            index = (startA, bI-lenOfSubSeq)
      else :
        bI += 1 
  return maxlength, index

def quickMatch(textA, textB) :
  matchSequences = dict()
  loopLength = len(textA)
  done = False 
  currenIndex = 0
  while(done == False) :
    length, index = subsequence(currenIndex, textA, textB)
    print length, index
    print textA
    print textB
    textA = textA[currenIndex+length:]
    currenIndex += length
    if currenIndex >= textA.__len__() :
      done = True

if __name__ == "__main__" :
  import cProfile as profile 
  import string, random
  import time 
  textA = "abcdefg"
  textB = "xyababcdg"
  #textA = "".join([random.choice('abcde') for i in xrange(100)])
  #textB = "".join([random.choice('abcdewx') for i in xrange(100)])
  #print textA
  
  t1 = time.clock()
  quickMatch(textA, textB)
  print("A: ", time.clock() - t1)
  
  import difflib 
  t1 = time.clock()
  x = difflib.SequenceMatcher(None, textA, textB)
  print("B: ", time.clock() - t1)
