#!/usr/bin/env python3

import os
from types import MethodType
try:
    import shoutcast as sc
except ImportError:
    sc = None
try:
    from mpg123 import MPG123, MPG123A
except ImportError:
    MPG123 = None
    MPG123A = None
try:
    from mplayc import MPLAYC, MPLAYCA
except ImportError:
    MPLAYC = None
    MPLAYCA = None

class Controller():
    player = None
    cmds = []

    status = ""

    def __init__(self):
        if MPG123:
            self.player = MPG123()
        else:
            raise ImportError

        self.cmds = [c for c in dir(self) if \
                         isinstance(getattr(self, c, None), MethodType) \
                         and c != "cmd" \
                         and not c.startswith("__")]

    def cmd(self, args):
        if args[0] in self.cmds:
            f = getattr(self, args[0], None)
            f(args)
        else:
            self.status = "%s: Command not found." % args[0]

    def ls(self, args):
        def not_hidden(f):
            return not f.startswith(".")

        lst = os.listdir()
        self.status = "\n".join(filter(not_hidden, lst))

    def cd(self, args):
        arg = " ".join(args[1:])
        print(arg)
        try:
            if arg == "":
                arg = os.path.expanduser("~/")
            os.chdir(arg)
            self.status = arg
        except OSError:
            self.status = "OSERROR"

    def add(self, args):
        self.player.add(args[1:])
        self.status = "Added :\n" + "\n".join(args[1:])

    def new(self, args):
        self.player.new(args[1:])
        self.status = "New playlist :\n" + "\n".join(args[1:])

    def play(self, args):
        self.player.play(args[1:])
        self.status = "Player terminated."

    def set(self, args):
        d = {}
        for p in args[1:]:
            d[p] = True
        self.player.set(d)
        self.status = "Property " + " ".join(args[1:]) + " is set."

    def list(self, args):
        self.status = "Playlist :\n" + "\n".join(self.player.playlist)

    def shoutcast(self, args):
        if not sc:
            self.status = "Shoutcast module not found."
            return
        m = sc.get_media_from_words(" ".join(args))
        if m:
            self.play(m)
            self.status = "Player terminated."
        else:
            self.status = "Url not found."

    def help(self, args):
        self.status = "Available commands are :\n"

class ControllerA(Controller):
    def __init__(self, pipepath, pidfile):
        if MPG123A:
            self.player = MPG123A(pipepath, pidfile)
        else:
            raise ImportError

        self.cmds = [c for c in dir(self) if \
                         isinstance(getattr(self, c, None), MethodType) \
                         and c != "cmd" \
                         and not c.startswith("__")]

    def play(self, args):
        self.player.play(args[1:])
        self.status = self.player.status

    def volumeup(self, args):
        self.player.volume(1)

    def volumedown(self, args):
        self.player.volume(-1)

    def stop(self, args):
        self.player.stop()
        self.status = self.player.status

    def pp(self, args):
        self.player.playpause()
        self.status = self.player.status
