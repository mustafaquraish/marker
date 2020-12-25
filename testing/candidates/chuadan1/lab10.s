.data
array1: .word 5, 8, 3, 4, 7, 2
size: .word 6

.globl main
.text

main: 
	la 	$t0, array1 # starting address of array
	lw 	$t1, size # size of array
	li 	$t2, 0 # counter
	li 	$t3, 1 # accumulator
	WHILE:
		beq 	$t1, $t2, DONE
		lw 	$t4, ($t0) # load array value
		mult 	$t3, $t4 # multiply
		mflo 	$t3 # move back to accumulator
		
		addi 	$t2, $t2, 1 # increase counter
		addi 	$t0, $t0, 4 # increase pointer 
		j 	WHILE
	DONE:

print_results:
	li 	$v0, 1
	move 	$a0, $t3
	syscall
	
exit:
	li 	$v0, 10
	syscall