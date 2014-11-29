#!/bin/sh

# git rstash --- git stash for remote

# usage: git rstash save <tagname> [<message>]
#    or: git rstash add <tagname> <stash>|<num>
#    or: git rstash apply <tagname>

# Basically there is no way to send stash to remote repository directly.
# But you can send tags, and tags can be used for any object including stashes.
# rstash add tags for stash objects so that they can be sent to remote
# repository.

# In the first form, new rstash is created from current working tree without
# adding it to usual stash list.
# In the second form, new rstash is created from existing stash object.
# Only number can be used for specifying stash, or usual form like `stash@{0}
# can be used too.
# In the third form, apply rstash to current working tree and index.

__warn(){
    echo "$1" 1>&2
}

mk_rstash(){
    # mk_rstash <tagname> <sha1>
    git tag "$1" "$2" && \
        echo "Rstash created as tag \`$1' from $2."
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
        commitobj=`git stash create "$2"` || return 1
    else
        commitobj=`git stash create` || return 1
    fi
    mk_rstash "$1" $commitobj
    git reset --hard
}

do_add(){
    if test -z "$1" || test -z "$2"
    then
        do_help
        return 1
    elif expr "$2" : "^\[0-9][0-9]*\)$" >/dev/null 2>&1 # $1 is num
    then
        stash_ref=stash@{$1}
    elif expr "$2" : "^stash@.*$" >/dev/null 2>&1
    then
        stash_ref=$1
    else
        __warn "$2: Invalid stash name"
        do_help
        return 1
    fi

    mk_rstash "$1" `git rev-parse "$stash_ref"`
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
usage: git rstash save <tagname> [<message>]
   or: git rstash add <tagname> <stash>|<num>
   or: git rstash apply <tagname>
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

    if type do_"$_cmd" >/dev/null 2>&1
    then
        do_"$_cmd" "$@"
    else
        __warn "$_cmd: unknown option"
        do_help
        return 1
    fi
}

main "$@"
