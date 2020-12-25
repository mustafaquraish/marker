.data 

productMsg: .asciiz "THE PRODUCT IS:  "
newline: .asciiz "\n"
array1: .word    5, 8, 3, 4, 7, 2

.globl main
.text

main: 
	li $t0, 1  # product
	la $t1, array1  # address
	add $t2, $zero, $zero  # counter
	addi $t3, $zero, 24  # 24
	
loop:
	bge $t2, $t3, end
	add $t4, $t2, $t1
	lw $s1, 0($t4)
	
	mult $s1, $t0
	mflo $t0  # update product
	
	addi $t2, $t2, 4
	j loop



end:
	# print product
	li $v0, 4
	la $a0, productMsg
	syscall
	

	li $v0, 1
	move $a0, $t0
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall 


	li $v0, 10
	syscall
        
	
