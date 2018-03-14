#!/bin/sh
set -e

# git-format-patch-from-index --- Format patch from staged files

# NOTE: what happens when...
#   - submodules exist?

# NOTE: git am
# When index is dirty, git am fails with message 'Dirty index'.
# When working tree is dirty, git am fails with message 'does not match index',
# which means that the content in the worktree is not match with that in index.

_git_format_patch(){
    # _git_format_patch <commit>
    # Format patch from commit and output the patch filename
    git format-patch --binary --color=never -1 $1
}

_mk_commit_from_index(){
    #_mk_commit_from_index
    # Create new commit object from current index and output sha1 of that object
    # The parent of the commit is set to be HEAD
    _parent_commit=`git rev-parse --verify HEAD`
    _tree=`git write-tree`
    cat <<__EOC__ | git commit-tree $_tree -p $_parent_commit
Commit at $(LANG=C date)

Write some more comments here.
__EOC__
}

do_help(){
    cat <<__EOC__
usage: git format-patch-from-index [-h|--help]
__EOC__
}

main(){
    while getopts h opt
    do
        case "$opt" in
            h) do_help; return 0;;
            *) do_help; return 1;;
        esac
    done


    _gitdir=`git rev-parse --git-dir`
    _index_orig="$_gitdir"/index
    _index="$_gitdir"/index.$$

    _commit=`_mk_commit_from_index`
    _git_format_patch $_commit
}

main "$@"
