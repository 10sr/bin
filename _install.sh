#!/bin/sh

if test $# -lt 2
then
    echo "$0: usage: $0 <filename> <binname>"
    exit 1
fi

dst="$HOME/.local/bin"

mkdir -p "$dst"

path="`readlink -f "$1"`"
name="$2"
ln -s "$path" "$dst/$name"
echo "\`$name' installed."
