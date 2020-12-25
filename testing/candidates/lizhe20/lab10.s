.data
	array1: .word 5, 8, 3, 4, 7, 2
	arrLenL: .word 6
.text
	la $s0, array1 # arr addr
	lw $t1, arrLenL # len
	addi $t1, $t1, -1 # offset by -1 to index
	li $s1, 4 # offset constant

	li $t0, 0 #  counter
	for: 
		mult $t0, $s1 #index
		mflo $t3 # store index in t3
		add $t4, $s0, $t3
		
		li $v0, 1
		lw $a0, 0($t4)
		syscall # print the element at index num
		
		beq $t0, $t1, end # condition
		addi $t0, $t0, 1 # increment
		j for
end:
	li $v0, 10 	# system call code for exit
	syscall 	# terminate program	
		