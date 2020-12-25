.data
array1: .word 5, 8, 3, 4, 7, 2
promptA: .asciiz "The product of the array is: "
newline: .asciiz "\n"

.globl main
.text

main: 

	add $t0, $zero, $zero # holds the array iterated value
	addi $t1, $zero, 24  # Gets the array size
	la $t2, array1 #address for array1
	li $t3, 1 # Stores the result value
	loop:
		add $t4, $t2, $t0 # is the iterated address being used
		lw $s0, 0($t4)	#load in this value to s0
		mult $t3, $s0 #multiply loaded in value by t3 (1 to start)
		mflo $t3
		addi $t0, $t0, 4 # add 4 to t0 as i want to iterate the next word in the array (each word is 4 bytes)
		bne $t0, $t1, loop # When you loop through all your array spots
		
	li $v0, 4
	la $a0, promptA
	syscall 

	move $a0, $t3	
	li $v0, 1
	syscall 
	
	li $v0, 4
	la $a0, newline
	syscall 
	
	li $v0, 10
	syscall
