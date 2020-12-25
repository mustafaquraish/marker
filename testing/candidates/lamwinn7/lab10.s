.data 
newline: .asciiz "\n"
product: .asciiz "Product: "
array1: .word 5, 8, 3, 4, 7, 2
array1Length: .word 6

.globl main
.text

main:	
	# load array1 into a register as an argument
	la $a1, array1
	
	# initialize initial multiplication value to 1 (accumulator)
	addi $t0, $zero, 1
	
	# initial loop value i=0 (up to length of array)
	add $t1, $zero, $zero
	
	# saving length of array1
	lw $s0, array1Length
	
START:
	# load word address from array
	lw $t2, 0($a1)
	
	# do multiplication to accumulator
	mult $t0, $t2		# $t2 element in array
	mflo $t0
	
	# update increment
	addi $t1, $t1, 1
	
	# update offset to go to next address (4 bytes)
	addi $a1, $a1, 4
	
	# loop again if not reached end of array1
	bne $t1, $s0, START
	
EXIT:
	# print product math
	li $v0, 4		      
	la $a0, product
	syscall 
	
	move $a0, $t0	
	li $v0, 1
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall 
	
	# end the program
	li $v0, 10
	syscall
	
