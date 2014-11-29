#!/usr/bin/env python

import subprocess as sp

def main(argv):
    files = []
    options = []
    canoption = True
    for a in argv[1:]:
        if canoption and a == "--":
            canoption = False
        elif canoption and a.startswith("-"):
            options.append(a)
        else:
            files.append(a)
            # canoption = False

    git_ls_command = ["git", "ls-files", "-z", "--"] + files
    wc_command = ["xargs", "-0", "wc"] + options

    p_git_ls = sp.Popen(git_ls_command, stdout=sp.PIPE)
    p_wc = sp.Popen(wc_command, stdin=p_git_ls.stdout)
    p_git_ls.wait()
    return p_wc.wait()


if __name__ == "__main__":
    import sys
    main(sys.argv)
