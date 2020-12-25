.data 
array1: .word 5, 8, 3, 4, 7, 2
product: .asciiz "The product is: "

.globl main
.text

main: 
    la $t0, array1	#load address of array base
LOOPINIT:  
	li $t1, 0	#loop counter/offset
	li $t2, 1	#variable holds product
WHILE:	
	bgt $t1, 20, END	#loop condition, jump to END block after 6 iterations
	add $t3, $t0, $t1	#increments base by offset
	lw $t3, 0($t3)		#loads array1[i] to register
	mul $t2, $t2, $t3	#computes current product
	
	add $t1, $t1, 4		#increments counter/offset, i+=4
	
	j WHILE		#loops back to start of loop
	
END:	li $v0, 4		      
	la $a0, product
	syscall   	#print product message
	
	li $v0, 1
	move $a0, $t2
	syscall		#print product of all the numbers

	li $v0, 10
	syscall