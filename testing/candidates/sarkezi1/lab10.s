.data
array1:    .word    5, 8, 3, 4, 7, 2
arraySize: .word 20 
.globl main

.text
main: 
    LOOPINIT:
	la $t0, array1
        lw $t1, arraySize
        add $t2, $t0, $t1
        
        
    WHILE:
        lw $a0, 0($t0)
	li $v0, 1
	syscall

        IF:
            beq $t0, $t2, ELSE
            
        THEN:
            addi $t0, $t0, 4
            j WHILE
            
        ELSE:
            j DONE

    DONE:

    	li $v0, 10 
	syscall 
