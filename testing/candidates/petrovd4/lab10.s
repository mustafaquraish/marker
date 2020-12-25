.data
result: .asciiz "Product: "
array: .word 5, 8, 3, 4, 7, 2  # -> 6720
#array: .word 1, 1, 2, 3, 1, 1 # ->  6
arrayLen: .word 24 # (len(Array))*4
.text
main:
	INIT:
		#Iterator i
		li $t1, 0
		#Product
		li $t2, 1
		#Array
		la $t3, array
		#len(Array)-1
		lw $t5, arrayLen
	
	
	# product = 1; 
	# for (i=0; i<len(A); i++): product *= A[i];
	
	FOR:
		beq $t1, $t5, END        #for (--; i<len(A); --). Once equal, done loop
		add $t4, $t3, $t1 	 # b = addr(Array)+i
		lw $s1, 0($t4)		 # Load A[b] to c
		mult $t2, $s1  		 # a = Product * Array[i]
		mflo $t2       		 # Product = Product * a
		
		addi $t1, $t1, 4 	  #i++
		j FOR
	

	END:	
		#Print result	
		li $v0, 4
		la $a0, result
		syscall
	
		li $v0, 1
		add $a0, $zero, $t2
		syscall
	
		#Exit program
		li $v0, 10 	
		syscall 		
		
			
	
	
