OBJS = a.pdf

lyx = $(shell which lyx)
ifeq ($(strip ${lyx}),)
	lyx = /Applications/Lyx.app/Contents/MacOS/lyx
endif

periodize = $(shell git rev-parse --show-toplevel)/common/yuk/bin/periodize.py

# _def :
# 	echo ${periodize}

default : all

clean :
	$(RM) *.aux *.dvi *.log *.bbl *.blg *~

all : ${OBJS}

%.pdf : %.dvi
	dvipdfmx $*

%.dvi : %.tex
	platex $<
	platex $<

%.tex : %.lyx
	${lyx} --export latex $<
	# mv $@ $@.bak
	# <$@.bak ${periodize} >$@
	# rm $@.bak
	# emacs --script process_main.el main.tex
