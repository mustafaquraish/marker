.data
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main:
	add $t0, $zero, $zero
	addi $t1, $zero, 24
	la $t3, array1
	
	#Stores answer
	li $t9, 1
	
loop:
	#Get current number
	#Current index
	add $t4, $t3, $t0
	lw $t5, 0($t4)
	#Multiply 
	mult $t9, $t5
	mflo $t9 
	addi $t0, $t0, 4
	bne $t0, $t1, loop
	
end:
	#Print result
	move $a0, $t9
	li $v0, 1
	syscall 
