.data 
array1: .word 5, 8, 3, 4, 7, 2
numberOfBytes: .word 24
.globl main

.text
main: 
	la $t8, array1
	lw $t9, numberOfBytes
	li $t1, 0
	li $t2, 1
	WHILE:
		beq $t9, $t1, DONE
		
		add $t6, $t8, $t1
		lw $t7, 0($t6)
		
		#t2 starts at 1 and takes on prev value, t3 is user input
		mult $t2, $t7
		mflo $t2
		
		addi $t1, $t1, 4
		j WHILE
	
	DONE:
		li $v0, 1
		move $a0, $t2
		syscall
	
		li $v0, 10
		syscall
