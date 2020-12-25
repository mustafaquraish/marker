.data 

result: .asciiz "The product is: "
newline: .asciiz "\n"
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main: 
	li $t1, 1	# t1 holds the product, start with 1
	add $t0, $zero, $zero	# t0 = 0, offset value (i)
	add $t4, $zero, 24	# t4 = 24, size of array
	la $t8, array1	# load address of array into t8
	
	loop:
		add $t3, $t8, $t0	# t3 holds address of array1 + i
		
		lw $s4, 0($t3)	# s4 = array1[i]

		# Perform multiplication and get Lo
		mult $t1 $s4
		mflo $t1
		
		addi $t0, $t0, 4	# increment i
		
		bne $t0, $t4, loop	# if i smaller than t4, keep going
		
	end:
	
	# Print product result
	li $v0, 4
	la $a0, result
	syscall
	
	move $a0, $t1	
	li $v0, 1
	syscall

	# exit program
	li $v0, 10
	syscall
