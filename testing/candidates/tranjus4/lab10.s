.data
array1: .word 5, 8, 3, 4, 7, 2 # 5*8*3*4*7*2 = 6720

.globl main

.text

main: 
	
	la $t0, array1 		#load the address of array1 into $t0
	add $t1, $zero, $zero	# i = 0
	addi $t3, $zero, 1	# result = 1
	
loop:
	bgt $t1, 5, done 	# if i == 5 exit loop
	
	lw $t2, 0($t0)		# retrieve integer at address $t0 (array[i])
	mult $t3, $t2		# result = result * array1[i]
	mflo $t3
	
	addi $t0, $t0, 4	# increment address by 4
	addi $t1, $t1, 1	# increment i
	
	j loop

done:

	li $v0, 1		#print result and exit program
	move $a0, $t3
	syscall 
	li $v0, 10
	syscall
