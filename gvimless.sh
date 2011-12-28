#!/bin/sh
# Shell script to start Gvim with less.vim.
# Read stdin if no arguments were given.

if test -t 1; then
 if test $# = 0; then
   gvim --cmd 'let no_plugin_maps = 1' -c 'runtime! macros/less.vim' -
  else
   gvim --cmd 'let no_plugin_maps = 1' -c 'runtime! macros/less.vim' "$@"
  fi
else
  # Output is not a terminal, cat arguments or stdin
  if test $# = 0; then
    cat
  else
    cat "$@"
  fi
fi