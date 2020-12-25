.data 
array1: .word 5,8,3,4,7,2
resultProduct: .asciiz "Product is: "
newline: .asciiz "\n"

.globl main
.text

main: 
	add $t0, $zero, $zero	# Loop counter
	addi $t1, $zero, 24	# Array size
	la $t9, array1		# Base address of array1
	addi $t3, $zero, 1	# Running product, initialized to 1
	
loop:

	lw $t4, 0($t9)	# Get the value in the array
	mult $t4, $t3	# Multiply the value from the array by the running product
	mflo $t3	# Get the running product and store it in $t3 again
	addi $t9, $t9, 4	# Add 4 to the base address
	addi $t0, $t0, 4	# Add 4 to the loop counter
	bne $t0, $t1, loop	# Keep iterating as long as the loop counter != array size

end: 
	# Printing the result code
	li $v0, 4
	la $a0, resultProduct
	syscall
	
	move $a0, $t3	
	li $v0, 1
	syscall 
	
	li $v0, 4
	la $a0, newline
	syscall 
	
	li $v0, 10
	syscall
