.data
	array1: .word 5, 8, 3, 4, 7, 2
	
.text
main:
	la $t0, array1
	li $t1, 0
	li $t2, 1
	
loop:
	bgt $t1, 5, done
	lw $t4, 0($t0)
	mul $t2, $t2, $t4
	addi $t1, $t1, 1
	addi $t0, $t0, 4
	j loop
	
done:
	li $v0 1
	move $a0, $t2
	syscall
	
	li $v0, 10
	syscall