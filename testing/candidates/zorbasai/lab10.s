.data 
array1: .word 5,8,3,4,7,2
productstr: .asciiz "Product of array values: "
newline: .asciiz "\n"

.globl main
.text

main: 	
	#In the main part of the program
	#t0 = array start location
	#t1 = length of array in bytes
	#t2 = offset from start of array
	#t3 = array start + offset
	#t4 = value at array start + offset
	#t5 = running product

	la $t0, array1	#Load address of array into t0
	li $t1, 6 	#Load length of array into t1
	li $t2, 4 	#Load 4 into t2
	mult $t1, $t2   #Multiply array length by 4
	mflo $t1        #Store byte length of array in t1
	
	lw $t5, 0($t0)   #Load first array value into running count
LOOPINIT: li $t2, 4	#Init offset counter to zero
WHILE:	beq $t1, $t2, END #if length of array(bytes) = offset from start of array (bytes), exit loop
	add $t3, $t0, $t2 # Add offset and array start, store in t3
	lw $t4, 0($t3) 	  #load value at arraystart+offset into t4
	mult $t5, $t4	  #multiply current value by new value
	mflo $t5	  #get product from lo
	addi $t2, $t2, 4  #increment offset by 4
	j WHILE
END:
	li $v0, 4		   #logic for printing result and exiting below this point   
	la $a0, productstr
	syscall    
	
	move $a0, $t5	
	li $v0, 1
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall 
	
	li $v0, 10
	syscall	
