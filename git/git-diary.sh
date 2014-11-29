#!/bin/sh

def_branch=diary

is_sane(){
    # fail when git is not installed or current dir is not a git repository
    git rev-parse --git-dir 1>/dev/null
}

get_config(){
    # get_config name
    git config "diary.$1"
}

set_config(){
    # set_config name val
    git config --local "diary.$1" "$2"
}

mk_empty_tree(){
    # create empty tree object and echo sha1
    echo "" | git mktree --batch
}

mk_commit(){
    # mk_commit [<parent>]
    # create new commit object with empty tree.
    # commit message is read from stdin.
    # echo created commit object.
    _tree=`get_config treeobj`
    if test -z "$_tree"
    then
        _tree=`mk_empty_tree`
        set_config treeobj $_tree
    fi

    if test -n "$1"
    then
        git commit-tree $_tree -p $1 -F -
    else
        git commit-tree $_tree -F -
    fi
}

edit_msg(){
    # edit_msg file
    # edit message using editor
    _editor="`get_config editor`"
    if test -z "$_editor"
    then
        _editor="`git var GIT_EDITOR`"
    fi

    echo "" >"$1"
    # eval "$_editor \"$1\""
    $_editor "$1"
}

do_add(){
    is_sane || return $?

    _msg="$*"
    if test -z "$_msg"
    then
        _file="`git rev-parse --git-dir`"/DIARY
        edit_msg "$_file"
        _msg="`cat "$_file"`"
    fi

    if test -z "$_msg"
    then
        echo "No message specified."
        return 1
    fi

    _branch="`get_config branch`"
    if test -z "$_branch"
    then
        _branch=$def_branch
    fi

    # is this correct for get sha1 from branch name?
    _parent=`git rev-parse --verify "refs/heads/$_branch" 2>/dev/null`
    if test -z "$_parent"
    then
        set_config branch "$_branch"
    fi

    echo "Add new diary:"
    echo ""
    echo "$_msg"
    _new=`echo "$_msg" | mk_commit $_parent`

    git update-ref "refs/heads/$_branch" $_new
}

set_alias_diary_show(){
    git config --local alias.diary-list log
    # log --reverse --pretty=tformat:"%C(green)%h%C(reset) %C(yellow)%ai%C(reset) [%C(red)%an%C(reset)] %C(white bold)%s%C(reset)"
}

do_list(){
    is_sane || return $?

    _branch="`get_config branch`"
    if test -z "$_branch"
    then
        # echo "No diary in this repository." 1>&2
        # return 1
        _branch=$def_branch
    fi

    if test -z "`git config alias.diary-list`"
    then
        set_alias_diary_show
    fi

    git diary-list "$_branch" "$@"
}

do_show(){
    is_sane || return $?
    git show "$@"
}

do_help(){
    _cmd="git diary"
    cat <<__EOC__ 1>&2
usage: $_cmd add [<text> ...]
   or: $_cmd list [<option> ...]
   or: $_cmd show [<option> ...]
   or: $_cmd help
__EOC__
}

main(){
    if test "$1" = debug
    then
        set -x
        shift
    fi

    if test -z "$1"
    then
        _cmd=help
    else
        _cmd="$1"
        shift
    fi

    if type "do_$_cmd" >/dev/null 2>&1
    then
        do_$_cmd "$@"
    else
        echo "Invalid option: $_cmd"
        do_help
        exit 1
    fi
}

main "$@"
