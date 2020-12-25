.data
array1: .word 5, 8, 3, 4, 7, 2
iterator: .word 0
size: .word 6

.globl main1
.text
	
main1: 
    la $t0 array1
    lw $t1 iterator
    lw $t2 size
    li $t3 1
run:
    bge $t1 $t2 exit
    sll $t4 $t1 2
    addu $t4 $t4 $t0
    lw $t7 0($t4)
    mult $t3 $t7
    mflo $t3
    addi $t1 $t1 1 
    j run
    
exit:
	li $v0 1
	move $a0 $t3
	syscall
	li $v0 10
	syscall
	
