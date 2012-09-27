#!/usr/bin/env python3

import os
from types import MethodType
try :
    import shoutcast as sc
except ImportError :
    sc = None
try :
    from mpg123 import MPG123
except ImportError :
    MPG123 = None

class Command() :
    player = None

    status = ""

    def __init__(self) :
        if MPG123 :
            self.player = MPG123()

    def cmd(self, args) :
        f = getattr(self, args[0], None)
        if isinstance(f, MethodType) \
                and args[0] != "cmd" \
                and args[0] != "__init__" :
            f(args)
        else :
            self.status = "%s: Command not found." % args[0]

    def ls(self, args) :
        def not_hidden(f) :
            return not f.startswith(".")

        lst = os.listdir()
        self.status = "\n".join(filter(not_hidden, lst))

    def cd(self, args) :
        try :
            if args == "" :
                args = os.path.expanduser("~/")
            os.chdir(args[1])
            self.status = args[1]
        except OSError :
            print("OSERROR")

    def play(self, args) :
        self.player.play()

    def shoutcast(self, args) :
        m = sc.get_media_from_words(" ".join(args))
        if m :
            play(m)

    def help(self, args) :
        self.status = "Available commands are :\n" 
