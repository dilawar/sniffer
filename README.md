sniffer
=======

Code sniffer to check the similarity between text files. Works well with
programming languages although the pdf are also supported.

Status 
======
 
  Under development. 

Dependency 
=========

1. Python2.6 or later
2. python-pdfminer (for pdf file)
3. python-sqlite3


Usage 
=====
  python sniffer.py --config ./snifferrc 

Config file 
===========

    [source]
    # this is the source directory
    dir = /home/dilawar/Works/hpc21/2013ee668/Assignments/A4/Submissions
    regex = .*(vhdl|vhd)$
    language = vhdl
    compiler = ghdl
    # make compare true if you want to compare.
    compare = true
    analyze_result = true 
    send_email = false

    [filter]
    # If this regex is matched then the file will be ignored. 
    regex = ((Madhav\s+Desai)|(entity\s+(reg|\w*mux\w*|unsigned\_(comparator|adder)|mux\dto\d|decoder\dto\d|Datapath)\s+is)|(operand1.+operand2.+result.+overflow)|(data\_in.+data\_out.+clock))
    regex_flags = DOTALL,IGNORECASE 
    # larger size will be ignored. -1 for all. In Kb
    max_size = -1
    # Max words a text file can contains. -1 for 2^32.
    max_words = 10000
    # Mininum words a text files must contain.
    min_words = 100
    autotest = false

    [algorithm]
    # Available algoritms : difflib, quick, 
    name = difflib

    [database]
    path = /home/dilawar/Works/hpc21/2013ee668/Assignments/A4/db/
    name = sniffer.sqlite3 
    #name = :memory:
