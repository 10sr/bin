#!/bin/sh

help(){
    cat <<'__EOC__' 2>&1
backup: backup [file ...]

Very simple backup tool by create directory named$dst/$timestr and copy files
into it.
__EOC__
}

test -z "$dst" && dst="$HOME/.my/backup"
timestr=`date +%Y%m%d-%H%M%S`
dstdir="$dst/$timestr"

do_rsync(){
    mkdir -p $dstdir
    # src=foo/ : copy the contents of this directory
    # src=foo : copy the directory by name
    # these two are same:
    #     rsync -av /src/foo  /dest
    #     rsync -av /src/foo/ /dest/foo

    # if $dstdir already exists and it is a directory
    #     copy files into $dstdir
    # elif $@ is one file ($1)
    #     copy create file named $dstdir with contents of $1
    # else
    #     fail
    rsync -a --stats --progress --human-readable "$@" "$dstdir"
}

main(){
    if test -z "$1"
    then
        help
    else
        do_rsync "$@"
    fi
}

main "$@"
