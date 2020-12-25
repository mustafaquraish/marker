.data
array1: .word 5, 8, 3, 4, 7, 2
productMessage: .asciiz "Product = "

.text

main:
	add $t0, $zero, $zero # Iteration Counter
	addi $t1, $zero, 1 # Product Counter
	addi $t2, $zero, 24 # Terminiation

	la $t9, array1

loop:
	add $t3, $t9, $t0 # Address of A[i]
	lw $s0, 0($t3) # Load A[i]
	
	mult $s0, $t1
	mflo $t1 # Assume result in last 32 bits
	addi $t0, $t0, 4
	bne $t0, $t2, loop

	li $v0, 4 # system call code for print_string
	la $a0, productMessage # address of string A to print
	syscall # print the string
	
	li $v0, 1
	move $a0, $t1
	syscall
	
	# End of main, make a syscall to "exit"
	li $v0, 10 	# system call code for exit
	syscall 	# terminate program	
	