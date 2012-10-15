''' 

This file read vhdl files in all directory and compare them and create a log
file which can be used by other script to analyze.

'''
import os 
import re 
import difflib
import sys
import time
import datetime
import numpy
import pickle
import collections as cl
import shutil
import cStringIO
from lang_vhdl import VHDL
from lang_verilog import Verilog
from lang_ctype import Ctype
from lang_pdf import Pdf
 
class CompareProgram():
    def __init__(self, lang, regex):
        self.src_path = '.'
        self.log_dir = self.src_path+"/stats/"
        self.allfiles = []
        self.file_dict = cl.defaultdict(list)
        self.total_program = 0
        self.lang = lang
        self.regex = regex
        self.log_name = self.src_path+"/stats.log"
        self.log_name_low = self.src_path+"/copy_low.log"
        self.log_name_med = self.src_path+"/copy_medium.log"
        self.log_name_hig = self.src_path+"/copy_high.log"
        self.log_name_exa = self.src_path+"/copy_exact.log"
        self.log_list_pkl = self.src_path+"/log_list.pkl"
        self.log_list = []
        self.is_log = True

    
    def get_log_list(self):

        return self.log_list
    
    
    def set_dir_path(self, dir, delFlag):
        
        if os.path.exists(dir):
            stat_dir = dir+"/stats"
            if os.path.exists(stat_dir):
                if delFlag == True :
                    # create a backup with timestamp.
                    time = datetime.datetime.now()
                    shutil.copytree(stat_dir, stat_dir+'_'\
                            +unicode('_'.join(time.isoformat().split(':'))))
                    shutil.rmtree(dir+"/stats")
                    os.makedirs(dir+"/stats")
                else : pass
            else:
                os.makedirs(dir+"/stats")
        else : 
            print 'There is no dirctory {0}'.format(dir)
            sys.exit(0)

        self.src_path = dir
        self.log_dir = self.src_path+"/stats/"
        self.log_name = self.log_dir+"/stats.log"
        self.log_name_low = self.log_dir+"/copy_low.log"
        self.log_name_med = self.log_dir+"/copy_medium.log"
        self.log_name_hig = self.log_dir+"/copy_high.log"
        self.log_name_exa = self.log_dir+"/copy_exact.log"
        self.log_list_pkl = self.log_dir+"/log_list.pkl"

    def safe_backup(self, path, keep_original=True):
        
        """safe_backup

        Rename a file or directory safely without overwriting an existing 
        backup of the same name.
        
        """
        count = -1
        new_path = path
        while True:
            if os.path.exists(path):
                new_path = unicode("{0}.bak".format(path))
                if os.path.isfile(path):
                        shutil.copy(path, new_path)
                elif os.path.isdir(path):
                        shutil.copytree(path, new_path)
                else:
                    shutil.move(path, new_path)
                break
            else:
                break
        return path


    def get_all_programs(self) :
        count = 0;
        print "Searching {0} for programs\n".format(self.src_path)
        for dirpath, dirnames, filenames in os.walk(self.src_path) :
          for file in filenames :
            if self.lang == 'vhdl' :
              if(self.regex.strip() == "") :
                self.regex = '\w+\.vhd[l]?$'
            elif self.lang == 'verilog' :
              if(self.regex.strip() == "") :
                self.regex = '\w+\.v$'
            elif self.lang == 'ctype' :
              if(self.regex.strip() == "") :
                self.regex = '\w+\.(c|cpp|cc|hh|h|hpp)$'

            elif self.lang == 'pdf' :
              if(self.regex.strip() == "") :
                self.regex = '\w+\.(pdf)$'

            else :
              print "This language {0} is not supported.".format(self.lang)

            if re.search(self.regex, file):
              path = dirpath+"/"+file
              size = os.path.getsize(path)
              if size > 20 :
                self.allfiles.append(path)
                count = count + 1

        self.total_program = count
        print "Total {0} programs".format(self.total_program)

    def create_dict_of_program(self):
        
        '''create_dict_of_program
        
        Extract students names and create a map which keeps their files. 
        
        '''
        
        self.get_all_programs()
        index = 0
        prevKey = ''
        for i in self.allfiles:
            key = i.split(self.src_path)[1]
            key = key.split('/')[1]
            if prevKey == key : 
                self.file_dict[(index, key)].append(i)
            else :
                self.file_dict[(index+1, key)].append(i)
                index = index + 1
                prevKey = key

        

    def init_log_streams(self):
        # string streams.
        self.log_file = cStringIO.StringIO()
        self.log_file_low = cStringIO.StringIO()
        self.log_file_med = cStringIO.StringIO()
        self.log_file_hig = cStringIO.StringIO()
        self.log_file_exa = cStringIO.StringIO()


    def compare_with_programs(self, count,  file, dict):
        '''
        Dictionary dict contains all files submitted by a single student. File
        'file' is compared with this dictionary.
        
        '''
        #print ' Compare with {0}'.format(file)
        #print dict
        with open(file, 'r') as f1 :
            textA = f1.read()
            cnt = 0
            for i in dict :
                with open(i, 'r') as f2:
                    textB = f2.read()

                    lenTextA = len(textA)
                    lenTextB = len(textB)

                    if float(lenTextA)/lenTextB > 0.2 or lenTextA/lenTextB  < 50 :
                      if self.lang == 'vhdl' :
                          vhdl = VHDL()
                          text1, line1, word_count1 = vhdl.fix_text(textA, self.lang)
                          text2, line2, word_count2 = vhdl.fix_text(textB, self.lang)
                      
                      elif self.lang == 'verilog' :
                          verilog = Verilog()
                          text1, line1 = verilog.fix_text(textA, self.lang)
                          text2, line2  = verilog.fix_text(textB, self.lang)
              
                      elif self.lang == 'ctype' :
                          ctype = Ctype()
                          text1, line1 = ctype.fix_text(textA, self.lang)
                          text2, line2  = ctype.fix_text(textB, self.lang)
              
                      elif self.lang == 'pdf' :
                          pdf = Pdf()
                          text1, line1 = pdf.fix_text(file, self.lang)
                          text2, line2 = pdf.fix_text(i, self.lang)

                      else :
                          print "This language is not supported."

                      print " ++ Comparing {0}:{2} <-> {1} : {3}".format(f1.name.split('/').pop()
                                     , f2.name.split('/').pop()
                                     , len(textA), len(textB))
                      s = difflib.SequenceMatcher(None, text1, text2)
                      lst = s.get_matching_blocks()
                      w = 0
                      for a, b, n in lst :
                          w = w + len(lst)*n
      
                      # there is no use of w < 200 file.
                      if(len(text1.split()) < 3 or len(text2.split()) < 3) :
                          pass

                      elif len(text1.split()) > 200 or len(text2.split()) > 200 :
                          f_ratio = 0.00
                          f_ratio = float(len(text1.split()))/ float(len(text2.split()))
                          log = '{0}, {1}, {2}, {3}, {4}, {5} \n'.format(\
                              f_ratio , w, w/len(lst) ,s.ratio(), f1.name, f2.name )
                          self.log_file.write(log)
                          self.log_list.append([f1.name, f2.name\
                                  , s.ratio() ,f_ratio, w, w/len(lst)])

  #                        if s.ratio() > 0.27 and s.ratio() < 0.42  :
  #                            print '   Mild copying is possible in following files'
  #                            print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
  #                                    .format(s.ratio(), f1.name, f2.name)
  #                            self.log_file_low.write(log)
  #                        if s.ratio() >= 0.42 and s.ratio() < 0.53  :
  #                            print '   Significant copying possible in files'
  #                            print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
  #                                    .format(s.ratio(), f1.name, f2.name)
  #                            self.log_file_med.write(log)
                          if s.ratio() >= 0.53 and s.ratio() <= 0.62 :
                              print '   *These two files matches significantly. Check manually.'
                              print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
                                      .format(s.ratio(), f1.name, f2.name)
                              self.log_file_hig.write(log)

                          if s.ratio() >= 0.62 :
                              print '   *NOTICE : These files are copied!'
                              print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
                                      .format(s.ratio(), f1.name, f2.name)
                              self.log_file_exa.write(log)

                          else : pass
                              #print 'No significant match.'
                              #print '{0} : {1} : {2}'.format(s.ratio(), f1.name, f2.name)

                      # Handle small files. Divide s.ratio() by a suitable number.
                      else :
                          a = [30,50,100,150,200,250,300]
                          b = [0.7,0.81,0.85,0.88,0.89,0.95,0.99]

                          poly_fit = numpy.polyfit(a, b, 3)

                          scaled_by = float(min(line1, line2))/30.0
                          f_ratio = 0.00
                          f_ratio = float(len(text1.split()))/ float(len(text2.split()))
                          ratio = s.ratio() * numpy.polyval(poly_fit, min(line1, line2))
                          log = '{0}, {1}, {2}, {3}, {4}, {5} \n'.format(\
                              f_ratio , w, w/len(lst) ,ratio, f1.name, f2.name )
                          self.log_file.write(log)
                          self.log_list.append([f1.name, f2.name\
                                  , ratio ,f_ratio, w, w/len(lst)])

  #                        if ratio > 0.27 and ratio< 0.42  :
  #                            print '   Mild copying is possible in following files'
  #                            print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
  #                                    .format(ratio, f1.name, f2.name)
  #                            self.log_file_low.write(log)
  #                        if ratio >= 0.42 and ratio < 0.53  :
  #                            print '   Significant copying possible in files'
  #                            print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
  #                                    .format(ratio, f1.name, f2.name)
  #                            self.log_file_med.write(log)
                          if ratio >= 0.53 and ratio <= 0.59 :
                              print '   *These two files matches significantly. Check manually.'
                              print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
                                      .format(ratio, f1.name, f2.name)
                              self.log_file_hig.write(log)

                          if ratio >= 0.59 :
                              print '   *NOTICE : These files are copied!'
                              print '   |- {1}\n   |- {2}\n   ++MATCH INDEX: {0} \n'\
                                      .format(ratio, f1.name, f2.name)
                              self.log_file_exa.write(log)

                          else : pass
                              #print 'No significant match.'
                              #print '{0} : {1} : {2}'.format(ratio, f1.name, f2.name)

        

    def save_logs(self):
        log_path = (self.log_name)
        with open(log_path, 'w') as log_file_f :
            log_file_f.write(self.log_file.getvalue())

        log_path =(self.log_name_low)
        with  open(log_path, 'w') as  log_file_low_f :
            log_file_low_f.write(self.log_file_low.getvalue())

        log_path = (self.log_name_med)
        with  open(log_path, 'w') as  log_file_med_f :
            log_file_med_f.write(self.log_file_med.getvalue())

        log_path = (self.log_name_hig)
        with  open(log_path, 'w') as log_file_hig_f :
            log_file_hig_f.write(self.log_file_hig.getvalue())

        log_path = (self.log_name_exa)
        with  open(log_path, 'w') as log_file_exa_f :
            log_file_exa_f.write(self.log_file_exa.getvalue())
        
        # Pickle the dictionary.
        log_path = (self.log_list_pkl)
        with  open(log_path, 'wb') as list_pkl :
            pickle.dump(self.log_list, list_pkl)


    def traverse_and_compare(self):
        ''' Take a file and compare it with all other files which have not been
        compared with it before.
        
        '''

        self.init_log_streams()
        self.create_dict_of_program()
        cnt0 = 0
        comp = dict()
        for i in self.file_dict :
            id1, name1 = i
            cnt1 = 0
            print 'Comparing for {0}'.format(name1)
            for fl1 in self.file_dict[i]:
                lst = []
                for j in self.file_dict :
                    id2, name2 = j
                    if j <= i : pass
                    else :
                        lst.append(id2)
                        cnt1 += len(self.file_dict[j])
                        self.compare_with_programs(cnt0, fl1, self.file_dict[j])
                comp[id1] = lst
                cnt0 += cnt1
            print '\n * For {0}, total {1} comparison * \n'.format(name1, cnt1)
        self.save_logs()   
        print '\n == NOTICE : TOTAL {0} comparisons for this assignment == \n'.format(cnt0)
