import re
import io, shutil
import glob, os, subprocess, sys

class Verilog:

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

## Following is for VHDL. Write equivalent verilog code or ognore them.

#
#    def compile_testbench(self, dir, cxx):
#        '''
#        This function compiles the test_bench in given directory.
#        
#        '''
#        os.chdir(dir)
#        files = glob.glob('*.v')
#        tbcount = 0;
#        for file in files:
#            f = open(file, "r")
#            self.src = ''
#            if f:
#                try:
#                    self.src = f.read()
#                except EOFError:
#                    print "Can not open file."
#                if not self.src: break
#                # This will match the testbech entity in given file.
#                m = re.search(r'entity\s+(\w+)\s+is[\s\n]+end\s+(\w*)\s*\w*[;]'\
#                        , self.src, re.I)
#                if m : 
#                    tbcount = tbcount+1
#                    test_bench = m.group(1)
#                    print "Testbench {0} is found".format(test_bench)
#                    self.tbname = test_bench
#
#                    self.get_ports(test_bench, self.src);
#
#                    if self.autotest == 'true':
#                        print '\n\n** ADDING NEW TESTBENCHES **\n'
#                        self.add_testbenches(self.component, self.port)
#                        self.add_test_vectors(self.testDir)
#                    else:
#                        print 'No self-testing...'
#
#                    #print(" |- Compiling {0} using {1}".format(test_bench, cxx))
#                    #print("In file {0}".format(f.name))
#                    #print "cxx : {0}".format(cxx)
#                    
#                    if self.compile == 'true' :
#                        if cxx == 'ghdl':
#                            vcdOption = "--vcd="+test_bench+".vcd"
#                            subprocess.call(["ghdl", "-a", f.name] \
#                                    , stdout=subprocess.PIPE)
#                            subprocess.call(["ghdl", "-m", test_bench] \
#                                    , stdout=subprocess.PIPE)
#                            subprocess.call(["ghdl", "-r" \
#                                    , test_bench, "--stop-time=1000ns" \
#                                    , vcdOption] \
#                                    , stdout=subprocess.PIPE)
#                        elif cxx == 'vsim' :
#                            pass
#                    else : pass
#
#                else : 
#                    pass
#                    
#        #print 'Total {0} testbenches are found in this dir.'.format(tbcount)
#
#    def get_ports(self, test_bench, data):
#        self.port = dict()
#        self.component = dict()
#        print "Getting port information for {0} in file {1}".format(test_bench, file)
#        m = re.search(r'''component\s+(\w+)\s*(is)*\s+
#                port\s*[(]
#                ((\s*\w+(\s*[,]\s*\w+\s*)*\s*[:]\s*
#                (in|out)\s*\w+\s*([(]\s*\d+\s*\w+\s*\d+\s*[)])*\s*[;]*)*)
#                \s*[)]\s*[;]
#                \s+end\s+component\s*\w*[;]'''
#                , data, re.I | re.VERBOSE)
#
#        if m:
#            name = m.group(1)
#            text = m.group(3)
#            self.comp_expr = text
#            self.component[(name, test_bench)] = text
#            for pExpr in text.split(';'):
#                if pExpr.strip() == '':
#                    pass
#                else:
#                    [p, expr] = pExpr.split(':')
#                    p = p.strip()
#                    temp = expr.split()
#                    type = temp[0].strip()
#                    del temp[0]
#                    for i in p.split(','):
#                        expr = ' '.join(temp)
#                        self.port[(i, m.group(1))] = (type, (expr))
#        
#        else:
#            pass
#            #print ("Can not find any component in this file.")
#
#
#
#    def add_testbenches(self, component, port):
#        '''
#        This function adds new testbenches.
#        '''
#        for (comp_name,tb_name), comp_expr in component.iteritems():
#
#            if not os.path.isdir('./AUTO_GEN'):
#                os.makedirs('./AUTO_GEN')
#            
#            # Check if testbench already been generated, if yes, delete it.
#            file = "./AUTO_GEN/auto_"+tb_name+".ghdl"
#            if os.path.isfile(file):
#                os.remove(file)
#
#            with open(file, "a+") as tb:
#                # Start writing testbench.
#                tb.write(u'''---
#-- This testbench is automatically generated using a python
#-- script.
#-- (c) Dilawar Singh, dilawar@ee.iitb.ac.in
#-- GNU GPL
#LIBRARY IEEE;
#USE IEEE.std_logic_1164.all;
#USE STD.textio.all;
#USE WORK.all;
#
#ENTITY testbench IS 
#end ENTITY testbench;
#
#ARCHITECTURE stimulus OF testbench IS\n\tCOMPONENT ''')
#                tb.write(unicode(comp_name)+u'\n')
#                tb.write(u'\tPORT ( \n')
#                tb.write(u'\t'+unicode(comp_expr)+u'\n')
#                tb.write(u'\t);\nEND COMPONENT;\n')
#
#                # Attach signal.
#                for (name,comp), (a, expr) in self.port.iteritems():
#                    if comp == comp_name :
#                        tb.write(u'\tSIGNAL '+unicode(name)+u' : '+unicode(expr))
#                        tb.write(u';\n')
#                    else:
#                        pass
#
#                tb.write(u'BEGIN\n')
#                tb.write(u'\tdut : '+unicode(comp_name)+u' \n\tPORT MAP (');
#
#                # construct port map expression.
#                portmap_expr = ''
#                for (name, comp), (a, expr) in self.port.iteritems():
#                    if comp == comp_name :
#                        portmap_expr = portmap_expr+(name)+u', '
#                    else:
#                        pass
#            
#                # remove last comma from the list.
#                expr = portmap_expr[:(len(portmap_expr)-2)]
#                tb.write(unicode(expr)+u' );\n')
#                tb.write(u'\n\ttest : PROCESS \n')
#
#                # Create variables.
#                for (name,comp), (a, expr) in self.port.iteritems():
#                    if comp == comp_name :
#                        tb.write(u'\t\tVARIABLE var_'+unicode(name.strip())+u' : '+unicode(expr))
#                        tb.write(u';\n')
#                    else:
#                        pass
#
#                tb.write(u'\n\t\tfile vector_file : text is in \"'\
#                        +unicode(self.tbname)+u'.txt\";\n')
#                tb.write(u'''
#\t\tVARIABLE l : LINE;
#\t\tVARIABLE vector_time : TIME;
#\t\tVARIABLE r : REAL;
#\t\tVARIABLE good_number, good_val : BOOLEAN;
#\t\tVARIABLE space : CHARACTER;
#                        ''')
#
#                tb.write(u'''
#\t\tBEGIN
#\t\tWHILE NOT endfile(vector_file) LOOP
#\t\t\treadline(vector_file, l);
#\t\t\tread(l, r, good => good_number);
#\t\t\tNEXT WHEN NOT good_number;
#\t\t\tvector_time := r * 1 ns;
#\t\t\tIF (now < vector_time) THEN
#\t\t\t\tWAIT FOR vector_time - now;
#\t\t\tEND IF;
#\t\t\tread(l, space);\n''')
#                # read other variables and use them as input.
#                for (name,comp), (a, expr) in self.port.iteritems():
#                    if comp == comp_name :
#                        tb.write(u'\t\t\tread(l, var_'+unicode(name.strip())+\
#                                u', good_val);\n') 
#                        tb.write(u'\t\t\tASSERT good_val REPORT \"bad '+\
#                                unicode(name)+u' value\";\n')
#                    else:
#                        pass
#                # Assign these values to input ports.
#                for (name,comp), (type, expr) in self.port.iteritems():
#                    if comp == comp_name :
#                        if type.strip() == 'in' :
#                            tb.write(u'\t\t\t'+unicode(name)+u' <= var_'+\
#                                    unicode(name.strip())+u';\n')
#                    else:
#                        pass
#
#                # ASSERT OUTPUT ports.
#                for (name,comp), (type, expr) in self.port.iteritems():
#                    if comp == comp_name :
#                        if type.strip() == 'out' :
#                            tb.write(u'\t\t\tASSERT var_'+unicode(name.strip())+\
#                                    u' = '+unicode(name.strip())+\
#                                    u' REPORT \"vector mismatch\"'+\
#                                    u' SEVERITY WARNING;\n')
#                    else:
#                        pass
#
#                tb.write(u'\t\tEND LOOP;\n')
#                tb.write(u'\t\tASSERT false REPORT \"Test complete\";\n')
#                tb.write(u'\t\tWAIT;\n')
#                tb.write(u'\tEND PROCESS;\n')
#                tb.write(u'END ARCHITECTURE;\n')
#
#
#    def add_test_vectors(self, dir):
#        print dir
#        for file in glob.glob('*.vec'):
#            print file.name
#
    # Fix vhdl input file to remove comments as well as keywords etc.
    def fix_text(self, text, lang) :

        processed_text = ''
        num_lines = 0
        if lang == 'verilog' :
            lines = text.split('\n')
            # ignore first comment block.
            i = 0
            line = lines[i]
            #ignore first block of comments and empty lines.

            while len(line.strip()) <= 4 :
                i += 1
                line = lines[i]

            if line.find("\'timescale") :
                i += 1;
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


