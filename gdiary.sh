#!/bin/sh

get_path(){
    git config --get gdiary.path
}

cd_path(){
    path="`get_path`"
    if test -z "$path"
    then
        echo \
            "Path is not set." \
            "Use \"$0 init <path>\" or set gdiary.path first." 1>&2
        return 1
    fi

    cd "$path"
}

help(){
    echo $0 help
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
    git config --global --add gdiary.path "`pwd`"
    git config --local --add diary.branch "master"
    echo init
}

main(){
    git diary help >/dev/null 2>&1 || exit $?

    if test "$1" = init
    then
        shift
        init "$@"
    elif test "$1" = help
    then
        shift
        help "$@"
    elif test "$1" = git
    then
        shift
        cd_path && git "$@"
    else
        cd_path && git diary "$@"
    fi
}

main "$@"
