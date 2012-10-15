"""
    iitb_moodle.py
    Author : Dilawar Singh
    Institute : IIT Bombay
    Email : dilawar@ee.iitb.ac.in
    Log : Created on Feb 16, 2012

    ABOUT : This module fetch assignements from moodle course page as specified
    in its configuration file .moodlerc which must be located in user home
    folder. See this file for options.

                                        """
import re
import mechanize, urllib, urllib2
import sys, os, shutil, getpass, glob, subprocess

class IitbMoodle():

    """ A python application to access moodle and download data from it.
    """
    def __init__(self):
        print("Initializing moodle ... ")
        self.br = mechanize.Browser( factory=mechanize.RobustFactory())
        self.br.set_handle_equiv(False)
        self.br.set_handle_robots(False)
        self.br.set_handle_referer(False)
        self.br.set_handle_redirect(True)
        self.br.set_debug_redirects(True)
        self.br.set_debug_responses(False)
        self.br.set_debug_http(False)
        self.br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=2)
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux 1686; en-US;\
            rv:1.9.0.1) Gecko/201171615 Ubuntu/11.10-1 Firefox/3.0.1')]
    
    def set_proxy(self):
        self.br.set_proxies({})

    def read_configuration(self):
        """ This function reads a config file and set the values needed for
        making a successfull connection to Moodle.
        """
        print("Reading configuration file ...")
        self.url = ''
        self.username = ""
        self.password = ""
        self.course_key = ""
        self.activity_name = ""
        self.activities = []
        self.num_assignment = 0;
        self.root_dir = "./Moodle";
        self.proxy = "false"
        self.extract = 'true'
        self.language = 'vhdl'
        self.regex = ''
        self.compile = 'false'
        self.compare = 'false'
        self.download = 'true'
        self.autotest = 'false'
        self.cxx = ''
        home = os.environ['HOME']
        path = home+"/.moodlerc"
        if os.path.isfile(path) :
            f = open(path, 'r')
        else :
            print "File .moodlerc does not exists in your home folder. \
            Existing..."
            sys.exit(0)

        for line in f :
            if line[0] == '#' :
                pass

            elif line.split() == "" :
                pass
            
            else :
                (key, val) = line.split("=")

                if key.split()[0] == 'url' :
                    self.url = val.split()[0]
                
                elif key.split()[0] == 'username' :
                    self.username = val.split()[0]
                

                elif key.split()[0] == 'password' :
                    self.password = ' '.join(val.split())
                    if self.password == '':
                        self.password=getpass.getpass()

                elif key.split()[0] == 'course' :
                    val = ' '.join(val.split())
                    self.course_key = val

                elif key.split()[0] == 'autotest' :
                    val = ' '.join(val.split())
                    self.autotest = val

                elif key.split()[0] == 'activities' :
                    val = ' '.join(val.split())
                    self.activity_name = val

                elif key.split()[0] == 'activity' :
                   val = ' '.join(val.split())
                   self.activities.append(val)
               
                elif key.split()[0] == 'download' :
                   self.download = val.split()[0] 
                
                elif key.split()[0] == 'downloaddir' :
                   self.root_dir = val.split()[0]
                
                elif key.split()[0] == 'extract' :
                   self.extract = val.split()[0]
                
                elif key.split()[0] == 'proxy' :
                   self.proxy = val.split()[0]

                elif key.split()[0] == 'language' :
                   self.language = val.split()[0]

                elif key.split()[0] == 'regex' :
                   self.regex = val.split()[0]

                elif key.split()[0] == 'compare' :
                   self.compare = val.split()[0]

                elif key.split()[0] == 'compile' :
                   self.compile = val.split()[0]

                elif key.split()[0] == 'cxx' :
                   self.cxx = val.split()[0]

                else :
                     print "Unknow configuration variable {0}..  Ignoring.".format(key.split()[0])


    def make_connection(self):
        if self.proxy == "true" :
            print("Acquiring proxy variables from environment ...")
        else :
            print("Ignoring proxy variables...")
            self.set_proxy()

        print("Logging into Moodle ..")
        res = self.br.open(self.url)
        # select the form and login
        assert self.br.viewing_html()

        form_id = 0;
        for i in self.br.forms():
            id = i.attrs.get('id') 
            id = id.lower()
            if id.find("login") == 0 :
                #select form 1 which is used for login.
                self.br.select_form(nr = form_id)
                self.br.form['username'] = self.username
                self.br.form['password'] = self.password
                self.br.submit()
                print(" |- Submitting login form ...")
                res = self.br.response()
                res_html = res.get_data()
            else:
                form_id = form_id + 1;

    def get_course_page(self):

        # We can handle both course name and id.
        if self.course_key.isdigit() == False :
            self.course = self.br.follow_link(text_regex=self.course_key)
            course_url = self.course.geturl()
            [url, id ] = course_url.split('id=')
            self.course_id = id
        else :
            self.course = self.br.follow_link(url_regex=r"course.*"+self.course_key)
            course_url = self.course.geturl()
            self.course_id = self.course_key 

        print(" |- Acquiring course page ...")

    def goto_main_activity(self):
        self.activity_id = []
        if self.download == 'true':
            print (" |- Acquiring link of activity ... ")
            #print self.activity_name
            print self.br.geturl()
            #print self.br.title()
            #for link in self.br.links() :
            #    print link.text, link.url
            activity_res = self.br.follow_link(text_regex=self.activity_name)
            assert self.br.viewing_html()
            print self.br.title()
            print self.br.geturl()
            
            for act in self.activities :
                act_res = self.br.follow_link(text_regex=act)
                act_url = act_res.geturl()
                [url, act_id] = act_url.split('id=')
                self.activity_id.append(act_id)
                view_act_res = self.br.follow_link(text_regex=r".*(Download all).*")
                print("Successfully downloaded data for this activity!")
                self.br.open(activity_res.geturl())
            else:
                print("Option variable \"Download\" is not true")

    def fetch_activity_links(self, link_res):
        self.user_dict = dict()
        """ Fetch user_id from the links. """
        for link in self.br.links(url_regex="course="+self.course_id):
            user_url = link.url
            [url, user_course_id] = user_url.split("id=")
            [user_id, rest] = user_course_id.split("&course")
            self.user_dict[user_id] = [link.text,""]

        """ For each user, fetch its assignement, if submitted. """
        for user in self.user_dict.keys():
            for link in self.br.links(url_regex=user):
                file_format = ['.tar', '.gz', '.zip', '.rar', '.7z', '.bz']
                found = False;
                for format in file_format:
                    if link.url.endswith(format) == True:
                        found = True
                        ''' Only update the url. '''
                        self.user_dict[user][1] =  link.url
                        self.num_assignment = self.num_assignment + 1

                    else:
                        found = False

    
    def download_data(self) :
        self.dir = "./Moodle"
        self.goto_main_activity()

    def download_files(self, act) :
        down_dir = self.root_dir +"/"+act
        if not os.path.exists(down_dir) :
            os.makedirs(down_dir)
        print(" |- Setting download directory to " + down_dir)
        for user in self.user_dict.keys() :
            if self.user_dict[user] == '':
                print('No submission found for {1}'.format(user))
            else :
                url = self.user_dict[user][1]
                if url == '':
                    pass
                else:
                    temp_dir = down_dir+"/"+self.user_dict[user][0]
                    
                    if not os.path.exists(temp_dir):
                        os.makedirs(temp_dir)
                    else:
                        print(" ** WARNING ** Path already exists.. Deleting ..")
                        if os.path.isdir(temp_dir):
                            shutil.rmtree(temp_dir) # remove dir
                            os.makedirs(temp_dir) # and create new one
                        else:
                            os.remove(temp_dir) # remove file.
                            os.makedirs(temp_dir) # create dir

                    print("Downloading submission of  "+self.user_dict[user][0])
                    loc = self.br.retrieve(url)[0]
                    shutil.move(loc,temp_dir) 
                    if self.extract == 'true':
                        self.extract_asssignments(temp_dir)
                    else:
                        pass

    def extract_asssignments(self, dir):
        
        path = dir
        if not os.path.isdir(path):
            shutil.rmtree(dir)
        
        os.chdir(path)
        listing = glob.glob(path+'/*gz')
        for file in listing:
            print " |- Extracting archive ...{0}".format(file)
            subprocess.call(["tar", "xzvf", file], stdout=subprocess.PIPE)

        listing = glob.glob(path+'/*bz')
        for file in listing:
            print " |- Extracting archive ...{0}".format(file)
            subprocess.call(["tar", "xjvf", file], stdout=subprocess.PIPE)

        listing = glob.glob(path+'/*zip')
        for file in listing:
            print " |- Extracting archive ...{0}".format(file)
            subprocess.call(["unzip", "-o", file], stdout=subprocess.PIPE)

        listing = glob.glob(path+'/*rar')
        for file in listing:
            print " |- Extracting archive ...{0}".format(file)
            subprocess.call(["unrar", "x", "-o+", file], stdout=subprocess.PIPE)
                   
        listing = glob.glob(path+'/*tar')
        for file in listing:
            print " |- Extracting archive ...{0}".format(file)
            subprocess.call(["tar", "xvf", file], stdout=subprocess.PIPE)
         

