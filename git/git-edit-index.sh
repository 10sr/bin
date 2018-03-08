#!/bin/sh
set -eu

# git-edit-index --- Edit staged changes

# Open editor that shows the diff of HEAD and index and apply the result diff.

# Available at: https://github.com/10sr/script/blob/master/git/git-edit-index.sh

# License: Unlicense

do_help(){
    cat <<__EOC__
usage: git edit-index [-h|--help]
__EOC__
}

main(){
    if test $# -eq 1
    then
        if test "$1" = -h -o "$1" = --help
        then
            do_help
            return 0
        else
            echo Unknown option: $1
            return 1
        fi
    fi

    _gitdir="`git rev-parse --git-dir`"
    _difffile="$_gitdir"/EDIT_INDEX.diff

    _defaultindex="$_gitdir"/index
    _workingindex="$_gitdir"/index.edit-index

    git diff --cached --binary --color=never >"$_difffile"

    if test "`du "$_difffile" | cut -f 1`" -eq 0
    then
        echo "Nothing staged." 1>&2
        echo "Aborting" 1>&2
        return 1
    fi

    `git var GIT_EDITOR` "$_difffile"

    if test "`du "$_difffile" | cut -f 1`" -eq 0
    then
        echo "Empty diff." 1>&2
        echo "Aborting" 1>&2
        return 1
    fi

    cp -pf "$_defaultindex" "$_workingindex"
    GIT_INDEX_FILE="$_workingindex" git reset --mixed HEAD
    GIT_INDEX_FILE="$_workingindex" git apply --cached --whitespace=nowarn "$_difffile"
    cp -pf "$_workingindex" "$_defaultindex"
    rm "$_difffile"
}

main "$@"
