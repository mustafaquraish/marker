.data
array1: .word 5, 8, 3, 4, 7, 2

.text

main:
	LOOPINIT:
		add $t0, $zero, $zero # offset
		li $t1, 1 # product
		li $t2, 24 # array size 
		la $t3, array1 # load address of array1 (address of first element)
	LOOP:
		add $t4, $t3, $t0 # index
		lw $t5, 0($t4) # value of array[index] 
		mult $t1, $t5 # multiply
		mflo $t1 # store 32 least significant bits from operation $t4 * $v0
		addi $t0, $t0, 4 # index++
		bne $t0, $t2, LOOP # loop until end of array
	DONE:
	
	# print result
	li $v0, 1
	move $a0, $t1
	syscall
	
	# exit program
	li $v0, 10
	syscall
	
		
		
		