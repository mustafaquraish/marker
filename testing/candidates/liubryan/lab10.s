.data 
# TODO: What are the following 5 lines doing?
promptA: .asciiz "Enter an int A: "
promptB: .asciiz "Enter an int B: "
resultAdd: .asciiz "A + B = "
resultSub: .asciiz "A - B = "
newline: .asciiz "\n"
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main: 
	add $t0, $zero, $zero
	addi $t1, $zero, 24
	addi $t2, $zero, 1
	
	la $t8, array1 
loop: 
	add $t3, $t8, $t0
	lw $t4, 0($t3) 
	mult $t2, $t4
	mflo, $t2 
	addi, $t0, $t0, 4
	bne $t0, $t1, loop
end:
	li $v0, 1
	move $a0, $t2 
	syscall

	li $v0, 10
	syscall
