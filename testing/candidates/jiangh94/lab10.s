.data 

result: .asciiz "The product of all elements in array1 is: "
array1: .word 5, 8, 3, 4, 7, 2
newline: .asciiz "\n"

.globl main
.text

main: 
	la $t8, array1
	
	LOOPINIT:		
		li $t0, 0  #The index (i)
		li $t1, 1  #The product (acc value)
		li $t2, 6  #Length of the array
		
		
	WHILE:
		bge $t0, $t2, DONE  #Loop condition
		
		sll $t4, $t0, 2  #Turn i into a byte offset (*4)
		add $t4, $t8, $t4  #A[i] address
       	 	lw $t3, 0($t4)  #A[i] content
       	 	
       	 	mult $t1, $t3 #Multiplication
       	 	mflo $t1
       	 	
       	 	addi $t0, $t0, 1 #Next index
       	 	j WHILE

	DONE:
	li $v0, 4 	                
	la $a0, result      
	syscall
	
	li $v0, 1 	                
	move $a0, $t1     
	syscall
	
	li $v0, 4 	                
	la $a0, newline      
	syscall
	
	li $v0, 10
	syscall
