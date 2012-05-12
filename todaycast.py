#!/usr/bin/python3

feed = "http://www3.nhk.or.jp/rj/podcast/rss/english.xml"
player = "mpg123 -C -v --title"

from urllib.request import urlopen
from xml.dom.minidom import parseString
import subprocess as sp
import os

def get_latest_media(url):
    data = urlopen(url)
    dom = parseString(data.read().decode('utf-8'))
    media = dom.getElementsByTagName("enclosure")[0].getAttribute("url")
    print("Latest media is %s." % media)
    return media

def play(media):
    sp.call(player + " " + media, shell=True)

def conf_file():
    env = "XDG_CONFIG_HOME"
    if(env in os.environ):
        return os.environ[env] + "/todaycast.conf"
    else:
        return os.path.expanduser("~/.todaycast.conf")

def check_new(media):
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

def main():
    media = get_latest_media(feed)
    if(check_new(media)):
        play(media)
        save_conf(media)

main()
