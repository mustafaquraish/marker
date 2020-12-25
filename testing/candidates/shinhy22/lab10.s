
.data


array1:		.word	5, 8, 3, 4, 7, 2


.text
	
	la $t0, array1
	li $t1, 1
	
	li $t6, 6
	li $t7, 0

loop:
	beq $t6, $t7, exit
	
	lw $t3, 0($t0)
	
	mul $t1, $t1, $t3
	
	addi $t0, $t0, 4
	addi $t7, $t7, 1
	j loop

exit:
	li $v0, 1
	move $a0, $t1
	syscall
	
	li $v0, 10
	syscall
	
	
