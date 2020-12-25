.data
# TODO: iterate through array1 and compute products of the array
result: .asciiz "The result is = "
newline: .asciiz "\n"
array1: .word    5, 8, 3, 4, 7, 2

.globl main
.text

main: 

LOOPINIT:

    li $t0, 6
    li $t1, 0
    li $t2, 1
    la $s0, array1

WHILE:
	
	
	beq  $t1,$t0,DONE
	
	lw $t3, 0($s0)
	mult $t2, $t3
	mflo $t2
	addi $s0, $s0, 4
    	addi $t1,$t1, 1

    	j WHILE 

DONE:

	li $v0, 4
	la $a0, result
	syscall
	
	li $v0, 1
	move $a0, $t2	
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall 

	li $v0, 10
	syscall
