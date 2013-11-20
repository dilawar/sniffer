import sqlite3 as sql
import os, sys
import difflib

def formatText(txt, lang) :
  if lang == "vhdl" :
    import lang_vhdl as vhdl
    obj = vhdl.VHDL()
    return obj.fix_text(txt)
  if lang == "verilog" :
    import lang_verilog as verilog
    obj = verilog.Verilog()
    return obj.fix_text(txt)
  if lang == "pdf" :
    import lang_pdf as pdf
    # NOTE: txt is filename
    obj = pdf.Pdf()
    return obj.fix_text(txt)
  if lang == "text":
      return txt
  else :
    print("[W] This language is not supported. Assuming text ...")
    return txt

def compareAndReturnResult(textA, textB, algorithm="subsequence" ) :
  if algorithm == "subsequence" :
    wordsA = textA.split()
    wordsB = textB.split()

    if len(wordsA) < 4 or len(wordsB) < 4 :
      return "Less than four words", 0.0

    lR = float(len(wordsA)) / len(wordsB)
    if lR > 1.0 :
      lR = 1/lR
    if lR < 0.2 :
      return "Files differ in sizes", lR

    # check intersection of keywords
    setA = set(wordsA)
    setB = set(wordsB)

    intersectionSize =  float(len(setA.intersection(setB))) / min(len(setA), len(setB))
    if intersectionSize < 0.35 :
      return "Small keyword intersection", intersectionSize

    # if intersection of these two set is very small then there is little
    # maching in these two files.
    s = difflib.SequenceMatcher(None, textA, textB)
    return "difflib", s.ratio()

  else :
    print("[E] Algorithm not specified")
    sys.exit(0)


def commonPrefix(string1, string2) :
  prefix = ""
  done = False;
  i = 0
  while(done == False) :
    if string1[i] == string2[i] :
      prefix += string1[i]
    else :
      done = True
    i += 1
  return prefix
