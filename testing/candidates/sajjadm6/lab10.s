.data
array1: .word 5,8,3,4,7,2

.globl main
.text

main:
	la $t9, array1
	add $t0, $zero, $zero
	addi $t1, $zero, 24
	li $t3, 1
	
loop:
	beq $t0, $t1, end
	add $t2, $t9, $t0
	lw $s4, 0($t2)
	mul $t3, $t3, $s4
	addi $t0, $t0, 4
	j loop

end:
	li $v0, 1
	move $a0, $t3
	syscall 

	li $v0, 10
	syscall
	
	
	
