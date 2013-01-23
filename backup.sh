#!/bin/sh

# Very simple backup tool
# copy files into $dst/$timestr
# Usage: backup <args> ...

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
    do_rsync "$@"
}

main "$@"
