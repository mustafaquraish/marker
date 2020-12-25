.data 
array1: .word 5, 8, 3, 4, 7, 2
promptProduct: .asciiz "Product = "
newline: .asciiz "\n"

.globl main
.text

main: 

	#$t0 is index, $t1 is value, %t2 is product

    la $t0, array1
    
    li $t2, 1
    li $t4, 6

	LOOP:  
   	  lw $t1, 0($t0) 

	  mult $t2, $t1
	  mflo $t3
	  
	  move $t2, $t3
	  
	  addi $t0, $t0, 4
	  subi $t4, $t4, 1

	  bgt $t4, 0, LOOP
	DONE:
	
	#print "Product = "
 	li $v0, 4
 	la $a0, promptProduct
 	syscall

	# print product from t2
	li $v0, 1
	move $a0, $t2	
	syscall 
	
	
	li $v0, 10
	syscall
