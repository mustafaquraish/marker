.data
array1:    .word    5, 8, 3, 4, 7, 2

.globl main

#compute product of all elements and prints them
.text
main:
		add $t0, $zero, $zero		#initialize offset
		addi $t1, $zero, 24		#store size of array: 4 bytes per word * 6 word=24
		addi $t2, $zero, 1		#load value 1 in t2 to store result of multiplcation
		la $t9, array1			#load address of array in t9
loop:	
		add $t3, $t9, $t0		#address of array1 + offset
		lw $s3, 0($t3)			#load array1[i] from mem and keep result in s3
		
		mult  $t2, $s3			#multiply by result s3
		mflo $t2			#store in t2
		
		addi $t0, $t0, 4		#add 4 bytes to offset
		
		bne $t0, $t1, loop		#check loop condition and jump
end: 
		li $v0, 1			#print out final result
		move $a0, $t2
		syscall
