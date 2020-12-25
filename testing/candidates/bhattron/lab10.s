
.data
array1:    .word    5, 8, 3, 4, 7, 2
arraySize: .word 20 #5*4
.globl main

.text
main: 
    LOOPINIT:
	la $t0, array1
        lw $t1, arraySize
        add $t2, $t0, $t1
        li $t3, 1
	WHILE:
        	lw $a0, 0($t0)
		mult $t3, $a0
		mflo $t3
        IF:
            beq $t0, $t2, ELSE
        THEN:
            addi $t0, $t0, 4
            j WHILE
        ELSE:
            j DONE

    DONE:
	li $v0, 1
	move $a0, $t3
	syscall 

    	li $v0, 10 	# system call code for exit
	syscall 	# terminate program	
