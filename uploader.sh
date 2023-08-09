#!/bin/bash

#cd /home/arnab/JioTV-epg
python3 start.py
gzip -f ./epg.xml
gzip -f ./epg1d.xml
git add epg.xml.gz
git add epg1d.xml.gz
git commit -m "daily epg update"
git push origin main
