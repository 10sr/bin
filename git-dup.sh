#!/bin/sh

# Duplicate work tree with git-new-workdir.
# $ git dup [<branch>]

# This creates new working directory for current repository named
# "_<repname>_<branch>" in current directory.
# If <branch> is omittted current branch name is used.
# If branch does not exist, creates it newly.

__error(){
    echo "$1" 1>&2
    echo "Abort." 1>&2
    exit 1
}

git rev-parse --git-dir 1>/dev/null || exit $?

nw="`which git-new-workdir 2>/dev/null`"

if test -z "$nw"
then
    __error "fatal: $0 requires \`git-new-workdir'"
fi

branch="$1"

if test -z "$branch"
then
    branch="`git symbolic-ref --short HEAD`"
fi

if test -z "$branch"
then
    echo "I cannot get current branch name (currently on detached HEAD?)."
    echo "Try \`master' branch."
    if git rev-parse --verify master >/dev/null 2>&1
    then
        branch=master
    else
        __error "\`master' branch not found"
    fi
fi

if ! git rev-parse --verify "$branch" >/dev/null 2>&1
then
    echo "Branch named \`$branch' does not exist."
    echo "Create branch \`$branch'."
    git branch "$branch"
fi

repname="$(basename "$(git rev-parse --show-toplevel)")"

"$nw" . "_${repname}_${branch}" "$branch"
