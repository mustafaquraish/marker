.data
array1: .word 5,8,3,4,7,2

.text
main :
    #size of array = length * 4 (bytes / element)
    addi $t1, $zero, 24

    #address of array
    la $t9, array1

LOOPINIT:
    #counter
    add $t0, $zero, $zero # $t0 = 0

    #product
    li $t2, 1 # $t2 = 1

WHILE:
    beq $t0, $t1, BREAK  # if $t0 == N  break

    #obtain address of the ith element
    add $t3, $t9, $t0  # $t3 = address of array + offset

    #load element from array
    lw $s0, 0($t3)

    #update product
    mult $t2,$s0
    mflo $t2

    #increment offset    
    addi $t0, $t0, 4  # t0+=4
    
    j WHILE

BREAK:
    #print product
    li $v0, 1
    move $a0, $t2
    syscall

    #exit	
	li $v0, 10 
	syscall
