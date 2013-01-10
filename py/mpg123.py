#!/usr/bin/env python3

from subprocess import call, Popen, PIPE
import os
import signal as sig

class MPG123():
    program = "mpg123"
    opts = ["-C", "-v", "--title"]
    playlist = []

    repeat = False
    shuffle = False
    random = False

    status = ""
    args = []

    def add(self, playlist):
        self.playlist.extend(playlist)
        self.status = "Added :\n%s" % "\n".join(playlist)

    def new(self, playlist):
        self.playlist = list(playlist)
        self.status = "New playlist :\n%s" % "\n".join(playlist)

    def set(self, args):
        if "repeat" in args:
            self.repeat = True
        if "shuffle" in args:
            self.shuffle = True
        if "random" in args:
            self.random = True
        # for p in args:
        #     if p.startswith("no"):
        #         val = False
        #         p = p[2:]
        #     else:
        #         val = True
        #     m =
        self.status = "Property %s was set." % " ".join(args)

    def gen_args(self, args=[], playlist=[]):
        self.args = [self.program]
        self.args.extend(self.opts)

        if self.repeat:
            self.args.extend(["--loop", "-1"])
        if self.shuffle:
            self.args.append("--shuffle")
        if self.random:
            self.args.append("--random")
        self.args.extend(args)

        if playlist == None or len(playlist) == 0:
            self.args.extend(self.playlist)
        else:
            self.args.extend(playlist)

    def play(self, playlist=None):
        self.gen_args(playlist=playlist)
        call(self.args)

class MPG123A(MPG123):
    p = None
    status = "Not running."     # must not be empty string
    pipe = ""
    pidfile = ""

    def __init__(self, pipepath, pidfile):
        MPG123.__init__(self)
        self.pipe = pipepath
        self.pidfile = pidfile

    def play(self, playlist=None):
        if self.p:
            self.status = "Already playing!"
            return
        if len(self.playlist) == 0 and len(playlist) == 0:
            self.status = "Playlist is empty!"
            return

        self.gen_args(args=["-C" , "--fifo", self.pipe], playlist=playlist)
        try:
            os.mkfifo(self.pipe)
        except OSError as e:
            if e.errno == 17:
                pass
            else:
                raise

        self.p = Popen(self.args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

        f = open(self.pidfile, 'w')
        f.write("%d" % self.p.pid)
        f.close()

        self.status = "Start playing."

    def send_command(self, s):
        if self.p:
            # f = open(self.pipe, mode="w")
            # f.write(s)
            # f.close()
            fd = os.open(self.pipe, os.O_WRONLY | os.O_NDELAY)
            os.write(fd, bytes(s))
            os.close(fd)
            return True
        else:
            return False

    def playpause(self):
        if self.send_command("s"):
            self.status = "Play/Pause player."
            self.p = None
        else:
            self.status = "Player not running."

    def stop(self):
        if self.send_command("q"):
            self.status = "Stopped player."
            os.unlink(self.pipe)
            self.p = None
        else:
            self.status = "Player not running."

    def volume(self, arg):
        pass

    def kill(self):
        if self.p:
            os.kill(self.p.pid, sig.SIGTERM)
            self.status = "Player killed."
        else:
            self.status = "Player not running."

    def clear(self):
        self.args = []
        self.status = "Cleared playlist."
