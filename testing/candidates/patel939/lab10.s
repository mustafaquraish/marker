.data
array1: .word 5, 8, 3, 4, 7, 2
array1Size: .word 24
productResult: .asciiz "Product Result: "

.globl main
.text

main:
	LOOPINIT:
		# Store 1 in $t1 for multiplication
		li $t1, 1
		# Store address of array in $t9 
		la $t9, array1
		# Save size of array: 4*len(array1) = 4*6 = 24
		lw $t3, array1Size
		# $t0 is the counter for the index, it increments by 4 for each index
		add $t0, $zero, $zero
	WHILE:
		# $t2 saves the address of the ith index
        	add $t2, $t9, $t0
        	# Access the number stored at the address saved in $t2 and store it in $s0
        	lw $s0, 0($t2)
        	# Store the result of the prodcuts in $t1
        	mul $t1, $t1, $s0
        	# Increment the index counter: 1 index/4 bytes
        	addi $t0, $t0, 4
        	# Loop until the end of the array has been reached
        	bne $t0, $t3, WHILE
        DONE:
       	
       	# Printing result
       	li $v0, 4
	la $a0, productResult
	syscall
	li $v0, 1
	move $a0, $t1
	syscall 
       	
       	#End program
	li $v0, 10
	syscall