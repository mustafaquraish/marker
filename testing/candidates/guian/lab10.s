.data
array1: .word 5,8,3,4,7,2

.text

main:
	add $t0, $zero, $zero # load “0” into $t0
	addi $t1, $zero, 24 # load “400" into $t1
	li $t2, 1
	la $t8, array1 # store address of A
loop:
	add $t3, $t8, $t0 # $t4 = addr(A) + i
	lw $s4, 0($t3) # $s4 = B[i]
	mult $t2, $s4
	mflo, $t2
	
	addi $t0, $t0, 4 # $t0 = $t0++
	bne $t0, $t1, loop # branch back if $t0<400
end:

li $v0, 1
move $a0, $t2
syscall

li $v0, 10
syscall