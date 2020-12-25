.data
array1: .word 5, 8, 3, 4, 7, 2

.text
main:
	la $t1, array1		# Store address of array
	li $t0, 0 		# Creating an offset in a register
	li $t2, 24		# Put array byte size in a register
	li $t3, 1		# Product register
	
loop: 
	add $t4, $t1, $t0	# base + offset
	lw $s1, 0($t4)
	mult $t3, $s1	
	mflo $t3		# save product
	addi $t0, $t0, 4	# increase offset
	bne $t0, $t2, loop	# loop conditonal statement

end: 
	# Print product
	li $v0, 1		      
	move $a0, $t3
	syscall
	
	# Exit
	li $v0, 10
	syscall

	  

