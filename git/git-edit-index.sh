#!/bin/sh
set -e

# git-edit-index --- Edit staged changes

# Open editor that shows the diff of HEAD and index and apply the result diff.

# Available at: https://github.com/10sr/script/blob/master/git-commit-diff/git-commit-diff.sh

do_help(){
    cat <<__EOC__
usage: git edit-index [-h|--help]
__EOC__
}

main(){
    if test "$1" = -h -o "$1" = --help
    then
        do_help
        return 0
    fi

    _gitdir="`git rev-parse --git-dir`"
    _difffile="$_gitdir"/EDIT_INDEX

    git diff --cached --binary --color=never >"$_difffile"

    `git var GIT_EDITOR` "$_difffile"

    if test "`du "$_difffile" | cut -f 1`" -eq 0
    then
        echo "Empty diff."
        echo "Abort."
        return 1
    fi

    # TODO: Restore index state if failed to apply patch
    git reset --mixed HEAD
    git apply --cached "$_difffile"
    rm "$_difffile"
}

main "$@"
