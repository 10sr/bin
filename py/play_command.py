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

def bye(arg) :
    print("Bye!")
    exit(0)

def ls(arg) :
    lst = os.listdir()
    for f in lst :
        print(f, end=" ")
    print("")

def cd(arg) :
    try :
        os.chdir(arg)
    except OSError :
        print("OSERROR")

def play(arg) :
    if MPG123 :
        p = MPG123()
        p.set_args([arg])
        p.call()

def shoutcast(arg) :
    m = sc.get_media_from_words(arg)
    play(m)

def print_help(arg) :
    print("Available commands are :")
    for c in commands :
        print(c, end=" ")
    print("")

commands = {
    "ls" : ls,
    "cd" : cd,
    "play" : play,
    "bye" : bye,
    "exit" : bye,
    "help" : print_help,
    "h" : print_help
    }

if sc :
    commands["sc"] = shoutcast
