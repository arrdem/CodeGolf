#!/usr/bin/env clisp

(defun sum (list)
    (setf s 0)	
    (loop for foo in list do
        (setf s (+ s foo))
    )
    s
)

(defun fib-list (n)
    (loop for x from 1 to n do
        (setf *fibs* (append *fibs* (list (sum (last *fibs* 2)))))
    )
)

(defun test ()
    (progn
            ;; variable initializations
        (setf n 12000)
        (setf ti (get-universal-time))
        (setf tf (get-universal-time))

        (loop while (<= (- tf ti) 8) do ; while the end time minus the start time
                                        ; is less than 8 sec...
            (progn
                (print n)
                (setf *fibs* '(1 1))
                (setf ti (get-universal-time))  ; record the start time

                (fib-list n)
                (print (sum *fibs*))

                (setf tf (get-universal-time))  ; record the end time
                (setf n (+ n 25))
            )
        )
        (print "MAXIMUM NUMBER......")
        (print n)
    )
)

(test)
