.data
array1: .word 5, 8, 3, 7, 4, 2
result: .asciiz "Their product is:"
newline: .asciiz "\n"

.globl main, LOOPINIT, WHILE, DONE
.text

main: 
    
LOOPINIT:
	
	#stopping point for loop
	li $t0, 24
	# counter for while loop and offset
	li $t1, 0
	# keeps track of result
	li $t2, 1
	#load address of array1
	la $t3, array1

WHILE:

	# check if we are at stopping condition for while loop
	beq $t0, $t1, DONE
	
	# store offset with address of array1 into a register
	add $t4, $t3, $t1   

        # load word at location array1 + offset into a register for mutiplying
        lw $t5, 0($t4)
	
	# multiply the word stored in $t5 with the int in $t2
	mult $t2, $t5
	
	# load the product back into $t2
	mflo $t2
	
	#increment the offset
	addi $t1, $t1, 4
	
	# go back to while to get next int
	j WHILE
	 
DONE:

	# Print new line 
	li $v0, 4
	la $a0, newline
	syscall
	
	# make syscall to print result on screen
	li $v0, 4
	la $a0, result
	syscall

        # print the product on screen
	li $v0, 1
	move $a0, $t2	
	syscall
	
	# Print new line 
	li $v0, 4
	la $a0, newline
	syscall


    # Exit program
	li $v0, 10
	syscall
