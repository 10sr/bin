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
    print("Latest media is %s." % media)
    if(check_conf(media)):
        play(media)
        save_conf(media)

def play(media):
    sp.call(player + " " + media, shell=True)

def conf_file():
    return os.path.expanduser("~/.config/todaycast.conf")

def check_conf(media):
    "test if media is new"
    conf = conf_file()
    if(os.access(conf, os.R_OK)):
        fd = open(conf, mode="r")
        last = fd.read() if fd.readable() else ""
        fd.close()
        if(last == media):
            s = input("Already played! Play again? [y/N]: ")
            if(s == "y"):
                return True
            else:
                return False
        else:
            return True
    else:
        return True

def save_conf(media):
    fd = open(conf_file(), mode="w+")
    fd.write(media)
    fd.close()

get_latest_media(url)
