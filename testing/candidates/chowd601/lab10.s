.data
	array1: .word 5, 8, 3, 4, 7, 2
	opMsg: .asciiz "Product is: "
	newline: .asciiz "\n"
	
.text
	la $t0, array1 # get arr addr
	li $t1, 1 # start accumulator var
	li $v0, 6 # start count
	loop:
		lw $t2, 0($t0) # get next val
		mul $t1, $t1, $t2 # multiply into accumulator var
		addi $v0, $v0, -1 # decrement count
		addi $t0, $t0, 4 # get next word
		beqz $v0 loopDone # finish when processed count words
		j loop
	loopDone:
	
	# print prompt
	li $v0, 4
	la $a0, opMsg
	syscall
	
	# print int
	li $v0, 1
	move $a0, $t1
	syscall
	
	# print newline
	li $v0, 4
	la $a0, newline
	syscall
	
	# exit
	li $v0, 10
	syscall
	