#!/usr/bin/python3

shoutcast = "http://www.shoutcast.com/"
player = "mpg123 -C -v --title -@"

from urllib.request import urlopen
#from xml.dom.minidom import parse
from html.parser import HTMLParser
from subprocess import call
import os

class MyHTMLParser(HTMLParser):
    playlists = []

    def handle_starttag(self, tag, attrs):
        if tag != "a" : return

        pstr = "http://yp.shoutcast.com/sbin/tunein-station.pls"

        for a in attrs :
            if a[0] == "href" and pstr in a[1] :
                self.playlists.append(a[1])

def play(url):
    call(player + " " + url, shell=True)

def search(word):
    return shoutcast + "Internet-Radio/" + word

def get_playlists(url):
    data = urlopen(url)
    parser = MyHTMLParser()
    parser.feed(data.read().decode("utf-8"))
    return parser.playlists


def main():
    url = search("alternative")
    p = get_playlists(url)
    play(p[0])

main()
