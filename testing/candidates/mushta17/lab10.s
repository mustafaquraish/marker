.data
array1: .word 5, 8, 3, 4, 7, 2
product: .asciiz "The product is: "

.globl main
.text

main: #t0 will hold i, t1 will hold max, t2 will hold array, t3 will hold product
	addi $t0, $zero, 0
	addi $t1, $zero, 6
	la $t2, array1
	addi $t3, $zero, 1
	add $t4, $zero, $t2

loop:	lw $s0, 0($t4)		# load int at address t4 (initially set to
				# 	address of first element in array)
	mult $t3, $s0		# multiply
	mflo $t3
	addi $t4, $t4, 4	# increment t4 by 4 to get the next int
	addi $t0, $t0, 1
	bne $t1, $t0, loop

end: 	
	li $v0, 4		      
	la $a0, product
	syscall
	
	li $v0, 1
	add $a0, $zero, $t3
	syscall
	
	li $v0, 10
	syscall 
