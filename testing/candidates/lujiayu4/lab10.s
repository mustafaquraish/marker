.data
	array1: .word 5, 8, 3, 4, 7, 2
	result: .asciiz "The result is: "

.text

main:
	la $t9, array1	# $t9 stores the base of the array
	li $t0, 1	# t1 stores the value 1
	
	loop_init:
		li $t1, 0	# $t1 = index = 0
	while:
		beq $t1, 6, done	# check if complete the interation
		
		lw $t2, 0($t9)		# $t2 stores the ith element
	
		mult $t2, $t0		# multiply the ith element
		mflo $t0		# store current result to $t0
		
		addi $t9,$t9, 4		# increase offset by 4
		
		addi $t1, $t1, 1	# index = index + 1
	
		j while
		
	done:
	
	li $v0, 4
	la $a0, result
	syscall
	
	move $a0, $t0	
	li $v0, 1
	syscall 
	
	li $v0, 10
	syscall
