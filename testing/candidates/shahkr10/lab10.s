.data
before: .asciiz "Before function\n"
promptA: .asciiz "Enter value for A: "
promptB: .asciiz "Enter value for B: "
resultAdd: .asciiz "Mystery: "
resSub: .asciiz "A - B is: "
newline: .asciiz "\n"

.text
main:
	li $v0, 4		      
	la $a0, promptA
	syscall    
	li $v0, 5
	syscall 
	move $a0,$v0
	jal mystery
	move $t1,$v0
	li $v0, 4
	la $a0, resultAdd
	syscall
	move $a0, $t1
	li $v0, 1	
	syscall 	
	li $v0, 4
	la $a0, newline
	syscall 	
	# End of main, make a syscall to "exit"
	li $v0, 10 	# system call code for exit
	syscall 	# terminate program	
	
	


mystery:
	addi $sp, $sp, -4 
	sw $ra, ($sp)  #add ra to stack\
	bnez $a0, nZero
 	li $v0, 0
 	lw $ra, 0($sp) # pop $ra from stack
	addi $sp, $sp, 4 
	jr $ra
 nZero:
 	add $t9, $a0, $t9
	add $t9, $a0, $t9
	addi $t9, $t9	,-1
	addi $a0,$a0,-1
 	jal mystery
 	add $v0,$v0,$t9
 	li $t9,0  #ifyou comment this out you get n^3
 	lw $ra, 0($sp) # pop $ra from stack
	addi $sp, $sp, 4 
	jr $ra
 	