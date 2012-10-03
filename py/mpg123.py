#!/usr/bin/env python3

from subprocess import call, Popen, PIPE
import os
import signal as sig

class MPG123() :
    program = "mpg123"
    opts = ["-C", "-v", "--title"]
    plist = []

    args = []

    repeat = False
    shuffle = False
    random = False

    status = ""

    def add(self, plist) :
        self.plist.extend(plist)
        self.status = "Added :\n%s" % "\n".join(plist)

    def new(self, plist) :
        self.plist = list(plist)
        self.status = "New playlist :\n%s" % "\n".join(plist)

    def set(self, args) :
        if "repeat" in args :
            self.repeat = True
        if "shuffle" in args :
            self.shuffle = True
        if "random" in args :
            self.random = True
        # for p in args :
        #     if p.startswith("no") :
        #         val = False
        #         p = p[2:]
        #     else :
        #         val = True
        #     m =

    def gen_args(self, args=[], plist=[]) :
        self.args = [self.program]
        self.args.extend(self.opts)

        if self.repeat :
            self.args.extend(["--loop", "-1"])
        if self.shuffle :
            self.args.append("--shuffle")
        if self.random :
            self.args.append("--random")
        self.args.extend(args)

        if plist == None or len(plist) == 0 :
            self.args.extend(self.plist)
        else :
            self.args.extend(plist)

    def play(self, plist=None) :
        self.gen_args(plist=plist)
        for i in self.args :
            print(i)
        call(self.args)

class MPG123A(MPG123) :
    p = None
    status = "Not running."     # must not be empty string
    fifo = "/tmp/mpg123a"

    def play(self, plist=None) :
        if len(self.plist) == 0 and len(plist) == 0 :
            self.status = "Playlist is empty!"
            return
        self.gen_args(args=["-C" , "--fifo", self.fifo], plist=plist)
        self.p = Popen(args)
        self.status = "Start playing."

    def send_command(s) :
        pass

    def playpause(self) :
        pass

    def stop(self) :
        if self.p :
            print("stopping player.")
            self.p.stdin.write(b"q")
            # self.p.communicate("q".encode())
            # self.p.terminate()
            print("stooped player.")
            self.status = "Stopped player."
        else :
            self.status = "Player not running."

    def volume(self, arg) :
        pass

    def kill(self, args) :
        os.kill(self.p.pid, sig.SIGTERM)
        self.status = "Player killed."

    def clear(self) :
        self.args = []
        self.status = "Cleared playlist."
