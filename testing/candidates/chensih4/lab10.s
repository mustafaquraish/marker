.data 
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "The product is: "
newline: .asciiz "\n"
.globl main
.text 
main:
	li $t0, 0
	li $t1, 24
	la $t2, array1
	li $t3, 1
LOOP:
	beq $t0, $t1, END
	add $t4, $t0, $t2
	lw $t4, 0($t4)
	mult $t3, $t4
	mflo $t3
UPDATE:
	addi $t0, $t0, 4
	j LOOP
END:
	li $v0, 4
	la $a0, result
	syscall 
	li $v0, 1
	move $a0, $t3
	syscall 
	li $v0, 4
	la $a0, newline
	syscall 
	li $v0, 10
	syscall 
