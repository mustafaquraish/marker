.data 
ArrayProduct: .asciiz "Product of All Elements in Array: "
NewLine: .asciiz "\n"
N: .word 5
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

# $v for function returns
# $a for function arguments
# $t temporary caller saved registers
# $s callee saved

main: 
	LOOPINIT:
	
		# store address of array1
		la $t1, array1 
		li $t2, 1
		lw $t3, N
		sll $t3, $t3, 2
		add $t3, $t3, $t1
		
	WHILE: 
		# while t1 is less than or equal t3
		bgt $t1, $t3, DONE
		
		# Multiply array element by old product
		lw $t0, ($t1)
		mul $t2, $t0, $t2
  		
  		# Output product after current index
		li $v0, 1
    		move $a0, $t2
    		syscall
    		
    		# Output new line after each product
		li $v0, 4		      
		la $a0, NewLine
		syscall   
		
		# next element
		addi $t1, $t1, 4
		
		j WHILE

	DONE: # This label marks the end of the loop.
    	
    	# Output description
	li $v0, 4		      
	la $a0, ArrayProduct
	syscall   
	
	# Output product of array
	li $v0, 1
    	move $a0, $t2
    	syscall
	
	
	
	
	
