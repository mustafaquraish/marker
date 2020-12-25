.data
array1: .word 5, 8, 3, 4, 7, 2
size: .word 6
res: .asciiz "RESULT: "

.text
main:
	la $t0, array1
	add $t1, $zero, $zero
	
	lw $t2, size
	addi $t7, $t7, 4
	mult $t2, $t7
	mflo $t2
	
	add $t3, $zero, $zero
	addi $t4, $zero, 1
	add $t5, $zero, $zero
WHILE:
	beq $t1, $t2, END
	add $t5, $t0, $t1
	lw $t3, 0($t5)
	mult $t3, $t4
	mflo $t4
	addi $t1, $t1, 4
	j WHILE
END:
	addi $v0, $zero, 4
	la $a0 res
	syscall
	addi $v0, $zero, 1
	add $a0, $t4, $zero
	syscall
	
	li $v0, 10
	syscall
	 