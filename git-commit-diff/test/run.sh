#!/bin/sh
set -xe

dir="$(realpath "$(dirname "$0")")"
top="$dir"/..

_with_rep_prepared(){
    cwd=`pwd`
    tmp="$top"/tmp
    mkdir -p "$tmp"
    cd "$tmp"
    git init
    eval "$@"
    cd "$cwd"
    rm -rf "$tmp"
}

_with_rep_prepared '
git rev-parse --show-toplevel
touch a.txt
git add a.txt
git commit -m First\ commit
"$top"/git-commit-diff.sh -m Second\ commit "$dir"/a.diff
'
