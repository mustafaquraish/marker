.data 
# TODO: What are the following 5 lines doing?
array1: .word 5, 8, 3, 4, 7, 2
newline: .asciiz "\n"

.globl main
.text

main: 

	la $t0, array1			#load first index into t0
	addi $t1, $t0, 24		#load final index into t1
	
	LOOP:
		li $v0, 1			#Loads [print a0 string] instruction into v0      
		lw $a0, 0($t0)	        	#Loads address for A[i]
		syscall    			#Executes v0 instruction
		
		li $v0, 4
		la $a0, newline
		syscall
		
		addi $t0, $t0, 4	#add offset to counter
		bne $t0, $t1, LOOP	#check if at the end of array

	
	li $v0, 4
	la $a0, newline
	syscall 

	li $v0, 10
	syscall
