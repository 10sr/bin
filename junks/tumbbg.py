#!/usr/bin/env python
import os.path as p
import subprocess
import urllib
import lxml.html

todir = p.expanduser("~/Pictures/background/tmbr/")
tumburl = "http://10sr.tumblr.com/"

def setbg(filename):
    subprocess.Popen(["gconftool-2", "--type", "string", "--set", "/desktop/gnome/background/picture_filename", imgfilename])
    subprocess.Popen(["gconftool-2", "--type", "string", "--set", "/desktop/gnome/background/picture_options", "scaled"])
    return

tumbhtml = urllib.urlopen(tumburl).read()
root = lxml.html.fromstring(tumbhtml)
# content = root.get_element_by_id('content')
img = root.xpath("//div[@class='post']//img[@class='image']")
imgurl = img[0].attrib["src"]

imgbasename = p.basename(imgurl)
imgfilename, header = urllib.urlretrieve(imgurl, p.join(todir, imgbasename))

print(imgurl)
setbg(imgfilename)
