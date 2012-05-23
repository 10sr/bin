#!/usr/bin/python3

shoutcast = "http://www.shoutcast.com/"
player = "mpg123 -C -v --title -@"

from urllib.request import urlopen
from urllib.parse import urlencode
from html.parser import HTMLParser
from subprocess import call
import os
import sys

class MyHTMLParser(HTMLParser):
    playlists = []

    def handle_starttag(self, tag, attrs):
        if tag == "a" : 

            pstr = "http://yp.shoutcast.com/sbin/tunein-station.pls"

            title = ""
            url = ""
            for a in attrs :
                if a[0] == "href" and pstr in a[1] :
                    url = a[1]
                elif a[0] == "title" :
                    title = a[1]
                elif a[0] == "class" and "playimage" in a[1] :
                    # if tag has playimage class ignore the url
                    return

            if url != "" :
                self.playlists.append([title, url])

        elif tag == "class" :
            pass

def play(url):
    call(player + " " + url, shell=True)

def search(word):
    return shoutcast + "Internet-Radio/" + word

def get_playlists(url):
    data = urlopen(url)
    parser = MyHTMLParser()
    parser.feed(data.read().decode("utf-8"))
    return parser.playlists

def choose(stations):
    if len(stations) == 0 :
        print("No station found.")
        return None

    i = 0
    for s in stations :
        i = i + 1
        print("%2d : %s" % (i, s[0]))
    s = input("Input num: ")
    if s == "" :
        return None
    else :
        return stations[int(s) - 1][1]

def main():
    if len(sys.argv) <= 1 : return
    url = search(sys.argv[1])
    p = get_playlists(url)
    # for s in p :
    #     print("%s %s" % (s[0], s[1]))
    u = choose(p)
    if u :
        play(u)

main()
