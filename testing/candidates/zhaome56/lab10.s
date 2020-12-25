.data
array1: .word 5,8,3,4,7,2

.text
main:
	add $t0, $zero, $zero 
	addi $t1, $zero, 24 
	addi $t2, $zero, 1 
	la $t8,array1
	
loop: 
	add $t3, $t8, $t0 
	lw $s4, ($t3)
	mul $t2, $s4, $t2 
	addi $t0, $t0, 4 
	bne $t0, $t1, loop 

End:
	li $v0, 1
	la $a0, ($t2)
	syscall

	li $v0,10
	syscall