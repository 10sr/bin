#!/usr/bin/python3

shoutcast = "http://www.shoutcast.com/"
player = "mpg123 -C -v --title -@"

from urllib.request import urlopen
from urllib.parse import urlencode
from html.parser import HTMLParser
from subprocess import call
import sys

class MyHTMLParser(HTMLParser):
    stations = []
    current = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a" : 

            pstr = "http://yp.shoutcast.com/sbin/tunein-station.pls"

            title = ""
            url = ""
            for a in attrs :
                if a[0] == "href" and a[1].startswith(pstr) :
                    url = a[1]
                elif a[0] == "title" :
                    title = a[1]
                elif a[0] == "class" and "playimage" in a[1] :
                    # if tag has playimage class ignore the url
                    return

            if url != "" :
                self.stations.append({"title" : title, "url" : url})

        elif tag == "div" :
            for a in attrs :
                if a[0] != "class" : continue

                if a[1] == "playingtext" : 
                    self.current = "recent"
                elif a[1] == "dirgenre" :
                    self.current = "genre"
                elif a[1] == "dirlistners" : # wrong spelling!
                    self.current = "listeners"
                elif a[1] == "dirbitrate" :
                    self.current = "bitrate"
                elif a[1] == "dirtype" :
                    self.current = "type"

    def handle_data(self, data):
        if data == "" or  self.current == "" : return

        if "Recently played:" in data or "Now playing:" in data or "Now Playing:" in data:
            return

        ix = len(self.stations) - 1
        self.stations[ix][self.current] = data.strip(" \n")
        self.current = ""

def play(url):
    call(player + " " + url, shell=True)

def search(word):
    return shoutcast + "Internet-Radio/" + word

def get_stations(url):
    data = urlopen(url)
    parser = MyHTMLParser()
    parser.feed(data.read().decode("utf-8"))
    return parser.stations

def choose(stations):
    if len(stations) == 0 :
        print("No station found.")
        return None

    i = 0
    for s in stations :
        if i >= 5 : break
        i = i + 1
        print("%2d : %s | %s" % (i, s["title"], s["recent"]))
        print ("     ", end = "")
        for k, v in s.items() :
            if k != "url" and k != "title" and k != "recent" :
                print("%s : %s  " % (k, v), end = "")
        print("")
        print("")

    s = input("Input num: ")
    if s == "" or not s.isdigit() :
        return None
    else :
        return stations[int(s) - 1]["url"]

def main():
    if len(sys.argv) <= 1 : return
    url = search(sys.argv[1])
    s = get_stations(url)
    # print(s[0])
    u = choose(s)
    if u :
        play(u)

main()
