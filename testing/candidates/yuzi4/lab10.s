.data
	array1: .word 5, 8, 3, 4, 7, 2

.text

main:
	la $t0, array1    # Store starting address of the array in $t0
	li $t1, 0         # Initialize $t1 counter to 0
	li $t2, 4         # Set $t2 to constant integer of 4
	li $t3, 6         # Set $t3 to constant integer of 6 (array size)
	li $t4, 1         # Initialize $t4 to 1 (product)
	
	WHILE:
		beq $t1, $t3, DONE
		lw $t5 ($t0)                 # $t5 = array1[i]
		mult $t4, $t5
		mflo $t4                     # $t4 = array1[i] * current product value
		addi $t1, $t1, 1             # Increment counter
		addi $t0, $t0, 4             # i++ (because an int takes up 4 bytes, I need to add 4 to the current array index's address)
		j WHILE
	DONE:
	
	li $v0, 1
	move $a0, $t4
	syscall
	
	li $v0, 10
	syscall