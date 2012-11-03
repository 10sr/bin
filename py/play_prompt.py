#!/usr/lib/env python3

import os
from glob import glob
from shlex import split as shsplit

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    if "libedit" in readline.__doc__ :
        print("libedit used.")
        readline.parse_and_bind("bind ^I rl_complete")
    else :
        readline.parse_and_bind("tab: complete")

class PlayPrompt() :
    s = ""
    r = []

    def __init__(self, Controller) :
        pass

    def parse_input(self) :
        if self.s == "" :
            self.r = []
            return

        args = shsplit(self.s)
        eargs = [args[0]]
        for a in args[1:] :
            g = glob(a)
            if len(g) == 0 :
                eargs.extend([a])
            else :
                eargs.extend(g)
        self.r = eargs
        return

    def input(self) :
        home = os.getenv("HOME")
        d = os.getcwd()
        if home != "" :
            d = d.replace(home, "~")

        try :
            self.s = input("PLAY %s $ " % d)
        except (EOFError, KeyboardInterrupt) :
            self.s = "bye"
            print("")
        self.parse_input()
        return self.r
