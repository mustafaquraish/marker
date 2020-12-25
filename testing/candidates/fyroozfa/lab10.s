.data 
array1: .word 5, 8, 3, 4, 7, 2
resultProduct: .asciiz "The product is: "


.globl main
.text

main: 
	li $t7, 1			#product starts at 1 and is stored at $t7
	la $t6, array1			#load address of array1 and store it in $t6
	add $t0, $zero, $zero		# initial value w/ offset 0 stored in $t0
     	addi $t1, $zero, 24 		#6 * 4 = 24 b/c 6 ints w/ 4 bytes each stored in $t1
     	
	
	
	FOR: 
		
		add $t2, $t6, $t0	#address of array1[offset] is (address of array1: t6) + offset: t0
					#store address of array1[offset] in t2
		lw $t3, 0($t2)		#get int stored at $t2, store it in $t3
		mul $t7, $t7, $t3	#multiply product so far * array1[i] (ie $t3) and store new product in $t7
		addi $t0, $t0, 4	#adds 4 to offset
		blt $t0, $t1, FOR	#if offset < 24, then go back to for
		

	DONE:
		li $v0, 4
		la $a0, resultProduct
		syscall	
		
		li $v0, 1
		move $a0, $t7			
		syscall
		
		li $v0, 10
		syscall

