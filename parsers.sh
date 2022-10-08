#!/bin/bash

pip3 install -q beautifulsoup4 pandas numpy IPython requests datetime flask nltk pymorphy2  joblib==1.1.0 hdbscan

cd parsers

python3 ./rbc_finances_parser.py &
python3 ./cfo_parser.py &
python3 ./klerk_parser.py &
python3 ./consultant_parser.py &&
wait