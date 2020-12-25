 .data 
array1: .word 5, 8, 3, 4, 7, 2
promptA: .asciiz "5 * 8 * 3 * 4 * 7 * 2 = "
newline: .asciiz "\n"
.globl main
.text


main:  
        # counter $t0
        add $t0, $zero, $zero
        # size of array 
        addi $t1, $zero, 24
        # address of first ele in $t2
        la $t2, array1
 
        # product 
        li $t9, 1
        
        
loop:
        # address of current ele in $t3
        add $t3, $t2, $t0
        # load current ele to $s1
        lw $s1, 0($t3)
        # update product 
        mult $s1, $t9
	mflo $t9
	
	# update conuter
	addi $t0, $t0, 4
	
	# check loop condition and jump
	bne $t0, $t1, loop
	
	
end:
        # print product 
        li $v0, 4		      
	la $a0, promptA
	syscall 
	
	move $a0, $t9	
	li $v0, 1
	syscall 

	li $v0, 4
	la $a0, newline
	syscall 

	li $v0, 10
	syscall