.data
array1: .word  5, 8, 3, 4, 7, 2
space: .asciiz " "

.globl main
.text

main: # setup
	la $t0, array1
	li $t1, 0
	li $t2, 24
	
	li $t5, 1

LOOP:
	add $t3, $t0, $t1
	lw $t4, 0($t3)
	
	mult $t5, $t4
	mflo $t5
	
	
	addi $t1, $t1, 4
	bge $t1, $t2, END
	j LOOP
	
END:	
	li $v0, 1
	move $a0, $t5
	syscall

