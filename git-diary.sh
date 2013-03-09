#!/bin/sh -x

def_branch=diary
def_defcommand=help
def_show_options="--oneline --reverse"

is_sane(){
    # fail when git is not installed or current dir is not a git repository
    git rev-parse --git-dir 1>/dev/null
}

get_config(){
    # get_config name
    git config --get "diary.$1"
}

set_config(){
    # set_config name val
    # maybe should use --unset-all
    if test "$2" != "`git config --local --get "diary.$1"`"
    then
        git config --local --add "diary.$1" "$2"
    fi
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
        git commit-tree $_tree -p $1
    else
        git commit-tree $_tree
    fi
}

do_add(){
    is_sane || return $?

    _msg="$*"
    if test -z "$_msg"
    then
        # todo: launch editor
        echo message not specified.
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

    _new=`echo "$_msg" | mk_commit $_parent`

    git update-ref "refs/heads/$_branch" $_new
}

do_show(){
    is_sane || return $?

    _options="`get_config show.options`"
    if test -z "$_options"
    then
        _options="$def_show_options"
    fi
    git log "`get_config branch`" $_options "$@"
}

do_help(){
    _cmd="git diary"
    cat <<__EOC__ 1>&2
usage: $_cmd add [<strings>]
   or: $_cmd show [<options>]
   or: $_cmd help
__EOC__
}

main(){
    if test -z "$1"
    then
        _cmd="`get_config defcommand`"
        if test -z "$_cmd"
        then
            _cmd=$def_defcommand
        fi
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
