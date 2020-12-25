.data
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "The total product is: "

.globl main
.text

main:

loopinit:
	la $t0, array1
	li $t1, 0
	lw $t2, 0($t0)

loop:
	bge $t1, 5, end
	addi $t0, $t0, 4
	lw $t3, 0($t0)
	mult $t2, $t3
	mflo $t2
	addi $t1, $t1, 1
	j loop

end:
	li $v0, 4		      
	la $a0, result		# print result
	syscall

	li $v0, 1
	move $a0, $t2		# print product
	syscall
	
	li $v0, 10		# exit program
	syscall
