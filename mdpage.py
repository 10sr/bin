#!/usr/bin/python3

import os
from markdown import Markdown
from io import BytesIO

def make_file_list():
    """Return list of md file without .md extension"""
    l = os.listdir()
    return list((f for f, e in map(os.path.splitext, l) \
                if not f.startswith(".") and e == ".md" and os.path.isfile(f + e)))

def make_dir_list():
    """return list of directory name"""
    l = os.listdir()
    return list((d + "/" for d in l if os.path.isdir(d) and not d.startswith(".")))

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
    str = "<ul class=\"menu\">\n"

    flist.sort()
    dlist.sort()

    for f in dlist :
        str = str + "<li><a href=\"%s\">%s</a><br /></li>\n" % (f, f)
    for f in flist :
        str = str + "<li><a href=\"%s.html\">%s</a><br /></li>\n" % (f, f)

    str = str + "</ul>\n"
    return str

def gen_header(file):

    if os.access(file, os.R_OK) :
        fd = open(file, mode="r", encoding="utf-8")
        str = fd.read()
        fd.close()
    else :
        str = """<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<head>
<title>{name}</title>
</head>
<body>
"""

    return str

def gen_footer(file):

    if os.access(file, os.R_OK) :
        fd = open(file, mode="r", encoding="utf-8")
        str = fd.read()
        fd.close()
    else :
        str = """</body>
</html>
"""

    return str

def is_file_updated(f, flist):
    if not os.path.isfile(f) : return False

    for f2 in flist:
        if os.path.isfile(f2 + ".html") and file_newer(f, f2 + ".html") :
            return True

    return False

def gen_html(flist, dlist):
    """generate html file from file list"""
    md = Markdown()

    headerfile = ".header.html"
    footerfile = ".footer.html"

    if update_list_file(flist, dlist) :
        print("file list updated.")
        uplist = flist
    elif is_file_updated(headerfile, flist):
        print("header file updated.")
        uplist = flist
    elif is_file_updated(footerfile, flist):
        print("footer file updated.")
        uplist = flist
    else :
        uplist = (f for f in flist if is_updated(f))

    header = gen_header(headerfile)
    footer = gen_footer(footerfile)
    menu = gen_menu(flist, dlist)

    for f in uplist :
        print("updating %s.html." % f)
        out = BytesIO()
        #out = open(f + ".html")
        out.write(header.format(name=f).encode("utf-8"))
        out.write(menu.encode("utf-8"))
        md.convertFile(input=f + ".md", output=out, encoding="utf-8")
        out.write(footer.format(name=f).encode("utf-8"))
        #print(out.getvalue().decode("utf-8"))
        htmlfd = open(f + ".html", mode="w", encoding="utf-8")
        htmlfd.write(out.getvalue().decode("utf-8"))
        htmlfd.close()
        out.close()

def main():
    # for f in make_file_list():
    #     print(f)
    #     if is_updated(f):
    #         print("%s updated." % f)
    fl = make_file_list()
    dl = make_dir_list()
    gen_html(fl, dl)

main()
