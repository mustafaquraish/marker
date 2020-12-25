.data 
prompta: .asciiz "Enter N: "
promptb: .asciiz "Enter an int: "
result: .asciiz "The product is: "
newline: .asciiz "\n"

array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main: 
	li $t9, 6

	li $t8, 0
	li $t1, 1
	la $t2, array1

while:

	beq $t8, $t9, out
	
	lw $t0, 0($t2)
	
	mult $t0, $t1
	mflo $t1
	
	addi $t2, $t2, 4
	addi $t8, $t8, 1
	j while
out:
	li $v0, 4
	la $a0, result
	syscall
	
	li $v0, 1
	move $a0, $t1
	syscall
done:

	li $v0, 10
	syscall
