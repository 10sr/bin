#!/usr/bin/python3

import os
from markdown import Markdown
from io import BytesIO

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
    elif is_file_updated(footerfile, flist):
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

main()
