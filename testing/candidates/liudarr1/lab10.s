.data 
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main:
	# Counter
	add $t0, $zero, $zero
	
	# Size of darray1 in bytes
	addi $t1, $zero,  24
	
	# Load Array
	la $t3, array1
	
	# Product Sum
	# Start with first number, and increment counter.
	lw $t2, 0($t3)
	addi $t0, $zero, 4
	
loop:
	# Get Adress & Load
	add $t4, $t3, $t0
	lw $s0, 0($t4)
	
	# Calculate Product
	mult $t2, $s0
	
	# Since product is less than 32 bits, 
	# we only concern ourselves with lo
	mflo $t2
	
	# Increment Counter
	addi $t0, $t0, 4
	
	# check if entire array is read
	bne $t0, $t1, loop

end:
	move $a0, $t2
	li $v0, 1
	syscall
	
	li $v0, 10
	syscall
