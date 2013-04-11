#!/bin/sh

_conf=memo

get_path(){
    git config --get $_conf.path
}

cd_path(){
    path="`get_path`"
    if test -z "$path"
    then
        echo \
            "Path is not set." \
            " Use \"$0 init <path>\" or set $_conf.path first." 1>&2
        return 1
    fi

    cd "$path"
}

help_diary(){
    git diary help
}

help_init(){
    cat <<__EOC__ 1>&2
usage: $0 init <path>
__EOC__
}

help_help(){
    cat <<__EOC__ 1>&2
usage: $0 help [<command>]
Show help for specified command.
__EOC__
}

help(){
    _c="`basename $0`"
    if test -z "$1"
    then
        cat <<__EOC__ 1>&2
usage: $_c init <path>
   or: $_c <command_for_git_diary> [arg ...]
   or: $_c git [<options_for_git> ...]
   or: $_c pull [arg ...]
   or: $_c push [arg ...]
   or: $_c config [arg ...]
   or: $_c help [<command>|diary]

Take notes using git-diary. Directory of repository for memo is defined at
  $_conf.path
__EOC__
    else
        help_$1 || return 1
    fi
}

init(){
    # init path
    if test -z "$1"
    then
        echo "Path is not specified." 1>&2
        echo "usage: $0 init <path>" 1>&2
        return 1
    fi

    mkdir -p "$1" && \
        cd "$1" || return 1

    if git rev-parse --git-dir >/dev/null 2>&1
    then
        echo "$1 is already initialized as a git repository." 1>&2
        echo "Abording." 1>&2
        return 1
    fi

    git init
    git config --global --add $_conf.path "`pwd`"
}

main(){
    git diary help >/dev/null 2>&1 || exit $?

    if test "$1" = debug
    then
        set -x
        shift
    fi

    if test -z "$1"
    then
        help
    elif test "$1" = init
    then
        shift
        init "$@"
    elif test "$1" = help
    then
        shift
        help "$@"
    elif test "$1" = push
    then
        shift
        cd_path && git push "$@"
    elif test "$1" = pull
    then
        shift
        cd_path && git pull "$@"
    elif test "$1" = config
    then
        shift
        cd_path && git config "$@"
    elif test "$1" = git
    then
        shift
        cd_path && git "$@"
    else
        cd_path && git diary "$@"
    fi
}

main "$@"
