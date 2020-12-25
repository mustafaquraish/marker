.data
output: .asciiz "The product is: "
newline: .asciiz "\n"
array1: .word 5, 8, 3, 4, 7, 2

.text
main: 
  LOOPINIT:
    li $t1, 0
    li $t3, 24
    li $t2, 1
    la $t9, array1

  LOOPBODY:
    add $t4, $t9, $t1
    lw $t0, 0($t4)
    mult $t2, $t0
    mflo $t2

    addi $t1, $t1, 4
    bne $t1, $t3, LOOPBODY
  
  DONE:
    li $v0, 4
    la $a0, output
    syscall

    li $v0, 1
    mflo $a0
    syscall

    li $v0, 4
    la $a0, newline
    syscall 

    li $v0, 10
    syscall
