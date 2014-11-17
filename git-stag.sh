#!/bin/sh
set -e

# git stag --- git stash tagging utility

# usage: git stag s[ave] <tagname> [<message>]
#    or: git stag t[ag] <stash>|<num> <tagname> [<message>]
#    or: git stag a[pply] <tagname>

# This script creates stashes with tags attached and easily attach tags to
# existing stash objects.
# It enables 'naming' tags with optional messages, and pushing stashes to remote
# repositories.

# In the first form, new tagged stashes is created from current working tree
# without adding it to usual stash list.
# The second form enables to attach tags to existing stashes easily.
# Only numbers are required for specifying stash, or usual form like `stash@{0}
# can be used too.
# In the third form, apply stash to current working tree and index.
# Actuallly this is just an alias for `git stash apply`, since `stash apply`
# accepts any commit object which looks like a stash.



##############################################################################
# Auther: 10sr
# URL: https://github.com/10sr/script/blob/master/git-stag.sh
# LICENSE: Unlicense: http://unlicense.org

# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <http://unlicense.org/>
##############################################################################

__warn(){
    echo "$1" 1>&2
}

mk_stag(){
    # mk_stag <tagname> <sha1> [<message>]
    if test -n "$3"
    then
        git tag "$1" "$2" -am "$3"
    else
        git tag "$1" "$2"
    fi
    echo "Stag created as tag \`$1' from $2."
}

do_save(){
    if test -z "$1"
    then
        __warn "Tag name not spedified."
        do_help
        return 1
    fi
    if test -n "$2"
    then
        commitobj=`git stash create "$2"`
    else
        commitobj=`git stash create`
    fi
    mk_stag "$1" $commitobj "$2"
    git reset --hard
}

do_tag(){
    # do_tag <stash>|<num> <tagname> [<message>]
    if test -z "$1" || test -z "$2"
    then
        __warn 'Both stash number and tagname are required.'
        do_help
        return 1
    elif expr "$1" : "^\[0-9][0-9]*\)$" >/dev/null 2>&1
    then
        # $1 is num
        stash_ref=stash@{$1}
    elif expr "$1" : "^stash@.*$" >/dev/null 2>&1
    then
        stash_ref=$1
    else
        __warn "$1: Invalid stash name"
        do_help
        return 1
    fi

    mk_stag "$2" `git rev-parse "$stash_ref"` "$3"
}

do_apply(){
    if test -z "$1"
    then
        do_help
        return 1
    else
        git stash apply "$1"
    fi
}

do_help(){
    cat <<__EOC__
usage: git stag s[ave] <tagname> [<message>]
   or: git stag t[ag] <stash>|<num> <tagname> [<message>]
   or: git stag a[pply] <tagname>
__EOC__
}

main(){
    if test -z "$1"
    then
        _cmd=help
    else
        _cmd="$1"
        shift
    fi

    # Currently only first letter of $1 is used
    case "$_cmd" in
        s*) _cmd=save;;
        t*) _cmd=tag;;
        a*) _cmd=apply;;
    esac


    if command -v do_"$_cmd" >/dev/null
    then
        do_"$_cmd" "$@"
    else
        __warn "$_cmd: unknown option"
        do_help
        return 1
    fi
}

main "$@"
