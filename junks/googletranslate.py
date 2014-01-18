#!/usr/bin/env python
#coding:utf-8
import urllib
import json

URL = ("https://www.googleapis.com/language/translate/v2"
       "?key={key}&target={target}&q={query}")
KEY = "AIzaSyDrtCSkX5VZ3bxXz96Mur9P6olw96UYndw"

def translate(query, frm="en", to="ja"):
    query = query.encode("utf-8")
    data = {
        "query": query,
        "key": KEY,
        "target": "ja"
    }
    f = urllib.urlopen(URL.format(**data))
    result = f.read()
    print(result)
    ret = json.loads(result)
    return ret["data"] and ret["data"]["translations"][0]["translatedText"]

print(translate("Dog"))
