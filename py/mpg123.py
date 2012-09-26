#!/usr/bin/env python3

from subprocess import call, Popen, PIPE
import os
import signal as sig

class MPG123() :
    program = "mpg123"
    opts = ["-C", "-v", "--title"]
    args = []

    def set_args(self, args) :
        self.args = list(args)

    def call(self) :
        args = [self.program] + self.opts + self.args
        for i in args :
            print(i)
        call(args)

class MPG123A(MPG123) :
    p = None
    status = "Not running."     # must not be empty string

    def call(self) :
        pass

    def play(self) :
        if self.p :
            self.stop()
        if len(self.args) == 0 :
            self.status = "Playlist is empty!"
            return
        opts = self.opts + ["-C" , "-q"]
        args = [self.program] + opts + [self.args[0]]
        self.p = Popen(args, stdin = PIPE, stdout = PIPE, stderr = PIPE)
        self.status = "Start playing %s." % self.args[0]

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
