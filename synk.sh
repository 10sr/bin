#!/bin/sh
set -e

# synk --- Simple File Synchronization Utility

# usage: synk [-h] {push|pull|info}

# Syncronize files in current directory to the pre-defined remote directory
# with the simple commands `synk {pull|push}`.

# First you need to create a file named `.synk.conf`, which is a shellscript.
# This file may contain some variable definitions:
#     remote=[[user]@host:]dir (required):
#         Remote directory to synk files with.
#     rsync_opts:
#         Additional arguments for rsync command.
# The directory containing `.synk.conf` is considered to be the "root" of
# the directory to synk. Even if you issue `synk` in "subdirectories", synk is
# done from the "root" directory.

conf=.synk.conf
rsync_default_opts="--archive --compress --stats --progress --human-readable"
#rsync_default_opts="$rsync_default_opts --list-only"

error(){
    echo "$@" 1>&2
    echo "Abort." 1>&2
    exit 1
}

do_pull(){
    $rsync --exclude "$conf" "$@" "$remote/" "$PWD/"
}

do_push(){
    $rsync --exclude "$conf" "$@" "$PWD/" "$remote/"
}

print_info(){
    true
    #echo "rsync=$rsync"
}

print_help(){
    cat <<__EOC__
usage: synk [-h] {push|pull}
__EOC__
    true
}

find_conf_cd(){
    # Find `.synk.conf`. If not found, go upper and try recursively,
    # then cd to the directory where `.synk.conf` is found.
    # If .synk.conf not found, abort immediately.
    while ! test -r "$PWD/$conf"
    do
        if ! cd ..
        then
            error "$conf not found."
        fi
    done
    echo "Synk directory: $PWD/"
    return
}

main(){
    cmd="$1"
    if test -z "$cmd" -o "$cmd" = help -o "$cmd" = -h
    then
        print_help
        exit 0
    fi
    shift

    find_conf_cd
    . "$conf"
    if test -z "$remote"
    then
        error "remote not set."
    fi

    if expr "$remote" : '^.*:$' >/dev/null
    then
        error "Only host name spedified for remote."
    fi
    echo "Remote directory: $remote/"

    rsync="`command -v rsync`"
    if test -z "$rsync"
    then
        error "rsync not found."
    fi
    #rsync="echo rsync::"

    if test "$cmd" = pull
    then
        do_pull $rsync_default_opts $rsync_opts
    elif test "$cmd" = push
    then
        do_push $rsync_default_opts $rsync_opts
    elif test "$cmd" = info
    then
        print_info
    else
        echo "$cmd: Unknown command"
        print_help
        exit 1
    fi
}

main "$@"
