#!/bin/sh
set -e

# git commit-diff --- Make a commit from a diff

# usage: git commit-diff [-m|--message <msg>] [--] [<patch>...]

# Options:

#   -m|--message <msg>
#       Use the given <msg> as the commit message.
#   <patch>...
#       The files to read the patch from. - can be used to read from the
#       standard input.



# Possible options:
# I think these options can be potentially used

# usage: git commit-diff [-R|--reverse] [-p<n>] [-C<n>] [--unidiff-zero]
#                        [--no-add] [--allow-binary-replacement|--binary]
#                        [--exclude=<path-pattern>] [--include=<path-pattern>]
#                        [--ignore-space-change|--ignore-whitespace]
#                        [--whitespace=<action>]
#                        [--inaccurate-eof] [-v|--verbose]
#                        [--recount] [--directory=<root>]

#                        [(--reuse-message|--reedit-message|--fixup|--squash) <commit>]
# TODO: -C is used both from git-apply and git-commit
#                        [--reset-author] [--author=<author>] [--date=<date>]
#                        [-n|--no-verify] [--no-post-rewrite] [--amend]
#                        [-F|--file <file>] [-t|--template <file>]
#                        [-e|--edit] [--no-edit]
#                        [-m|--message <msg>] [--cleanup=<mode>]
#                        [<patch>...]

_msg(){
    echo "$@"
}

_warn(){
    echo "$@" 1>&2
}

_die(){
    _warn Fatal: "$@"
    _warn Abort.
    exit 1
}

_sq(){
    git rev-parse --sq-quote "$@"
}

_do_apply(){
    eval "git apply --cached $1"
}

_do_commit(){
    eval "git commit $1"
}

_do_help(){
    cat <<__EOC__
usage: git commit-diff [<options>...] [--] [<patch>...]

Options
    -m|--message <msg> use the given <msg> as the commit message
    <patch>...         patch files which will be applied
__EOC__
}

_commit_args=
_apply_args=

main(){
    while test $# -ne 0
    do
        case "$1" in
            -m|--messsage)
                if test -n "$2"
                then
                    _commit_args="$_commit_args `_sq --message="$2"`"
                    shift
                else
                    _die "Message not given"
                fi
                ;;
            --message=*)
                _commit_args="$_commit_args `_sq "$1"`"
                ;;
            -h|--help)
                _do_help; return 0;;
            --)
                shift; break ;;
            *)
                # Other args are patches
                _apply_args="$_apply_args `_sq "$1"`";;
        esac
        shift
    done

    # Args left because of break by occurance of "--"
    if test $# -ne 0
    then
        _apply_args="$_apply_args `_sq "$@"`"
    fi

    # Specify path to index file to apply patch and copy existing index file
    _gitdir=`git rev-parse --git-dir`
    _index_file="$_gitdir"/commit-diff.index
    cp "$_gitdir"/index "$_index_file"

    # First try to apply patch to current index
    _do_apply "$_apply_args"

    # Reset only index
    export GIT_INDEX_FILE="$_index_file"
    git reset --mixed --quiet

    _do_apply "$_apply_args"
    _do_commit "$_commit_args"
}

main "$@"
