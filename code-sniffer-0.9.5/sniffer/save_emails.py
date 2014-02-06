import os
import tarfile
import smtplib
import mimetypes
import collections as cl
from optparse import OptionParser
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.Utils import formatdate
from email import Encoders

class CreateMsgAndDatabase():

    def __init__(self, dir, activity_name):
        self.log_path = dir
        self.log_list = []
        self.activity = unicode(activity_name)
        self.student_dict = cl.defaultdict(list)
        self.src_path = dir.split('stats')[0]
        self.down_dir = dir.split(activity_name)[0]
        self.grade_file = self.down_dir+'/grades.txt'
        
    def save_emails_convicted(self, convict_dict, accused_dict):

        '''
        This function sends email to student who should meet the instructors.
        '''
        print 'Creating emails database. Make sure you have grades.txt (CSV) file your'
        print '{0}'.format(self.src_path)

        if os.path.exists(self.grade_file) :
            fl_grader = open(self.grade_file, "r")
        else :
            print 'File grades.txt (CSV) does not exists in {0}'\
                    .format(self.down_dir)
            sys.exit(32)

        
        # create data_base of emails and marks. 
        dict_students = cl.defaultdict(list)
        # ignore the first line.
        first_line = fl_grader.readline()
        for line in fl_grader.readlines() :
            ln = line.split(',')
            if ln[1] == '': # if surname is not present.
                key = ln[0]
            else : # append surname.
                key = ln[0]+' '+ln[1]

            dict_students[key] = ln[2:] 

        for i in convict_dict : 
            tarfile_name = self.log_path+'/'+'_'.join(self.activity.split())\
                    +'_'+'_'.join(i.split())+'.tar'
            if len(dict_students[i]) < 4 : pass 
            else :
                email_id = dict_students[i][3]
                msg = ''
                #print tarfile_name
                with tarfile.open(tarfile_name, 'w:gz') as tar :
                    for entry in  convict_dict[i] :
                        # create an archive.
                        file1 = entry[0]
                        file2 = entry[1]
                        msg = msg + '\n\n |- {0}\n |- {1}\n |- MATCH INDEX {2}'\
                                .format(file1, file2, entry[2])
                        tar.add(self.src_path+file1, recursive=False, arcname=file1)
                        tar.add(self.src_path+file2, recursive=False, arcname=file2)
                tar.close()

                # Now construct the mail msg
                HOST = 'smtp-auth.iitb.ac.in'
                message = MIMEMultipart()
                FROM = 'EE705-TA'
                COMMMASPACE = ', '
                TO = [email_id]
                CC = ['dilawars@iitb.ac.in', 'nanditha@iitb.ac.in', \
                        '08307r20@iitb.ac.in', '07d07022@iitb.ac.in' \
                        , '10307009@iitb.ac.in', '07d07011@iitb.ac.in']

                message["From"] = "dilawars@iitb.ac.in"
                message["To"] = unicode(TO)
                message["Cc"] = unicode(CC)
                message["Subject"] = "Attached files are very similar. Meet your instructor!"
                message["Date"] = formatdate(localtime=True)

                f = open('msg_convicted', 'r')
                text = f.read()
                text = text + msg
                text = text +'\n--\n' \
                        +'\nThis email is system-generated. You need not reply.' 

                message.attach(MIMEText(text))
                # attach a file
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(tarfile_name,"rb").read() )
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'\
                        % os.path.basename(tarfile_name))
                message.attach(part)
             

                with open(self.log_path+"/"+unicode(email_id)+"_email_con.msg",\
                        'w') as email_msg :
                    email_msg.write(message.as_string())
                 
    
    def save_emails_accused(self, convict_dict, accused_dict):

        '''
        This function sends email to student who are warned of copying.
        '''
        print 'Getting emails database. Make sure you have grades.txt (CSV) file your'
        print '{0}'.format(self.src_path)

        if os.path.exists(self.grade_file) :
            fl_grader = open(self.grade_file, "r")
        else :
            print 'File grades.txt (CSV) does not exists in {0}'\
                    .format(self.down_dir)
            sys.exit(32)
        
        # create data_base of emails and marks. 
        dict_students = cl.defaultdict(list)
        # ignore the first line.
        first_line = fl_grader.readline()
        for line in fl_grader.readlines() :
            ln = line.split(',')
            if ln[1] == '': # if surname is not present.
                key = ln[0]
            else : # append surname.
                key = ln[0]+' '+ln[1]

            dict_students[key] = ln[2:] 

        for i in accused_dict : 
            tarfile_name = self.log_path+'/'+'_'.join(self.activity.split())\
                    +'_'+'_'.join(i.split())+'.tar'
            if len(dict_students[i]) < 4 : pass
            else :
                email_id = dict_students[i][3]
                msg = ''
                #print tarfile_name
                with tarfile.open(tarfile_name, 'w:gz') as tar :
                    for entry in accused_dict[i] :
                        # create an archive.
                        file1 = entry[0]
                        file2 = entry[1]
                        msg = msg + '\n\n |- {0}\n |- {1}\n |- MATCH INDEX {2}'\
                                .format(file1, file2, entry[2])
                        tar.add(self.src_path+file1, recursive=False, arcname=file1)
                        tar.add(self.src_path+file2, recursive=False, arcname=file2)
                tar.close()

                COMMMASPACE = ', '
                # Now construct the mail msg
                HOST = 'smtp-auth.iitb.ac.in'
                message = MIMEMultipart()
                FROM = 'EE705-TA'
                TO = [email_id]
                CC = ['dilawars@iitb.ac.in', 'nanditha@iitb.ac.in', \
                        '08307r20@iitb.ac.in', '07d07022@iitb.ac.in' \
                        , '10307009@iitb.ac.in', '07d07011@iitb.ac.in']

                message["From"] = "dilawars@iitb.ac.in"
                message["To"] = unicode(TO)
                message["Cc"] = COMMMASPACE.join(CC)
                message["Subject"] = "FYI : Attached files are similar. TA should verify."
                message["Date"] = formatdate(localtime=True)

                f = open('msg_accused', 'r')
                text = f.read()
                text = text + msg
                text = text +'\n--\n' \
                        +'\nThis email is system-generated. You need not reply.' 

                message.attach(MIMEText(text))
                # attach a file
                part = MIMEBase('application', "octet-stream")
                part.set_payload( open(tarfile_name,"rb").read() )
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition', 'attachment; filename="%s"'\
                        % os.path.basename(tarfile_name))
                message.attach(part)
     
                with open(self.log_path+"/"+unicode(email_id)+"_email_accuse.msg",\
                        'w') as email_msg :
                    email_msg.write(message.as_string())
                 
    def create_moodle_database(self) :
        pass


