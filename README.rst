About
-----

This program is intended to be used to check plagiarism in assignments. It is a
poor man's `MOSS<http://theory.stanford.edu/~aiken/moss/>`_.

Status 
======
 
  Under development but can be used. Report bugs on it `github
  page<http://github.com/dilawar/sniffer>`_.

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

A sample config file is shown below

::
    [source]

    # This is main directory.
    # This directory contains folders. Each folder is compared against every
    # other folder.
    # Each folder is walked and files matching `regex` are collected. These
    # files will be compared.
    dir = /home/dilawar/Works/hpc21/2013ee668/Assignments/A4/Submissions

    # This is the regular expression of the names of files. If you want to compare
    # all files leave it empty or .* will do. In this example, we will only
    # consider files which are ended with vhdl or vhd extension.
    regex = .*(vhdl|vhd)$

    # Specify language of file.
    # Available : vhdl, verilog, ctype, text, pdf. If in doubt make it text.
    # Further support to be added to other languages as well. 
    language = vhdl

    # Make compare true if you want to compare. If this is not set to true, it won't
    # match. This is here for development purpose. In most cases, this should be
    # true.
    compare = true

    # Dump the results of analysis in directory of `database`.
    analyze_result = true 

    # Currently useless.
    send_email = false

    [filter]
    # If this regex is found in the text of file, then the file is ignored. The
    # format of regex is defined in python re library.
    regex = ((Madhav\s+Desai)|(entity\s+(reg|\w*mux\w*|unsigned\_(comparator|adder)|mux\dto\d|decoder\dto\d|Datapath)\s+is)|(operand1.+operand2.+result.+overflow)|(data\_in.+data\_out.+clock))
    regex_flags = DOTALL,IGNORECASE 

    # larger than this size will be ignored. -1 for all. In Kb
    max_size = -1

    # Max words a text file can contains. -1 for 2^32.
    max_words = 10000
    # Mininum words a text files must contain.
    min_words = 100

    [algorithm]
    # Available algoritms : difflib, quick, . Quick is not available in this
    # relase. So leave it unchanged.
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
