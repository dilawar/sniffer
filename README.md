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

The default path for configuration file is ``~/.config/sniffer/config``. For
non-standard location, use ``--config`` option.::

  code-sniffer --config config-file-path

If you want to run it from the repository then run the ``run.sh`` file in
terminal. Make sure you have ``python-pdfmider`` library installed.


See the following section on how to edit the `snifferrc` file.

Config file 
===========

A sample config file is shown below::

    [source]
    # Dir where various folders containing source codes or text files are located.
    # This directory will be 'walked' and each subdirectory inside this directory
    # will be considered as belonging to different student. In short, inside
    # 'dir', each subdirectory will be compared with every other subdirectory.
    dir = /home/dilawar/Works/hpc21/2013ee668/Assignments/A4/Submissions

    # This is the regular expression of the names of files. If you want to compare
    # all files leave it empty or .* will do. In this example, we will only
    # consider files which are ended with vhdl or vhd extension.
    regex = .*(vhdl|vhd)$

    # Specify language of file.
    # Available : vhdl, verilog, ctype, text, pdf 
    language = vhdl

    # Compiler. Currently this is of no use.
    compiler = ghdl

    # make compare true if you want to compare. If this is not set to true, it won't
    # match. This is here for development purpose. In most cases, this should be
    # true.
    compare = true

    # Dump the results of analysis in directory of database.
    analyze_result = true 

    # Currently useless.
    send_email = false

    [filter]
    # If this regex is found in the text of file, then the file is ignored. 
    regex = ((Madhav\s+Desai)|(entity\s+(reg|\w*mux\w*|unsigned\_(comparator|adder)|mux\dto\d|decoder\dto\d|Datapath)\s+is)|(operand1.+operand2.+result.+overflow)|(data\_in.+data\_out.+clock))
    regex_flags = DOTALL,IGNORECASE 

    # larger size will be ignored. -1 for all. In Kb
    max_size = -1

    # Max words a text file can contains. -1 for 2^32.
    max_words = 10000
    # Mininum words a text files must contain.
    min_words = 100

    [algorithm]
    # Available algoritms : difflib, quick, 
    name = difflib

    [database]
    # Path where sqlite3 database should be saved. Generated graphviz files will
    # be saved to this file only. After match is complete, results are stored in
    # csv files. identical_severity.csv has the almost matching files followed
    # by very_high_serverity.csv, high_serverity.csv etc.
    path = /home/dilawar/Works/hpc21/2013ee668/Assignments/A4/db/

    # Name of the database. Leave it as it is. If :memory: is used then database
    # is build in memory. Untested feature.
    name = sniffer.sqlite3 
    #name = :memory:
