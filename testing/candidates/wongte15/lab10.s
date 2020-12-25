.data
#declare a 6 integer array and store it in memory
array1: .word 5, 8, 3, 4, 7, 2 
#declare the size of the array for iteration
array1size: .word 6
newline: .asciiz "\n"
productMsg: .asciiz "The product is: "

#memory address formula: base + offset
	#base is address of first element
	#offset is byte_size * index
	

.globl main
.text
main: 
	#load address of array1 into a register
	#la $t1, array1
	
	#get index 0 of array1 into t2
	#lw $t2, 8($t1)
	
	#print index 0
	#li $v0, 1
	#move $a0, $t2
	#syscall
	
	la $t1, array1
	lw $t2, array1size
	
	li $v0, 1
	move $a0, $t2
	syscall
	
	li $v0, 4 	
	la $a0, newline 
	syscall
	
	LOOPINIT:
		#let t3 be the iterator
		li $t3, 0
		#let t4 be the product
		li $t4, 1
	WHILE:
		#exit condition
		beq $t3, $t2, DONE
		
		#multiply iterator by 4
		sll $t5, $t3, 2
		#add that to the first element address
		add $t5, $t5, $t1 
		#load element
		lw $t6, 0($t5)
		#print element
		li $v0, 1
		move $a0, $t6
		syscall
		li $v0, 4 	
		la $a0, newline 
		syscall
		#multiply
		mult $t6, $t4
		mflo $t4
		
		## Iterate
		addi $t3,$t3, 1
		j WHILE
	DONE:
	#Print Product
	li $v0, 4
	la $a0, productMsg
	syscall
	li $v0, 1
	move $a0, $t4
	syscall
	
	#stop program
	li $v0, 10
	syscall
	
