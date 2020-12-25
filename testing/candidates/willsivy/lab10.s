.data
array1: .word 5, 8, 3, 4, 7, 2
resultAdd: .asciiz "The addition of the elements in the array is: "

.globl DONE
.text

main: 

	add $t2, $zero, $zero
	addi $t1, $zero, 24
	la $t8, array1
	
	
	WHILE:
		
		add $t3, $t8, $t2
 		lw $s4, 0($t3)
		add $t6, $s4, $t6
	
		addi $t2, $t2, 4
		bne $t2, $t1, WHILE
	
	DONE:
	
	li $v0, 4
	la $a0, resultAdd
	syscall

	li $v0, 1
	move $a0, $t6	
	syscall