.data
array1:	.word 5,8,3,4,7,2

.text
main:
	add $t0, $zero, $zero	#store index i to $t0
	addi $t1, $zero, 24	#array size
	la $t9, array1	#store address of array1
	addi $t8, $zero, 1	#store 1 to $t8

loop:
	add $t4, $t9, $t0	# $t4 = array1 + i
	lw $s4, 0($t4)		# $s4 = array1[i]
	mult $s4, $t8	# mult $s4 and $t8, store to hi, lo
	mflo $t8	# move lo to $t3
	addi $t0, $t0, 4	# $t0 = $t0 + 4
	bne $t0, $t1, loop	#back to loop if $t0 not euqls to $t1
	
end:	
	li $v0, 1	# print the result
	move $a0, $t8
	syscall
	
	li $v0, 10
	syscall		# end the program
	
