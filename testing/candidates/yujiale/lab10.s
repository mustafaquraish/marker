.data 
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "The result is: "

.globl main
.text 

main: 
	li $t7, 0
	li $s0, 1
	li $t6, 6
	la $t9, array1
	li $t0, 0
	
	WHILE:
	beq  $t7, $t6 , EXIT
	
	add $t4, $t9, $t0
	lw $s4, 0($t4)
	
	
	mult $s0, $s4
	
	mflo $s0
	
	addi $t7, $t7,1
	addi $t0,  $t0 , 4
	
	j WHILE
	
	EXIT: 
	li $v0, 4		      
	la $a0, result
	syscall  
	
	li $v0, 1		      
	move  $a0, $s0
	syscall
	
	
	li $v0, 10
	syscall
