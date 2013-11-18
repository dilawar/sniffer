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
  index = 0
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
            index = bI-lenOfSubSeq
      else :
        bI += 1 
  return maxlength, index

def quickMatch(textA, textB) :
  matchSequences = dict()
  loopLength = len(textA)
  currenIndex = 0
  maxlength = 1
  i = 0
  while(textA.__len__() > maxlength) :
    length, index = subsequence(0, textA, textB)
    if length > 1 :
      textA = textA[length:]
      i += length
    if length >  maxlength :
      maxlength = length
      print length, index
      #print("Text A: ",textA)
      #print("Text B: ",textB)
      matchTxt = textA[:length]
      print("[M] : ", matchTxt)
    currenIndex += length
    if length > 10 :
      pass
      #textB = textB.replace(matchTxt, "")
      #textB = textB[:index] + textB[index+length:]
    textA = textA[1:]
    i += 1
    matchSequences[(i, index)] = matchTxt

  return matchSequences

if __name__ == "__main__" :
  import cProfile as profile 
  import string, random
  import time 
  #textA = "abcdefg"
  #textB = "xyababcdg"
  textA = open("../../hpc21/sniffer/files/file1.txt", "r").read()
  textB = open("../../hpc21/sniffer/files/file2.txt", "r").read()
  #textA = "".join([random.choice('ab') for i in xrange(1000)])
  #textB = "".join([random.choice('ba') for i in xrange(1000)])
  #print textA
  
  t1 = time.clock()
  matchSequences = quickMatch(textA.split(), textB.split())
  print("A: ", time.clock() - t1)
  #for m in matchSequences :
  #  if len(matchSequences[m]) > 10 :
  #    print(m, " ".join(matchSequences[m]))
  #    print("\n")
  
  import difflib 
  t1 = time.clock()
  x = difflib.SequenceMatcher(None, textA, textB)
  print("B: ", time.clock() - t1)
