.data
array1: .word 5, 8, 3, 4, 7, 2
newline: .asciiz "\n"

.text
loopInit:
	li $t0, 0		# The current position in the array.
	li $t1, 6		# The number of elements in the array.
	la $t2, array1	# The address of the array.
	
while:
	lw $t3, ($t2)	# Load the word at the current position in the array.
	
	li $v0, 1		# System call code to print an integer.
	move $a0, $t3	# Print the value in $t3 (value at the current array position).
	syscall
	
	li $v0, 4		# System call to print a string.
	la $a0, newline	# Print a newline.
	syscall

	addi $t0, $t0, 1	# Increment the current array position.
	addi $t2, $t2, 4	# Increase the offset of the current address by one word.
	
	blt $t0, $t1, while	# Continue the loop if we are not at the last element in the array.