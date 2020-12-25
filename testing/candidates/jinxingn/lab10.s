.data 
array1: .word 5,8,3,4,7,2
size: .word 6
promptA: .asciiz "The product is: "
newline: .asciiz "\n"

.globl main
.text

main:
	# $a1 is the address of the first element of array1
	la $a1, array1
	
	# $t0 is the answer (product of the array)
	li $t0, 1
	
	# $t1 is the size of the array
	lw $t1, size
	
	# $t3 is the counter
	li $t3, 0
	
	WHILE:
	# check if the list size has reached
	beq $t3, $t1, DONE
	
	# $t2 is the current element in the array
	lw $t2, 0($a1)
	
	# multiply $t2 to the answer
	mul $t0, $t0, $t2
	
	# counter++
	addi $t3, $t3, 1
	
	# move to the next address (4 byte for int)
	addi $a1, $a1, 4
	
	# loop
	j WHILE
	
	DONE:
	# print the prompt
	li $v0, 4
	la $a0, promptA
	syscall
	
	# print the answer
	li $v0, 1
	move $a0, $t0
	syscall
	
	# exit
	li $v0, 10
	syscall