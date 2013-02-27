#!/bin/sh -x

if test $# -lt 2
then
    echo "$0 filename binname"
    exit 1
fi

dir="`pwd`"
dst="$HOME/.local/bin"

mkdir -p "$dst"

path="$dir/$1"
name="$2"
ln -s "$path" "$dst/$name"
