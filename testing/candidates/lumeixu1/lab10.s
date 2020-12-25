.data
array1: .word 5, 8, 3, 4, 7, 2
result: .asciiz "Now we have: "
newline: .asciiz "\n"
.text

main:
	#initialize
	add $t0, $zero, $zero #i=0
	addi $t1, $zero, 24 #size = 6*4 = 24
	addi $t2, $zero, 1 #count = 1
	la $t8, array1 #get &array1
	
	#for(i=0,i<6,i++) count *= a[i]
loop:   add $t3, $t8, $t0 # $t3 = addr(A) + i -- which is an address
	lw $t4, 0($t3) # $t4 = value of A[i]
	mult $t4, $t2
	mflo $t2 #count multiply and update
	#print string "Now we have "
	li $v0, 4
	la $a0, result
	syscall
	# print the actual value
	li $v0, 1
	move $a0, $t2	
	syscall 
	# print newline
	li $v0, 4
	la $a0, newline
	syscall
	#update
	addi $t0, $t0, 4 #i++
	bne $t0, $t1, loop
	
	#here we end our program
	li $v0, 10
	syscall
