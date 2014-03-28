#!/usr/lib/env python3

import os
from glob import glob
from shlex import split as shsplit

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

class PlayPrompt():
    s = ""
    r = []
    cmds = []

    _c = []

    def __init__(self, Controller):
        if readline:
            readline.set_completer(self.completer)
        self.cmds = Controller.cmds

    def completer(self, text, state):
        def com_filter(array, text):
            return [s for s in array if s.startswith(text)]

        b = readline.get_line_buffer()
        for c in self.cmds:
            if b.startswith(c + " "):
                if state == 0:
                    self._c = com_filter(os.listdir(text or "."), text)
                if state < len(self._c):
                    return self._c[state]
                else:
                    return None

        if state == 0:
            self._c = com_filter(self.cmds, text)
        if state < len(self._c):
            return self._c[state] + " "
        else:
            return None

    def parse_input(self):
        if self.s == "":
            self.r = []
            return

        args = shsplit(self.s)
        eargs = [args[0]]
        for a in args[1:]:
            g = glob(a)
            if len(g) == 0:
                eargs.extend([a])
            else:
                eargs.extend(g)
        self.r = eargs
        return

    def input(self):
        home = os.getenv("HOME")
        d = os.getcwd()
        if home != "":
            d = d.replace(home, "~")

        try:
            self.s = input("PLAY %s $ " % d)
        except (EOFError, KeyboardInterrupt):
            self.s = "bye"
            print("")

        self.parse_input()
        return self.r
