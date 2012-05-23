#!/usr/bin/python3

shoutcast = "http://www.shoutcast.com/"
player = "mpg123 -C -v --title"

from urllib.request import urlopen
#from xml.dom.minidom import parse
from html.parser import HTMLParser
from subprocess import call
import os

def play(url):
    call(player + " " + media, shell=True)

def search(word):
    url = shoutcast + "Internet-Radio/" + work

def get_playlists(url):
    data = urlopen(url)
    dom = parse(data)
    media = dom.getElementsByClassName("")
