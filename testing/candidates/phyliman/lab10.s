.data 
newline: .asciiz "\n"
array1: .word 5, 8, 3, 4, 7, 2
iterator: .word 0
size: .word 6
byte: .word 4

.globl main
.text

main: 
	la $t0, array1  
	lw $t1, iterator
	lw $t2, size
	lw $t3, byte
	li $t4, 1
	
	LOOP:
	beq $t1, $t2, ENDLOOP
	#Iterator x Bytes
	mul $t5, $t1, $t3
	#Get the array's element
	lw $t6, array1($t5)
	#Multiply to current product
	mul $t4, $t4, $t6
	
	#Increment interator
	addi $t1, $t1, 1
	j LOOP
	
	ENDLOOP:
	#print the product of the arrays' elements
	li $v0, 1
	move $a0, $t4
	syscall

	#end the program
	li $v0, 10
	syscall	
