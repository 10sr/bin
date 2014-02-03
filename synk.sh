#!/bin/sh
set -e

# synk --- Simple File Synchronization Utility

# usage: synk [-h] {push|pull|info} [<option> ...]

# Synchronize files in current directory to the pre-defined remote directory
# with simple commands `synk {pull|push}`.

# First you need to create a file named `.synk.conf`, which is a shellscript.
# This file may contain some variable definitions:
#     remote=[[user]@host:]dir: (required)
#         Remote directory to synk files with.
#     rsync_opts:
#         Additional options for rsync command.
# The directory containing `.synk.conf` is considered to be the "root" of
# the directory to synk. Even if you issue `synk` in "subdirectories", synk is
# done from the "root" directory.

# `synk pull` fetch files from the remote directory defined in `.synk.conf`
# and `synk push` do the otherwise.
# Remaining options are directly passed to rsync.


##############################################
# synk --- Simple File Synchronization Utility

# Auther: 10sr
# URL: https://github.com/10sr/script/blob/master/synk.sh
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


conf=.synk.conf
# rsync_default_opts="--archive --compress --stats --progress --human-readable"
rsync_default_opts="--archive --progress --compress --human-readable"
#rsync_default_opts="$rsync_default_opts --list-only"

msg(){
    echo ":: $*"
}

error(){
    msg "$@" 1>&2
    msg "Abort." 1>&2
    exit 1
}

do_rsync(){
    msg Running \"rsync "$@"\"
    "$rsync" "$@"
}

# NOTE: when calling do_rsync DST should be the last argument, otherwise
# unexpected path might be used as DST given by user (from $@).
do_pull(){
    msg Pull: "$remote/ => $local/"
    do_rsync --exclude "/$conf" "$@" "$remote/" "$local/"
}

do_push(){
    msg Push: "$local/ => $remote/"
    do_rsync --exclude "/$conf" "$@" "$local/" "$remote/"
}

print_info(){
    msg "Synk Root: $local/"
    msg "Remote   : $remote/"
    msg "rsync    : $rsync"
}

print_help(){
    cat <<__EOC__
usage: synk [-h] {push|pull|info} [<option> ...]

commands:
    push: send files to remote directory
    pull: fetch files from remote directory
    info: print info about local and remote directory

Remaining options are directly passed to rsync.
__EOC__
}

find_conf_cd(){
    # Find `.synk.conf`. If not found, go upper and try again,
    # then cd to the directory where `.synk.conf` is found.
    # If .synk.conf not found, abort immediately.
    _lastdir="$PWD"
    while ! test -r "$PWD/$conf"
    do
        cd ..
        if test "$_lastdir" = "$PWD"
        then
            error "$conf not found."
        fi
        _lastdir="$PWD"
    done
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
    local="$PWD"
    . "$local/$conf"
    # msg "Synk Root: $local/"

    if test -z "$remote"
    then
        error "remote not set."
    fi

    if expr "$remote" : '^.*:$' >/dev/null
    then
        error "Only host name spedified as remote."
    fi

    # here remove last slash, which is added explicitly later
    remote="`echo "$remote" | sed -e 's|/$||'`"
    # msg "Remote directory: $remote/"

    rsync="`command -v rsync`"
    if test -z "$rsync"
    then
        error "rsync not found."
    fi
    #rsync="echo rsync::"

    if test "$cmd" = pull
    then
        do_pull $rsync_default_opts $rsync_opts "$@"
    elif test "$cmd" = push
    then
        do_push $rsync_default_opts $rsync_opts "$@"
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
