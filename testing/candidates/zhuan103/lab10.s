.data 
array1:     .word   5, 8, 3, 4, 7, 2
prompt:     .asciiz "The product of the array is: "
newline:    .asciiz "\n"

.globl main

.text
main:
    # Use $t0 to store loop invariant
    # Use $t1 to count remaining loop counts
    # Use $t2 to store array pointer
    li $t0, 1
    li $t1, 6
    la $t2, array1

loop_0:
    beq $t1, $zero, end_0
    lw $t3, 0($t2)
    mult $t0, $t3
    mflo $t0


    addi $t2, $t2, 4
    addi $t1, $t1, -1
    j loop_0
end_0:
    # Prompt
    li $v0, 4
    la $a0, prompt
    syscall

    # Print product to screen
    li $v0, 1
    move $a0, $t0
    syscall

    # Newline
    li $v0, 4
    la $a0, newline
    syscall

    # Terminate the program
    li $v0, 10
    syscall