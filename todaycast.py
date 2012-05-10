#!/usr/bin/python3

url = "http://www3.nhk.or.jp/rj/podcast/rss/english.xml"
player = "mpg123 -C -v --title"

import urllib.request
from xml.dom.minidom import parseString
import subprocess as sp
import os

def get_latest_media(url):
    data = urllib.request.urlopen(url)
    dom = parseString(data.read().decode('utf-8'))
    media = dom.getElementsByTagName("enclosure")[0].getAttribute("url")
    print("Latest %s" % media)
    save_conf(media)

def play(media):
    sp.call(player + " " + media, shell=True)

def save_conf(media):
    conf = os.path.expanduser("~/.config/todaycast.conf")
    if(os.access(conf, os.R_OK)):
        fd = open(conf, mode="r")
        if(fd.readable() and fd.read() == media):
            s = input("Already played! Play again? [y/N]: ")
            if(s != "y"):
                fd.close()
                return
        fd.close()
    fd = open(conf, mode="w+")
    fd.write(media)
    fd.close()
    play(media)

get_latest_media(url)
