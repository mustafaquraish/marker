.data
array1: .word 5, 8, 3, 4, 7, 2
length: .word 6
prompt: .asciiz "\n"
.globl main
.text

main:
	la $t1, array1       # put address of list into $t1
	lw $s0, 0($t1)       # get the value from array1[0]
	li $k0, 1
	lw $k1, length
	WHILE:
		addi $t1, $t1, 4	#
		addi $k0, $k0, 1
		
		lw $s1, 0($t1)
		
		mult $s0, $s1		# $s0 = $s1 * $s0
		mflo $s0		# set LO to $s0
		
		beq $k0, $k1, DONE	# if $k0 reaches 0, then BREAK THE LOOP
		
		j WHILE
	DONE:
	
	li $v0, 1
	move $a0, $s0			# print out PRODUCT i.e. $s0
	syscall
	
	li $v0, 10			# exit the program
	syscall
