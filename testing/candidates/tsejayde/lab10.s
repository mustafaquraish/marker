.data
array1: .word 5, 8, 3, 4, 7, 2
newline: .asciiz "\n"

.globl main
.text

main:
	la $t0, array1
	li $t2, 1
	li $t3, 0
	li $t4, 6
	
WHILE:
	beq $t3, $t4, END
	lw $t1, 0($t0)
	mult $t2, $t1
	mflo $t2
	addi $t3, $t3, 1
	addi $t0, $t0, 4
	j WHILE
END:
	
	li $v0, 1
	move $a0, $t2
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall
	
	li $v0, 10
	syscall