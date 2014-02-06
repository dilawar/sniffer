#!/usr/bin/env python2.7
import re
import os, sys
import argparse
import database
import compare


def main():
    '''
    Main function.
    '''
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
    compare.compare(config, db)
    try:
        dumpResult = config.get("source", "dump_result")
    except Exception as e:
        database.writeContent(config, db)
        database.genrateDOT(config, db)
    if dumpResult == "true":
        database.writeContent(config, db)
        database.genrateDOT(config, db)
    else: pass
  
    
if __name__ == "__main__" :
    main()
