#!/bin/sh -x

def_branch=diary
def_defcommand=help

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

    echo "" >"$_file"
    eval "$_editor \"$1\""
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
    git config --local alias.diary-show \
        "log --reverse --pretty=tformat:\"%C(yellow)%ai%C(reset) [%C(red)%an%C(reset)] %C(white bold)%s%C(reset)\""
}

do_show(){
    is_sane || return $?

    _branch="`get_config branch`"
    if test -z "$_branch"
    then
        echo "No diary in this repository." 1>&2
        return 1
    fi

    if test -z "`git config alias.diary-show`"
    then
        set_alias_diary_show
    fi

    git diary-show "`get_config branch`" "$@"
}

do_help(){
    _cmd="git diary"
    cat <<__EOC__ 1>&2
usage: $_cmd add [<text> ...]
   or: $_cmd show [<pattern>]
   or: $_cmd help
__EOC__
}

main(){
    if test -z "$1"
    then
        _c="`get_config defcommand`"
        if test -z "$_cmd"
        then
            _c=$def_defcommand
        fi
        exec git diary $_c
    fi

    _cmd="$1"
    shift

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
