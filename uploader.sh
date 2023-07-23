#!/bin/bash

cd /mnt/data/JioTV-epg
python3 start.py
gzip -f ./epg.xml
git add epg.xml.gz
git commit -m "daily epg update"
git push origin main
