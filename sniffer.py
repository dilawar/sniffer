#!/usr/bin/env python2.7
import re
import os 
import argparse 
from database import buildListingDb

if __name__ == "__main__" :

  parser = argparse.ArgumentParser(description="This is code sniffer.")
  parser.add_argument('--config', metavar='filepath'
      , default="~/.snifferrc"
      , help = "Path of configuration file."
      )
  args = parser.parse_args()
  configFile = args.config 

  # check if file exists .
  if not os.path.exists(configFile) :
    print("[E] File {0} does not exists".format(configFile))
    sys.exit(0)
  
  # else parse it.
  import ConfigParser as cfg
  config = cfg.ConfigParser()
  config.read(configFile)
  db = buildListingDb(config) 