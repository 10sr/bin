#!/bin/sh

def_branch=diary
def_defcommand=help
def_show_options="--oneline --reverse"

is_sane(){
    # fail when git is not installed or current dir is not a git repository
    git rev-parse --git-dir 1>/dev/null
}

with_state_saved(){
    # with_state_saved command ...
    # save current status, run command and restore saved status
    echo "Save current state."
    _bak_HEAD="`git symbolic-ref --short HEAD 2>/dev/null`"
    if test -z "$_bak_HEAD"
    then
        _bak_HEAD=`git rev-parse HEAD`
    fi
    # if stash failed exit immediately
    _stash=`git stash create --no-keep-index || exit $?`
    git reset --hard >/dev/null

    "$@"

    echo "Restore saved state."
    git checkout $_bak_HEAD
    test -n "$_stash" && git stash apply --index --quiet $_stash
}

get_config(){
    # get_config name
    git config --get "diary.$1"
}

set_config(){
    # set_config name val
    # maybe should use --unset-all
    git config --local --add "diary.$1" "$2"
}

is_branch_initted(){
    _branch="`get_config branch`"
    if test -n "$_branch"
    then
        # what is the best way to test if branch exists?
        git rev-parse "$_branch" >/dev/null 2>&1
    else
        return 1
    fi
}

init_branch(){
    # initialize diary branch and checkout it
    if is_branch_initted
    then
        echo diary already initialized
        return 1
    fi

    _branch="`get_config branch`"
    if test -z "$_branch"
    then
        _branch=$def_branch
    fi
    echo git diary init
    echo branch name: $_branch
    git checkout --orphan "$_branch" && \
        git rm -rf . >/dev/null && \
        set_config branch "$_branch" # always config branch name locally
}

co_diary_branch(){
    if is_branch_initted
    then
        git checkout "`get_config branch`"
    else
        init_branch
    fi
}

add_diary(){
    if co_diary_branch
    then
        if test -n "$1"
        then
            git commit --allow-empty --message "$*"
        else
            git commit --allow-empty
        fi
    else
        echo "Checkout failed."
        return 1
    fi
}

do_add(){
    with_state_saved add_diary "$@"
}

do_show(){
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
    is_sane || exit $?

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
