#!/usr/bin/env python3

import os
from io import BytesIO
from sys import argv, stderr
from string import Template
from time import strftime
from subprocess import call, check_output

try :
    from markdown import Markdown
except ImportError :
    Markdown = None

# import locale
# locale.setlocale(locale.LC_ALL, '')
# code = locale.getpreferredencoding()

class MDPage:
    mdc = None
    hf = None
    fl = None

    cur_time = None

    enc = "utf-8"
    dec = "utf-8"

    menu = ""

    update_all = False

    def __init__(self):

        self.cur_time = strftime("%a, %d %b %Y %H:%M:%S %z")

        self.mdc = MDConv()
        self.hf = HeaderFooter()
        self.fl = FileList()

    def gen_menu(self):
        """generate menu ul"""
        s = "<ul class=\"menu\">\n"

        if "index" in self.fl.file_list :
            s = s + "<li><a href=\"%s.html\">%s</a></li>\n" % ("index", "index")
        for f in self.fl.dir_list :
            s = s + "<li><a href=\"%sindex.html\">%s</a></li>\n" % (f, f)
        for f in self.fl.file_list :
            if f != "index" :
                s = s + "<li><a href=\"%s.html\">%s</a></li>\n" % (f, f)

        s = s + "</ul>\n"

        self.menu = s

    def autoremove(self):
        for f in os.listdir() :
            if not os.path.isdir(f) and f.endswith(".html") and \
                    not f.startswith(".") and \
                    not os.path.splitext(f)[0] in self.file_list :
                print("rm : %s." % f)
                os.remove(f)

    def clean(self) :
        pass

    def make(self):
        self.check()
        self.update()

    def print_updated(self):
        for f in self.fl.updated_list:
            print("%s.md is to be updated." % f)

    def force(self):
        self.check()
        self.update_all = True
        self.update()

    def check(self):
        """only check, do not create any file"""
        self.fl.check_filelist_updated(self.enc)
        self.hf.check_updated(self.fl.file_list)

    def update(self):
        """do check() before call this"""
        if self.mdc.conv == None :
            print("No way to convert md file!", file = stderr)
            return

        if self.update_all or \
                self.fl.updated or \
                self.hf.header.exist == False or \
                self.hf.footer.exist == False or \
                self.hf.header.updated or self.hf.footer.updated :
            print("all files are to be updated.")
            fl = self.fl.file_list
        else :
            fl = self.fl.updated_list

        if self.update_all or self.fl.updated :
            self.fl.update_file(self.dec)

        if not fl :
            print("No file to update.")
            return

        self.hf.set()
        self.gen_menu()

        h_template = Template(self.hf.header.s)
        f_template = Template(self.hf.footer.s)

        for f in fl :
            res = self.mdc.conv(f + ".md", self.enc)
            htmlfd = open(f + ".html", mode="w", encoding=self.dec)
            htmlfd.write(h_template.safe_substitute(name = f, time = self.cur_time))
            htmlfd.write(self.menu)
            htmlfd.write("<div class=\"content\">\n")
            htmlfd.write(res.decode(self.dec))
            htmlfd.write("\n</div>\n")
            htmlfd.write(f_template.safe_substitute(name = f, time = self.cur_time))
            htmlfd.close()
            print("%s.md -> %s.html." % (f, f))

class FileList :
    file_list = []
    dir_list = []
    updated_list = []

    fname = ".files.lst"
    updated = None

    def __init__(self) :
        l = os.listdir()
        self.file_list = [f for f, e in map(os.path.splitext, l) \
                              if not f.startswith(".") and \
                              e == ".md" and os.path.isfile(f + e)]
        self.file_list.sort()

        self.dir_list = [d + "/" for d in l \
                             if os.path.isdir(d) and not d.startswith(".")]
        self.dir_list.sort()

        self.updated_list = [f for f in self.file_list if self.is_md_updated(f)]

    def is_md_updated(self, f):
        """Return True if html file is not exist or markdown file is newer"""
        return not os.path.isfile(f + ".html") or \
            self.is_file_newer(f + ".md", f + ".html")

    def is_file_newer(self, f1, f2):
        """Return True if f1 is newer than f2"""
        return os.path.getmtime(f1) > os.path.getmtime(f2)

    def update_file(self, encoding="utf-8"):
        """update list_file"""
        fd = open(self.fname, mode="w", encoding=encoding)
        for d in self.dir_list :
            fd.write(d + "\n")
        for f in self.file_list :
            fd.write(f + "\n")
        fd.close
        print("%s generated." % self.fname)

    def check_filelist_updated(self, encoding="utf-8"):
        """check if there is any file newly created or removed"""
        if not os.path.isfile(self.fname) :
            print("%s not exist." % self.fname)
            self.updated = True
            return

        fd = open(self.fname, mode="r", encoding=encoding)
        oldlist = fd.read().split("\n")[:-1]
        fd.close()
        if set(oldlist) == set(self.file_list + self.dir_list) :
            self.updated = False
        else :
            self.updated = True
            print("File list was updated.")

