#!/usr/bin/env python2.7
import re
import os, sys
import argparse
import database
import compare

if __name__ == "__main__" :

  parser = argparse.ArgumentParser(description="This is code sniffer.")
  parser.add_argument('--config'
          , metavar='filepath'
          , default=os.environ['HOME']+"/.config/sniffer/config"
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
  db = database.buildListingDb(config)
  if config.get("source", "compare") == "true" :
      compare.compare(config, db)
      database.dump(config, db)
  if config.get("source", "analyze_result") == "true" :
      database.writeContent(config, db)
      database.genrateDOT(config, db)
