.data 
array1: .word 5, 8, 3, 4, 7, 2
resultProduct: .asciiz "Product: "
newline: .asciiz "\n"

.text
main: 
	add $t0, $zero, $zero # $t0 = offset i, initial value "0"
	addi $t1, $zero, 24   # $t1 = 24 (6 ints: 6x4 bytes)
	la $t2, array1        # store address of array1 in $t2
	addi $t8, $zero, 1    # $t8 stores the product result, initial value "1"
LOOP:
	add $t3, $t2, $t0  # $t3 = addr(array1) + i
	lw $t4, 0($t3)     # t4 = array1[i]
	mult $t8, $t4      # multiply current value with previous product
	mflo $t8           # store current product in $t8
	addi $t0, $t0, 4   # $t0++
	bne $t0, $t1, LOOP # branch back if $t0<24
END:
	li $v0, 4
	la $a0, resultProduct
	syscall
	
	li $v0, 1
	move $a0, $t8
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall
	
	li $v0, 10
	syscall
