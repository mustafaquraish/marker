.data
product: .asciiz "Product: "
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main:
	li $t2, 1
loop:
	la $t1 array1
	add $t1, $t1, $t0
	lw $t3, 0($t1)
	mult $t2, $t3
	mflo $t2
	addi $t0, $t0, 4
	bne $t0, 24, loop
	
	li $v0, 4
	la $a0, product
	syscall
	
	li $v0, 1
	la $a0, 0($t2)
	syscall
	
	li $v0, 10
	syscall