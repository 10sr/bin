#!/usr/bin/env python3

shoutcast = "http://www.shoutcast.com/"
player = "mpg123 -C -v --title"
#player = "mocp -l"

from urllib.request import urlopen
from urllib.parse import quote as urlquote
from html.parser import HTMLParser
import sys

try:
    import readline
except ImportError:
    print("Module readline not available.")
    readline = None
else:
    if "libedit" in readline.__doc__:
        readline.parse_and_bind("bind ^I rl_complete")
    else:
        readline.parse_and_bind("tab: complete")

try:
    from mpg123 import MPG123
except ImportError:
    MPG123 = None
    from subprocess import call

class ScParser(HTMLParser):
    stations = []
    current = ""
    pls_url = "http://yp.shoutcast.com/sbin/tunein-station.pls"

    def __init__(self):
        HTMLParser.__init__(self)
        self.stations = []
        self.current = ""

    def handle_starttag(self, tag, attrs):
        if tag == "a":


            title = ""
            url = ""
            for a in attrs:
                if a[0] == "href" and a[1].startswith(self.pls_url):
                    url = a[1]
                elif a[0] == "title":
                    title = a[1]
                elif a[0] == "class" and "playimage" in a[1]:
                    # if tag has playimage class ignore the url
                    return

            if url != "":
                self.stations.append({"title" : title, "url" : url})

        elif tag == "div":
            for a in attrs:
                if a[0] != "class" : continue

                if a[1] == "playingtext":
                    self.current = "recent"
                elif a[1] == "dirgenre":
                    self.current = "genre"
                elif a[1] == "dirlistners" : # wrong spelling!
                    self.current = "listeners"
                elif a[1] == "dirbitrate":
                    self.current = "bitrate"
                elif a[1] == "dirtype":
                    self.current = "type"

    def handle_data(self, data):
        if data == "" or  self.current == "" : return

        if "Recently played:" in data or "Now playing:" in data or "Now Playing:" in data:
            return

        ix = len(self.stations) - 1
        self.stations[ix][self.current] = data.strip(" \n")
        self.current = ""

def play(url):
    """play url file"""
    if url:
        if MPG123:
            p = MPG123()
            p.new([url])
            p.play()
        else:
            call(player + " " + track, shell=True)

def get_media_url(url):
    """get media url from pls"""
    if not url:
        return None
    data = urlopen(url)
    track = parse_pls(data)
    data.close()
    return track

def parse_pls(file):
    lines = file.read().decode("utf-8").splitlines()
    for line in lines:
        if line.startswith("File1="):
            return line.replace("File1=", "")
    return None

def gen_search(words):
    """generate search url from words"""
    if words == "":
        print("No search word given.", file=sys.stderr)
        return None
    else:
        return shoutcast + "Internet-Radio/" + urlquote(words)

def get_stations(words):
    url = gen_search(words)
    if not url:
        return None
    data = urlopen(url)
    parser = ScParser()
    parser.feed(data.read().decode("utf-8"))
    data.close()
    return parser.stations

def choose(stations):
    if len(stations) == 0:
        print("No station found.")
        return None

    for i, s in enumerate(stations):
        if i >= 5 : break
        i = i + 1
        print("{:>2} : {} | {}".format(i, s["title"], s["recent"]))
        print ("     ", end = "")
        for k, v in s.items():
            if k != "url" and k != "title" and k != "recent":
                print("{} : {}  ".format(k, v), end = "")
        print("")
        print("")

    s = input("Input num: ")
    if s == "" or not s.isdigit():
        return None
    else:
        return stations[int(s) - 1]["url"]

def get_media_from_words(words):
    s = get_stations(words)
    if not s:
        return None
    u = choose(s)
    t = get_media_url(u)
    return t

def main(argv):
    if len(argv) > 1:
        w = " ".join(argv[1:])
        t = get_media_from_words(w)
        play(t)
    else:
        while True:
            w = input("Enter query: ")
            if w == "":
                break
            t = get_media_from_words(w)
            play(t)

if __name__ == '__main__':
    main(sys.argv)