class PageTemplate :
    """class for header and footer"""
    fname = None
    defalut = None
    exist = None
    s = None
    updated = None

    def __init__(self, filename, default) :
        self.fname = filename
        self.default = default
        self.check_exist()

    def set(self, encoding="utf-8") :
        """set self.s and create file if none"""
        if self.exist :
            self.read_file(encoding)
        else :
            self.write_file(encoding)
            self.s = self.default

    def check_exist(self) :
        if os.access(self.fname, os.R_OK) :
            self.exist = True
        else :
            self.exist = False
            print("%s not exist." % self.fname)

    def check_updated(self, flist) :
        """judge if file is newer than any of html file in flist"""
        if not self.exist :
            return
        for f in flist :
            if os.path.isfile(f + ".html") and \
                    self.is_file_newer(self.fname, f + ".html") :
                print("%s is updated." % self.fname)
                self.updated = True
                return
        self.updated = False

    def is_file_newer(self, f1, f2):
        """Return True if f1 is newer than f2"""
        return os.path.getmtime(f1) > os.path.getmtime(f2)

    def read_file(self, encoding="utf-8") :
        fd = open(self.fname, mode="r", encoding=encoding)
        self.s = fd.read()
        fd.close()

    def write_file(self, decoding="utf-8") :
        fd = open(self.fname, mode="w", encoding=decoding)
        fd.write(self.default)
        fd.close()
        print("%s generated." % self.fname)

class HeaderFooter :
    header = None
    footer = None

    header_file = ".header.html"
    footer_file = ".footer.html"
    HEADER_DEF = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<!-- <link rel="stylesheet" href="style.css" type="text/css" /> -->
<title>${name} | title</title>
</head>
<body>
<h1 class="title">${name} | <a href="index.html">title</a></h1>
<h2 class="subtitle">subtitle</h2>
"""
    FOOTER_DEF = """</body>
</html>
<!-- Last update : ${time} -->
"""

    def __init__(self) :
        self.header = PageTemplate(self.header_file, self.HEADER_DEF)
        self.footer = PageTemplate(self.footer_file, self.FOOTER_DEF)

    def check_updated(self, flist) :
        self.header.check_updated(flist)
        self.footer.check_updated(flist)

    def set(self) :
        self.header.set()
        self.footer.set()

class MDConv :
    md = None
    md_command = None
    conv = None

    def __init__(self) :
        if Markdown :
            print("Use Markdown python module to convert.")
            self.md = Markdown()
            self.conv = self.conv_py
        else :
            self.md_command = self.check_cmd("markdown.pl") or self.check_cmd("markdown")
            if self.md_command :
                print("Use command %s to onvert." % self.md_command)
                self.conv = self.conv_pl

    def check_cmd(self, command) :
        try :
            check_output([command, "--version"])
            return command
        except OSError :
            return None

    def conv_py(self, input, encoding) :
        """accept filename and return result as a byte string"""
        tmp = BytesIO()
        self.md.convertFile(input = input, output = tmp, encoding = encoding)
        res = tmp.getvalue()
        tmp.close()
        return res

    def conv_pl(self, input, encoding) :
        """accept filename and return result as a byte string"""
        f = open(file = input, encoding = encoding)
        res = check_output(self.md_command, stdin = f)
        f.close()
        return res

def help():
    pass

def main(argv):
    mp = MDPage()
    if len(argv) == 1 or argv[1] == "check" :
        mp.check()
        mp.print_updated()
    elif argv[1] == "update" :
        mp.make()
    elif argv[1] == "force" :
        mp.force()
    elif argv[1] == "autoremove" :
        mp.autoremove()
    elif argv[1] == "clean" :
        mp.clean()
    elif argv[1] == "help" or argv[1] == "--help" :
        help()
    else :
        print("Invalid argument: %s." % argv[1])
        help()

if __name__ == "__main__" :
    main(argv)
