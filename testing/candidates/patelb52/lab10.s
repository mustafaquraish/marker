.data 
array1: .word  5, 8, 3, 4, 7, 2

.globl main
.text

main: 
    		addi $t0, $zero,  0    #load into t0
    		addi $t1, $zero, 1    # load 1 into t1 to hold mutiplication
    		addi $t2, $zero, 24   # load size of array to t2
    		la $t3, array1  # store address of array1
	WHILE:
		beq $t0, $t2, DONE
		add $t4, $t3, $t0 
   		lw $t5, 0($t4)
   		mul $t1, $t1, $t5
   		addi $t0, $t0, 4
		j WHILE
	DONE:
		li $v0, 1
		move $a0, $t1
		syscall

	li $v0, 10 # exit cmd
	syscall
	
	
	
	
	
	
	
