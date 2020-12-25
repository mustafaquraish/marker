.data 
array1:    .word    5, 8, 3, 4, 7, 2

.globl main
.text

main: 
	add $t0, $zero, $zero
	addi $t1, $zero, 24
	la $t9, array1 
	add $t2, $zero, $zero
WHILE:
	add $t3, $t9, $t0
	lw $s4, 0($t3)
	addi $t0, $t0, 4
	beq $t2, 0, ELSE
	mult $t4, $s4
	mflo $t4
	bne $t0, $t1, WHILE
ELSE:
	move $t4, $s4
	addi $t2,$t2, 1
	bne $t0, $t1, WHILE
DONE:
	li $v0, 1		      
	mflo $a0
	syscall
	
	li $v0, 10
	syscall
