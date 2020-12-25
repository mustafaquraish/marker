.data 
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "THE RESULT IS: "
newline: .asciiz "\n"

.globl main
.text

main: 
	la $s0, array1
	addi $t1, $s0, 24
	li $t2, 1

loop:	
	beq $s0, $t1, end
	lw $t3, 0($s0)
	mult $t3 , $t2
	mflo $t2
	addi $s0, $s0, 4
	j loop

end:
	li $v0, 4
	la $a0, result
	syscall
	li $v0, 1
	move $a0, $t2
	syscall
	li $v0, 4
	la $a0, newline
	syscall 

	li $v0, 10
	syscall
