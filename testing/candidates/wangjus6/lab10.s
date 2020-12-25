.data
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "The product is: "

.globl main
.text

main:

   # Setting counter i = 0, and product = 1
	li $t3, 0
	li $t0, 6
	li $t2, 1
	
	la $a0, array1
	
	WHILE:
   #Checking if i >= 6
	beq $t3, $t0, DONE
	
	lw $t4, 0($a0)
	
	mul $t2, $t2, $t4
	
	add $a0, $a0, 4
	
	add $t3, $t3, 1
	
	j WHILE
		
	DONE:
	
	li $v0, 4
	la $a0, result
	syscall
	
	li $v0, 1
	move $a0, $t2
	syscall
	
	li $v0, 10
	syscall