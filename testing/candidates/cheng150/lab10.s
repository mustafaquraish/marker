.data 
# TODO: What are the following 5 lines doing?
result: .asciiz "The product of the array is: "
newline: .asciiz "\n"
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main: 
	LOOPINIT:
		li $t0, 0 # Initialising counter
		addi $t1, $zero,  24 # Initialising size of array (6 X 4 = 24)
		li $t2, 1 # Initialising total
		la $t3, array1 # Initialising address of array
	WHILE:
		
		add $t4, $t0, $t3
		lw $t5, ($t4)
		
		# Multiplies user value by total
		mult $t5, $t2		 
		mflo $t2 
		addi $t0, $t0, 4 # Incrementing counter
		beq $t0, $t1, DONE # Checks loop condition 
		j WHILE
	DONE: 
		li $v0, 4
		la $a0, result
		syscall 
		li $v0, 1
		move $a0, $t2 
		syscall