# JioTV-epg

This repository contains XML guide data for using with JioTv m3u playlist

Features:
1. Contains EPG data from past 7 days to next 2 days
2. Daily updated
3. Contains EPG for all channels

Sample JioTv playlist for using with this EPG
```
#EXTINF:-1 tvg-id="144" tvg-chno="144" tvg-name="Colors HD" tvg-logo="https://jiotv.catchup.cdn.jio.com/dare_images/images/Colors_HD.png" tvg-language="Hindi" group-title="Entertainment", Colors HD 
http://192.168.0.9:3501/getm3u8/144/master.m3u8
```
Usage:
for EPG with past 7 days data:
```
https://github.com/arnab8820/JioTV-epg/raw/main/epg.xml.gz
```

for single day epg data:
```
https://github.com/arnab8820/JioTV-epg/raw/main/epg1d.xml.gz
```