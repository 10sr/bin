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

# Basic work
_with_rep_prepared sh -xes <<__EOC__
git rev-parse --show-toplevel
touch a.txt
git add a.txt
git commit -m 'First commit'
sh -x '$top'/git-commit-diff.sh -m 'Commit by git-commit-diff' '$dir'/a.diff
# Check the commit message
git log --oneline -n 1 | grep 'Commit by git-commit-diff$'
__EOC__

# Work when working directory and index are dirty
_with_rep_prepared sh -xes <<__EOC__
git rev-parse --show-toplevel
touch a.txt
git add a.txt
git commit -m 'First commit'
echo eee >>a.txt
git add a.txt
echo fff >>a.txt
sh -x '$top'/git-commit-diff.sh -m 'Commit by git-commit-diff' '$dir'/a.diff
# Check the commit message
git log --oneline -n 1 | grep 'Commit by git-commit-diff$'
git status -s
__EOC__
