#!/usr/bin/env python3

from subprocess import call, Popen, PIPE
import os
import signal as sig

class MPG123() :
    program = "mpg123"
    opts = ["-C", "-v", "--title"]
    plist = []

    repeat = False
    shuffle = False
    random = False

    def add(self, plist) :
        self.plist.extend(plist)

    def new(self, plist) :
        self.plist = list(plist)

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

    def play(self, plist=None) :
        args = [self.program]
        args.extend(self.opts)
        if self.repeat :
            args.extend(["--loop", "-1"])
        if self.shuffle :
            args.append("--shuffle")
        if self.random :
            args.append("--random")
        if plist == None or len(plist) == 0 :
            args.extend(self.plist)
        else :
            args.extend(plist)
        for i in args :
            print(i)
        call(args)

class MPG123A(MPG123) :
    p = None
    status = "Not running."     # must not be empty string
    fifo = "/tmp/mpg123a"

    def play(self) :
        if self.p :
            self.stop()
        if len(self.args) == 0 :
            self.status = "Playlist is empty!"
            return
        opts = self.opts + ["-C" , "--fifo", self.fifo]
        args = [self.program] + opts + [self.args[0]]
        self.p = Popen(args, stdin = PIPE, stdout = PIPE, stderr = PIPE)
        self.status = "Start playing %s." % self.args[0]

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

    def add(self, args) :
        self.args.extend(args)
        self.status = "Added :\n%s" % "\n".join(args)

    def kill(self, args) :
        os.kill(self.p.pid, sig.SIGTERM)
        self.status = "Player killed."

    def playlist(self) :
        self.status = "\n".join(self.args)

    def clear(self) :
        self.args = []
        self.status = "Cleared playlist."
