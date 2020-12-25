.data
array1: .word 5, 8, 3, 4, 7, 2
size: .word 6

newline: .asciiz "\n"
.text

main:
#load 1 into t1 to be multiplied
li $t1,1
lw $t2, size # get size of list
move $t3, $zero # set counter for # of elems printed
move $t4, $zero # set offset from Array

loop:
bge $t3, $t2, end # stop after last elem is printed
lw $t0, array1($t4) # load new value
mul $t1, $t1, $t0 # multiply value
addi $t3, $t3, 1 # increment the loop counter
addi $t4, $t4, 4 # step to the next array elem
j loop # repeat the loop

end:
	#prints new line
	li $v0, 4
	la $a0, newline
	syscall 
   	#prints multiplied integer
	li $v0, 1
	move $a0, $t1
	syscall 
	#exits
	li $v0, 10
	syscall
