#!/bin/sh

help(){
    cat <<'__EOC__' 2>&1
backup: Usage: backup <files> ...

Very simple backup tool
Copy files into $dst/$timestr
__EOC__
}

test -z "$dst" && dst="$HOME/.my/backup"
timestr=`date +%Y%m%d-%H%M%S`
dstdir="$dst/$timestr"

do_rsync(){
    mkdir -p $dstdir
    # mkdir -p $dstbase
    # src=foo/ : copy the contents of this directory
    # src=foo : copy the directory by name
    # these two are same:
    #     rsync -av /src/foo  /dest
    #     rsync -av /src/foo/ /dest/foo
    # rsync never changed the name of copied file?
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
