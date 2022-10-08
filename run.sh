#!/bin/bash

pip3 install -q beautifulsoup4 pandas numpy IPython requests datetime

start=`date +%s`

python3 ./rbc_finances_parser.py &
python3 ./cfo_parser.py &
python3 ./klerk_parser.py &
python3 ./consultant_parser.py &&
wait

end=`date +%s`
runtime=$((end-start))
echo "Parsing runtime: $runtime"