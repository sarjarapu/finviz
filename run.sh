#!/bin/sh
rm -rf local
virtualenv -p /usr/local/bin/python3 local
pip3 install -r requirements.txt
python3 pyFinvizScrapeAnyView.py
