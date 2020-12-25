.data
array1: .word 5, 8, 3, 4, 7, 2

.globl main
.text

main: 

# the basic way to compute memory address of an element is 
# base + offset, base = ma of array1, offset = index of element * size of each element

# load address of first element into $s0
la $s0, array1

# load initial value of product into $t0
li $t0, 1

# store the initial value (0) of increment variable in $t1
add $t1, $zero, $zero

# load the max value (24) of increment variable in $t8
addi $t8, $zero, 24


WHILE:
# store the address of current element in $t2
add $t2, $s0, $t1

# load the value at address stored in $t2 (value of current element)
lw $s4, 0($t2)

# do multiplication between previous value of product and current element and store result in $t0
mult $t0, $s4
mflo $t0

# increment the loop variable by 4 (because of word type: 4-bytes)
addi $t1, $t1, 4

# check loop condition (if $t8 != 24)
bne $t8, $t1, WHILE
END:

# print product
li $v0, 1
la $a0, ($t0)
syscall

# exit program
li $v0, 10
syscall
