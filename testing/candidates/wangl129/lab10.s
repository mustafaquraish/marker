.data
array1: .word 5, 8, 3, 4, 7, 2
newline: .asciiz "\n"
Result: .asciiz "Result is : "






.text
main:
	li $t4, 4
	la $t0, array1
	li $t3, 0
	lw $t5, array1
LOOP:
	add $t0, $t0, $t4
	lw $t1, 0($t0)
	add $t3, $t3, 1
	mul $t5, $t5, $t1
	bge $t3, 5, DONE
	j LOOP

DONE:
	li $v0, 4 		
	la $a0, Result
	syscall 
	
	move $a0, $t5
	li $v0, 1
	syscall
	
	li $v0, 4		      
	la $a0, newline
	syscall   
		
	li $v0, 10
	syscall
	