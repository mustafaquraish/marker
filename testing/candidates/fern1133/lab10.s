.data 
sum: .asciiz "sum = "
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text 
main: 
START:
	la $s0, array1
	addi $t1, $s0, 24
	li $t2, 0
WHILE: 	beq $s0, $t1, DONE
	lw $t3, 0($s0)
	add $t2, $t2, $t3
	addi $s0, $s0, 4
	j WHILE
DONE:	li $v0, 4
	la $a0, sum
	syscall
	li $v0, 1
	move $a0, $t2
	syscall
	
	li $v0, 10 	
	syscall