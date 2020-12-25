.data
result: .asciiz "The product is: "
array1: .word 5, 8, 3, 4, 7, 2
newline: .asciiz "\n"

.globl main
.text

main:
	add $t0, $zero, $zero
	addi $t1, $zero, 24
	la $t2, array1
	add $t3, $zero, 1
loop:
	add $t4, $t2, $t0
	lw $s4, 0($t4)
	mult $s4, $t3
	mflo $t3
	
	addi $t0, $t0, 4
	bne $t0, $t1, loop
	
	j arrayProduct
	
arrayProduct:
	
	li $v0, 4
	la $a0, result
	syscall
	
	move $a0, $t3
	
	li $v0, 1
	syscall
	
	j DONE
	
DONE:
	li $v0, 4
	la $a0, newline
	syscall
	
	li $v0, 10
	syscall
