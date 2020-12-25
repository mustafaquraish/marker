.data
array1: .word 5, 8, 3, 4, 7, 2
product: .asciiz "Their product is: "
newline: .asciiz "\n"

.text
main: 
	add $t0, $zero, $zero	#t0 = 0
	la $t1, array1		#t1 = adr(array1)
	li $s2, 1		#s2 = 1

loop:
	add $t2, $t1, $t0	#t2 = t1 + t0
	lw $s1, 0($t2)		#s1 = array1[i]
	mul $s2, $s2, $s1	#s2 = s2 * s1
	addi $t0, $t0, 4	#t0 += 4 (ie i++)
	bge $t0, 24, end	#branch if t0 = 24 (ie i = 5)
	j loop
end: 
	li $v0, 4
	la $a0, product
	syscall 
	li $v0, 1	      
	move $a0, $s2
	syscall    
	
	li $v0, 4
	la $a0, newline
	syscall 
	
	li $v0, 10
	syscall