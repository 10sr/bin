#!/bin/sh

help(){
    cat <<'__EOC__' 2>&1
backup: backup [file ...]

Very simple backup tool by create directory named $dst/$timestr and copy files
into it.
__EOC__
}

debug=

defdst=".my/backup"
if test -z "$dst"
then
    dstdir="$HOME/$defdst"
elif expr "$dst" : '.*:$' >/dev/null
then
    # only hostname is specified
    dstdir="$dst./$defdst"
else
    dstdir="$dst"
fi
timestr=`date +%Y%m%d-%H%M%S`
dstdir="$dstdir/$timestr/"

do_rsync(){
    # if expr "$dstdir" : '.*:' >/dev/null
    # then
    #     host="$(expr "$dstdir" : '\(.*\):')"
    #     dir="$(expr "$dstdir" : '.*:\(.*\)$')"
    #     printf "Creating $dir in $host..."
    #     $debug ssh "$host" mkdir -p "$dir"
    #     echo "done"
    # else
    #     $debug mkdir -p "$dstdir"
    # fi

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
    $debug rsync -a --stats --progress --human-readable "$@" "$dstdir"
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
