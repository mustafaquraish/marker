.data 
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "The product is: "
newline: .asciiz "\n"

.globl main
.text

main: 
	
	LOOPINIT:
		li $t0, 1
		la $t2, array1
		lw $t4, 0($t2)
	FOR:
		# check if limit 6 reached
		subi $t3, $t0, 6
		bgez $t3, DONE
		
		# calculate offset
		li $t5, 4
		multu $t5, $t0
		mflo $t5
		
		# add offset to address of head
		add $t5, $t2, $t5
		lw $t6, 0($t5)
		
		# multiply operand into product
		multu $t6, $t4
		mflo $t4
	
		# increment the number of times looped
		addi $t0, $t0, 1
		
		j FOR
	DONE:

	li $v0, 4
	la $a0, result
	syscall

	move $a0, $t4	
	li $v0, 1
	syscall 

	li $v0, 4
	la $a0, newline
	syscall 
	
	li $v0, 10
	syscall
