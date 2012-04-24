#!/usr/bin/env gosh

; (main foo bar)で呼ぶとargs => (foo bar)になる
; $ test.scm foo bar で呼ぶと args => ((foo bar))になる
(define (main . args)
  (print "hello world!")
  ; (if args (print (car args)))
  (while (pair? args)
         (write (pop! args)))
  0)
;gauche #f

;(define (printlist . args) (print args) #f)
