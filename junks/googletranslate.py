#!/usr/bin/env python
#coding:utf-8
import urllib
import simplejson

def translate(query, frm="en", to="ja"):
    query = query.encode("utf-8")
    data = {"q":query, "v":"1.0", "hl":"ja", "langpair":"%s|%s" % (frm, to),}
    f = urllib.urlopen("http://ajax.googleapis.com/ajax/services/language/translate", urllib.urlencode(data))
    ret = simplejson.loads(f.read())
    return ret["responseData"]["translatedText"]

print(translate("Dog"))
