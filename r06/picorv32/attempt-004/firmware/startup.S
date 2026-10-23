.section .text.start,"ax"
.global _start
_start:
.option push
.option norelax
la gp, __global_pointer$
.option pop
li sp, 0xff00
call main
ebreak
1: j 1b
