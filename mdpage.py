#!/usr/bin/python3

import os
from markdown import Markdown
from io import BytesIO
from sys import argv

class MDPage:
    md = None

    file_list = []
    dir_list = []
    update_list = []

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

    def __init__(self):

        self.md = Markdown()

        l = os.listdir()
        self.file_list = sort([f for f, e in map(os.path.splitext, l) \
                          if not f.startswith(".") and e == ".md" and os.path.isfile(f + e)])
        self.dir_list = sort([d + "/" for d in l if os.path.isdir(d) and not d.startswith(".")])
        self.update_list = [f for f in self.file_list if self.is_updated(f)]

    def is_md_updated(self, f):
        """Return True if html file is not exist or markdown file is newer than htmls"""
        return not os.path.isfile(f + ".html") or self.file_newer(f + ".md", f + ".html")

    def file_newer(self, f1, f2):
        """Return True if f1 is newer than f2"""
        return os.path.getmtime(f1) > os.path.getmtime(f2)

    def is_file_updated(self, file):
        """judge if file is newer than any of html file in filelist"""
        if not os.path.isfile(file) :
            # i think error must be raised in this situation
            return
        
        for f2 in self.file_list :
            if os.path.isfile(f2 + ".html") and file_newer(file, f2 + ".html") :
                self.update_all = True

    def gen_header(self):
        """get header or generate file newly if needed"""
        if os.access(self.header_file, os.R_OK) :
            fd = open(self.header_file, mode="r", encoding="utf-8")
            self.header = fd.read()
            fd.close()
        else :
            fd = open(self_header_file, mode="w", encoding="utf-8")
            fd.write(self.header_def)
            fd.close()

    def gen_footer(self):
        """get footer or generate file newly if needed"""
        if os.access(self.footer_file, os.R_OK) :
            fd = open(self.footer, mode="r", encoding="utf-8")
            self.footer = fd.read()
            fd.close()
        else :
            fd = open(self.footer, mode="w", encoding="utf-8")
            fd.write(self.footer_def)
            fd.close()

    def gen_menu(self):
        """generate menu ul"""
        s = "<ul class=\"menu\">\n"

        for f in self.dirlist :
            s = s + "<li><a href=\"%s/index.html\">%s</a><br /></li>\n" % (f, f) # this <br /> seems to be unnecessary
        for f in self.filelist :
            s = s + "<li><a href=\"%s.html\">%s</a><br /></li>\n" % (f, f)

        s = s + "</ul>\n"

        self.menu = s

    def update_file_list(self):
        """judge if file is newly created or removed sinse last make and update file list if needed"""

        if os.access(self.list_file, os.R_OK) :
            fd = open(self.list_file, mode="r", encoding="utf-8")
            oldlist = fd.read().split("\n")[:-1]
            fd.close()
            if set(oldlist) == set(self.file_list + self.dir_list) :
                return

        self.update_all = True
        fd = open(self.list_file, mode="w", encoding="utf-8")
        for d in self.dir_list :
            fd.write(d + "\n")
        for f in self.file_list :
            fd.write(f + "\n")
        fd.close

    def update_filelist(self):


        

def make_file_list():
    """Return list of md file without .md extension"""
    l = os.listdir()
    return [f for f, e in map(os.path.splitext, l) \
                if not f.startswith(".") and e == ".md" and os.path.isfile(f + e)]

def make_dir_list():
    """return list of directory name"""
    l = os.listdir()
    return [d + "/" for d in l if os.path.isdir(d) and not d.startswith(".")]

def is_updated(f):
    """Return True if html file is not exist or markdown file is newer than htmls"""
    return not os.path.isfile(f + ".html") or file_newer(f + ".md", f + ".html")

def file_newer(f1, f2):
    """Return True if f1 is newer than f2"""
    return os.path.getmtime(f1) > os.path.getmtime(f2)

def update_list_file(flist, dlist):
    """return True if file is added or removed since last make.
    if file list is updated, write the list to file."""
    listfile = ".file.lst"

    if os.access(listfile, os.R_OK) :
        fd = open(listfile, mode="r", encoding="utf-8")
        oldlist = fd.read().split("\n")[:-1]
        fd.close()
        if set(oldlist) == set(flist + dlist) :
            return False

    fd = open(listfile, mode="w", encoding="utf-8")
    for d in dlist :
        fd.write(d + "\n")
    for f in flist :
        fd.write(f + "\n")
    fd.close
    return True

def gen_menu(flist, dlist):
    s = "<ul class=\"menu\">\n"

    flist.sort()
    dlist.sort()

    for f in dlist :
        s = s + "<li><a href=\"%s/index.html\">%s</a><br /></li>\n" % (f, f)
    for f in flist :
        s = s + "<li><a href=\"%s.html\">%s</a><br /></li>\n" % (f, f)

    s = s + "</ul>\n"
    return s

def get_header(f):

    if os.access(f, os.R_OK) :
        fd = open(f, mode="r", encoding="utf-8")
        s = fd.read()
        fd.close()
    else :
        s = """<?xml version="1.0" encoding="UTF-8"?>
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
        fd = open(f, mode="w", encoding="utf-8")
        fd.write(s)
        fd.close()

    return s

def get_footer(f):

    if os.access(f, os.R_OK) :
        fd = open(f, mode="r", encoding="utf-8")
        s = fd.read()
        fd.close()
    else :
        s = """</body>
</html>
"""
        fd = open(f, mode="w", encoding="utf-8")
        fd.write(s)
        fd.close()

    return s

def is_file_updated(f, flist):
    if not os.path.isfile(f) : return False

    for f2 in flist:
        if os.path.isfile(f2 + ".html") and file_newer(f, f2 + ".html") :
            return True

    return False

def gen_html(flist, dlist):
    """generate html file from file list"""

    headerfile = ".header.html"
    footerfile = ".footer.html"
    header = get_header(headerfile)
    footer = get_footer(footerfile)

    if update_list_file(flist, dlist) :
        print("File list updated.")
        uplist = flist
    elif is_file_updated(headerfile, flist):
        print("Header file updated.")
        uplist = flist
    elif isp_file_updated(footerfile, flist):
        print("Footer file updated.")
        uplist = flist
    else :
        uplist = [f for f in flist if is_updated(f)]

    menu = gen_menu(flist, dlist)

    md = Markdown()
    for f in uplist :
        tmp = BytesIO()
        md.convertFile(input=f + ".md", output=tmp, encoding="utf-8")
        #print(tmp.getvalue().decode("utf-8"))
        htmlfd = open(f + ".html", mode="w", encoding="utf-8")
        htmlfd.write(header.format(name=f))
        htmlfd.write(menu)
        htmlfd.write("<div class=\"content\">\n")
        htmlfd.write(tmp.getvalue().decode("utf-8"))
        htmlfd.write("\n</div>\n")
        htmlfd.write(footer.format(name=f))
        tmp.close()
        htmlfd.close()
        print("Update %s.html." % f)

def main():
    # for f in make_file_list():
    #     print(f)
    #     if is_updated(f):
    #         print("%s updated." % f)
    fl = make_file_list()
    dl = make_dir_list()
    gen_html(fl, dl)
    if argv[1] == "make" :
        pass
    elif argv[1] == "check" :
        pass
    elif argv[1] == "help" :
        pass
    elif argv[1] == "force" :
        pass

main()
