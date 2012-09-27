#!/usr/bin/env python3

import os
try :
    import shoutcast as sc
except ImportError :
    sc = None
try :
    from mpg123 import MPG123
except ImportError :
    MPG123 = None

def ls(arg) :
    lst = os.listdir()
    for f in lst :
        if not f.startswith(".") :
            print(f)

def cd(arg) :
    try :
        if arg == "" :
            arg = os.path.expanduser("~/")
        os.chdir(arg[1])
    except OSError :
        print("OSERROR")

def play(arg) :
    if MPG123 :
        p = MPG123()
        p.set_args(arg[1:])
        p.call()

def shoutcast(arg) :
    m = sc.get_media_from_words(" ".join(arg))
    if m :
        play(m)

def print_help(arg) :
    print("Available commands are :")
    for c in commands :
        print(c)

commands = {
    "ls" : ls,
    "cd" : cd,
    "play" : play,
    "help" : print_help,
    "h" : print_help
    }

if sc :
    commands["sc"] = shoutcast
