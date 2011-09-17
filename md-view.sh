#!/bin/sh

{
    {
        echo '<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"><head><title>markdown output</title></head><body>'


        if test $# -eq 0
        then
            markdown
        else
            markdown "$1"
        fi
        echo '</body></html>'
    } >/tmp/$$.html
} && $BROWSER /tmp/$$.html
