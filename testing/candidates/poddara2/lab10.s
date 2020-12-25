.data
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "The product is: "
product: .word 1

.text

main:
	add $t0, $zero, $zero		#offset
	lw $t1, product			#running product
	addi $t2, $zero, 6		#num elements
	la $t3, array1			
	
loop:
	add $t8, $t3, $t0		#t8 stores array1 + offset
	lw $t4, ($t8)
	
	multu $t1, $t4
	mflo $t1
		
	addi $t0, $t0, 4
	subi $t2, $t2, 1
	bne $t2, 0, loop

li $v0, 4
la $a0, result
syscall

move $a0, $t1
li $v0, 1
syscall

li $v0, 10
syscall

	

