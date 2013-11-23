#!/bin/sh

# @(#) Very simple backup tool using rsync

help(){
    cat <<'__EOC__' 1>&2
save: usage: save [-h] [-d <dst>] <file> ...
    Very simple backup tool using rsync.
    <dst> can be like `/path/to/dir', `user@host:' or `user@host:/path/to/dir'.
__EOC__
}

debug=

do_rsync(){
    # do_rsync dstdir files ...
    dstdir="$1"
    shift

    if expr "$dstdir" : '.*:' >/dev/null
    then
        host="$(expr "$dstdir" : '\(.*\):')"
        dir="$(expr "$dstdir" : '.*:\(.*\)$')"
        printf "Creating $dir in $host..."
        $debug ssh "$host" mkdir -p "$dir"
        echo "done"
    else
        $debug mkdir -p "$dstdir"
    fi

    # src=foo/ : copy the contents of this directory
    # src=foo : copy the directory by name
    # these two are same:
    #     rsync -av /src/foo  /dest
    #     rsync -av /src/foo/ /dest/foo

    # if $dstdir ends with /
    #     create dir $dstdir if not exists and copy files into $dstdir
    # if $dstdir already exists and it is a directory
    #     copy files into $dstdir
    # elif $@ is one file ($1)
    #     copy create file named $dstdir with contents of $1
    # else
    #     fail
    echo "Start copying files into \"$dstdir\"."
    $debug rsync --archive --compress --stats --progress --human-readable \
        "$@" "$dstdir"
}

find_dst(){
    # find_dst dst
    dst="$1"
    if test -z "$dst"
    then
        dst="$SAVE_PATH"
    fi

    defdst=".var/saved"
    if test -z "$dst"
    then
        dstdir="$HOME/$defdst"
    elif expr "$dst" : '.*:$' >/dev/null
    then
        # only hostname is specified
        dstdir="$dst$defdst"        # host:.var/saved
    else
        dstdir="$dst"
    fi
    timestr=`date +%Y%m%d-%H%M%S`
    dstdir="$dstdir/$timestr/"

    echo "$dstdir"
}


dst=
while getopts hd: opt
do
    case "$opt" in
        d) dst="$OPTARG";;
        h) help; exit 1;;
        *) help; exit 1;;
    esac
done

shift `expr $OPTIND - 1`

if test -z "$1"
then
    echo No file specified. 1>&2
    help
    exit 1
fi

dstdir="`find_dst "$dst"`"

do_rsync "$dstdir" "$@"
