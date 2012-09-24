#!/usr/bin/env python3

from subprocess import call

class MPG123() :
    program = "mpg123"
    opts = ["-C", "-v", "--title"]
    args = None

    def set_args(self, args) :
        self.args = list(args)

    def call(self) :
        args = [self.program] + self.opts + self.args
        for i in args :
            print(i)
        call(args)
