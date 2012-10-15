import re
import io, shutil
import glob, os, subprocess, sys

class Ctype:

    def __init__(self):
        self.tbname = ''
        self.comp_name = ''
        self.comp_expr = ''
        self.src = ''
        self.srcDir = ''
        self.testDir = ''
        self.autotest = 'false'
        self.compile = 'false'

    def dirName(self, dir):
        self.srcDir = dir
        self.testDir = dir


    # Fix vhdl input file to remove comments as well as keywords etc.
    def fix_text(self, text, lang) :

        processed_text = ''
        num_lines = 0
        if lang == 'ctype' :
            lines = text.split('\n')
            # ignore first comment block.
            i = 0
            line = lines[i]
            #ignore first block of comments and empty lines.

            while len(line.strip()) <= 4 :
                i += 1
                line = lines[i]

            if line.strip()[0:2] == "/*"  :
                while not line.find("*/"): 
                    i += 1
                    line = (lines[i]).strip()
            
            if line.strip()[0:2] == "//" :
                while line.strip()[0:2] == "//"  : 
                    i += 1;
                    line = (lines[i]).strip()
            
            if line.strip()[0:2] == "/*"  :
                while not line.find("*/"): 
                    i += 1
                    line = (lines[i]).strip()

            for i in range(i, len(lines)) :
                line = lines[i].strip()
                if len(line) == 0 : pass
                else :
                    processed_text += ' '+line.lower()
                    num_lines += 1

        return processed_text, num_lines

