#!/bin/bash
set +e 
if [ "$1" == "x" ]; then
  echo "Deleting old compilation..."
  rm -f *.c
  rm -f *.so
fi
python setup.py  build_ext --inplace
./sniffer.py --config ./snifferrc
