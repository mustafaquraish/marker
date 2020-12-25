.data 
array1: .word 5, 8, 3, 4, 7, 2
resultProduct: .asciiz "The Product Is: "
newline: .asciiz "\n"

.globl main
.text

main: 

loopinit:
	
	# $t0 is array size, $t1 is counter, $t2 is accumulator
	li $t0, 24
	li $t1, 0
	li $t2, 1
	
	# Load array address
	la $t9, array1

loop:
	# Do $t3 = addr(array1) + i and load it from memory
	add $t3, $t9, $t1
	lw $s4, 0($t3)
	
	# Perform multiplication and store result
	mult $t2, $s4 
	mflo $t2
	
	# increment counter
	addi $t1, $t1, 4
	bne $t1, $t0, loop

end:
	# Print the product/result
	li $v0, 4
	la $a0, resultProduct
	syscall

	move $a0, $t2	
	li $v0, 1
	syscall 
	
	li $v0, 10
	syscall
