.data
product: .asciiz "The product is: "
newline: .asciiz "\n"
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text 

main: 
	# load address of array1
	la $t8, array1
	
	LOOPINIT: 
		# counter variable
		li $t1, 0
		# holds product over each iteration
		li $t2, 1
	WHILE: 		
		# get address of current int (add 4 per iteration)
		add $t3, $t8, $t1  
		# $s4 = array1[i]
		lw $s4, 0($t3) 
		
		# Multiply input and previous product
		mult $t2, $s4
		# set t2 as product of current int and previous product 
  		mflo $t2 
  		
  		# $t1 += 4
  		addi $t1, $t1, 4 
  		# branch back if $t1 < 24 (6 ints x 4 bytes per int)	
		bne $t1, 24, WHILE
	DONE: 
		# Prompt product text
		li $v0, 4
		la $a0, product
		syscall
	
		# Print product
		li $v0, 1
		move $a0, $t2	
		syscall
		
		# Display newline
		li $v0, 4
		la $a0, newline
		syscall 

		# Exit program
		li $v0, 10
		syscall
