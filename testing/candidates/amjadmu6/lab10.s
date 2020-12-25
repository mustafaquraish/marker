.data 

array1: .word 5, 8, 3, 4, 7, 2
promptProduct: .asciiz "The product is: "
newline: .asciiz "\n"

.globl main
.text

main: 
	add $t0, $zero, $zero # set t0 to zero
	addi $t1, $zero, 24 # set t1 to 24 = 6*4
	
	la $t8, array1 # put address of array1 into register t8
	
	li $t2, 1 # put value of 1 into t1
WHILE:
	add $t3, $t8, $t0 # put address of array1[i] into register t3
	lw $s4, 0($t3) # load the word at address t3 into s4 with 0 offset
	
	mult $t2, $s4
	mflo $t2
	
	addi $t0, $t0, 4 # update i since int is 4 bytes

	bne $t0, $t1, WHILE
DONE:
	li $v0, 4 # load service number 4 (print string) in register v0 		      
	la $a0, promptProduct # set a0 to promptEven's address
	syscall # execute the system call specified by the value in v0 (printing promptProduct)  

	li $v0, 1 # load service number 1 (print integer) in register v0
	la $a0, ($t2) # set $a0 to contents of t2
	syscall # execute system call (print integer)

	li $v0, 10
	syscall
