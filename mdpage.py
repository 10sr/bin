#!/usr/bin/python3

import os
from markdown import Markdown
from io import BytesIO
from sys import argv

# import locale
# locale.setlocale(locale.LC_ALL, '')
# code = locale.getpreferredencoding()

class MDPage:
    md = None

    file_list = []
    dir_list = []
    updated_list = []

    header_file = ".header.html"
    footer_file = ".footer.html"
    header = None
    footer = None
    header_def = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<meta http-equiv="Content-Style-Type" content="text/css" />
<!-- <link rel="stylesheet" href="style.css" type="text/css" /> -->
<title>{name} | title</title>
</head>
<body>
<h1 class="title">{name} | <a href="index.html">title</a></h1>
<h2 class="subtitle">subtitle</h2>
"""
    footer_def = """</body>
</html>
"""

    list_file = ".files.lst"

    menu = ""

    update_all = False
    header_updated = False
    footer_updated = False
    filelist_updated = False

    def __init__(self):

        self.md = Markdown()

        l = os.listdir()
        self.file_list = [f for f, e in map(os.path.splitext, l) \
                          if not f.startswith(".") and e == ".md" and os.path.isfile(f + e)]
        self.file_list.sort()

        self.dir_list = [d + "/" for d in l if os.path.isdir(d) and not d.startswith(".")]
        self.dir_list.sort()

        self.updated_list = [f for f in self.file_list if self.is_md_updated(f)]

    def is_md_updated(self, f):
        """Return True if html file is not exist or markdown file is newer than htmls"""
        return not os.path.isfile(f + ".html") or self.is_file_newer(f + ".md", f + ".html")

    def is_file_newer(self, f1, f2):
        """Return True if f1 is newer than f2"""
        return os.path.getmtime(f1) > os.path.getmtime(f2)

    def is_file_updated(self, file):
        """judge if file is newer than any of html file in filelist. file must be exist."""
        for f in self.file_list :
            if os.path.isfile(f + ".html") and self.is_file_newer(file, f + ".html") :
                return True

        return False

    def gen_header(self):
        """get header or generate file newly if needed"""
        if os.access(self.header_file, os.R_OK) :
            fd = open(self.header_file, mode="r", encoding="utf-8")
            self.header = fd.read()
            fd.close()
        else :
            fd = open(self.header_file, mode="w", encoding="utf-8")
            fd.write(self.header_def)
            fd.close()

    def gen_footer(self):
        """get footer or generate file newly if needed"""
        if os.access(self.footer_file, os.R_OK) :
            fd = open(self.footer_file, mode="r", encoding="utf-8")
            self.footer = fd.read()
            fd.close()
        else :
            fd = open(self.footer_file, mode="w", encoding="utf-8")
            fd.write(self.footer_def)
            fd.close()

    def gen_menu(self):
        """generate menu ul"""
        s = "<ul class=\"menu\">\n"

        if "index" in self.file_list :
            s = s + "<li><a href=\"%s.html\">%s</a></li>\n" % ("index", "index")
        for f in self.dir_list :
            s = s + "<li><a href=\"%sindex.html\">%s</a></li>\n" % (f, f)
        for f in self.file_list :
            if f != "index" :
                s = s + "<li><a href=\"%s.html\">%s</a></li>\n" % (f, f)

        s = s + "</ul>\n"

        self.menu = s

    def update_filelist(self):
        """update file list"""
        fd = open(self.list_file, mode="w", encoding="utf-8")
        for d in self.dir_list :
            fd.write(d + "\n")
        for f in self.file_list :
            fd.write(f + "\n")
        fd.close

    def is_filelist_updated(self):
        """judge if file is newly created or removed sinse last make. list file must be exist."""
        fd = open(self.list_file, mode="r", encoding="utf-8")
        oldlist = fd.read().split("\n")[:-1]
        fd.close()
        if set(oldlist) == set(self.file_list + self.dir_list) :
            return False
        else :
            return True

    def make(self):
        self.check()
        self.run()

    def check(self):
        if not os.path.isfile(self.header_file) :
            print("Header file does not exist.")
            self.header_updated = True
        elif self.is_file_updated(self.header_file) :
            print("Header file is updated.")
            self.header_updated = True

        if not os.path.isfile(self.footer_file) :
            print("Footer file does not exist.")
            self.footer_updated = True
        elif self.is_file_updated(self.footer_file) :
            print("Footer file is updated.")
            self.footer_updated = True

        if not os.path.isfile(self.list_file) :
            print("List file does not exist.")
            self.filelist_updated = True
        elif self.is_filelist_updated() :
            print("File list is updated.")
            self.filelist_updated = True

    def print_updated(self):
        for f in self.updated_list:
            print("%s.md updated." % f)

    def force(self):
        self.check()
        self.update_all = True
        self.run()

    def run(self):
        """do check() before call this"""
        if self.update_all or self.header_updated or self.footer_updated or self.filelist_updated :
            print("Updating all files.")
            fl = self.file_list
        else :
            fl = self.updated_list

        if not fl :
            print("No file to update.")
            return

        if self.update_all or self.filelist_updated :
            self.update_filelist()

        self.gen_header()
        self.gen_footer()
        self.gen_menu()

        for f in fl :
            tmp = BytesIO()
            self.md.convertFile(input=f + ".md", output=tmp, encoding="utf-8")
            # print(tmp.getvalue().decode("utf-8"))
            htmlfd = open(f + ".html", mode="w", encoding="utf-8")
            htmlfd.write((self.header or self.header_def).replace("{name}", f)) # format() cant be used because str might contain unexpected { or }
            htmlfd.write(self.menu)
            htmlfd.write("<div class=\"content\">\n")
            htmlfd.write(tmp.getvalue().decode("utf-8"))
            htmlfd.write("\n</div>\n")
            htmlfd.write((self.footer or self.footer_def).replace("{name}", f))
            tmp.close()
            htmlfd.close()
            print("Update %s.html." % f)

def help():
    pass

def main():
    mp = MDPage()
    if len(argv) == 1 or argv[1] == "check" :
        mp.check()
        mp.print_updated()
    elif argv[1] == "update" :
        mp.make()
    elif argv[1] == "force" :
        mp.force()
    else :
        print("Invalid argument: %s." % argv[1])
        help()

main()
