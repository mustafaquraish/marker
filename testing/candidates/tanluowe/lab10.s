.data
array1: .word 5, 8, 3, 4, 7, 2
resultMULTI: .asciiz "Product is: "
newline: .asciiz "\n"

.globl main
.text
main:	add $t0, $zero, $zero
	addi $t1, $t1, 24
	la $t9, array1
	li $t8, 1
	
loop:	add $t2, $t9, $t0
	lw $s2, 0($t2)
	mult $t8, $s2
	mflo $t8
	addi $t0, $t0, 4
	bne $t0, $t1, loop
end:
	li $v0, 4
	la $a0, resultMULTI
	syscall
	
	li $v0, 1
	move $a0, $t8	
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall 
	
	li $v0, 10
	syscall
	