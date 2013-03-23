"""
    moodle.py
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

class MoodleBrowser():

    """ A python application to access moodle and download data from it.
    """
    def __init__(self, config):
        print("Initializing moodle ... ")
        self.config = config
        self.username = config.get('moodle', 'username')
        self.password = config.get('moodle', 'password')
        self.proxy = config.get('moodle', 'proxy')
        self.url = config.get('moodle', 'url')
        self.download = config.get('moodle', 'download')
        self.course_key = config.get('moodle', 'course')
        self.activity_type = config.get('moodle', 'activity_type')
        if len(self.password.strip()) == 0 :
          self.password = getpass.getpass("Your moodle password :")
        self.activity = config.get('moodle', 'activity').split(";")

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
    
    def make_connection(self):
        if self.proxy == "true" :
          print("TODO : Acquiring proxy variables from environment ...")
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
        print(" |- Acquiring course page ...")
        self.make_connection()
        if self.course_key.isdigit() == False :
            self.course = self.br.follow_link(text_regex=self.course_key)
            course_url = self.course.geturl()
            #print course_url
            [url, id ] = course_url.split('id=')
            self.course_id = id
        else :
            self.course = self.br.follow_link(url_regex=r"course.*"+self.course_key)
            course_url = self.course.geturl()
            self.course_id = self.course_key 

    def goto_main_activity(self):
      self.get_course_page()
      self.activity_id = []
      if self.download == 'true':
        print (" |- Acquiring link of activity ... ")
        #print self.activity_name
        #print self.br.geturl()
        #print self.br.title()
        activityLinks = dict()
        for act in self.activity :
          act = act.strip()
          for link in self.br.links() :
            if re.search(self.activity_type, link.url) :
              pat = re.compile(act.strip(), re.IGNORECASE)
              if pat.search(link.text) :
                print("[I] Found activity {0} : {1}".format(self.activity_type,
                  act))
                activityLinks[act] = link
        self.fetch_activity(activityLinks)

    def fetch_activity(self, activityDict) :
      for act in activityDict :
        link = activityDict[act]
        self.br.follow_link(link)
        assign = self.br.follow_link(text_regex=r"View/grade\s+all\s+submission")
        assignLinks = self.br.links()
        # go to alphabatically 
        toConsume = list()
        for al in assignLinks :
          if re.match(".*\&id=\d+\&page\=\d$", al.url) :
            toConsume.append(al)
        linksToDownload = set()
        while(len(toConsume) > 0) :
          lToC = toConsume.pop()
          total = 0
         
          print("Following {0}".format(lToC.url))
          self.br.follow_link(lToC)
         
          lls = self.br.links()
          for al in lls :
            pat = re.compile(r"pluginfile\.php\/(?P<cid>\d+)\/.+\/.+(?P<uid>\d+)"+\
               "\/.+\?forcedownload\=1", re.IGNORECASE)
            m = pat.search(al.url)
            if m :
              total += 1
              linksToDownload.add(al.url)
          # go back.
          print("Page {0} : {1}, {2}".format(len(toConsume), total,
            len(linksToDownload)))
          self.br.back()

        print("Total {0} assignments can be downloaded."\
           .format(len(linksToDownload)))
        

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
         

if __name__=="__main__" :
  import argparse 
  import ConfigParser as cfg
  parser = argparse.ArgumentParser(description="Moodle")
  parser.add_argument('--config', metavar='file', required=True
      , help="Config file")
  args = parser.parse_args()
  configFilePath = args.config 
  if not os.path.exists(configFilePath) :
    print("Config file {0} does not exists".format(configFilePath))
    sys.exit(0)
  config = cfg.RawConfigParser()
  config.read(configFilePath)
  print config.get('moodle', 'activity')
  moodle = MoodleBrowser(config)
  moodle.goto_main_activity()

  
