# func1.s
.data
product: .asciiz "The Product of the array elements is "
newline: .asciiz "\n"
array1:    .word    5, 8, 3, 4, 7, 2
 
.text
main:
	li $v0, 4	
	la $a0, product
	syscall
	
	li $t2,1	#product value is calculated here
	la $t0,array1
	LoopInit:
	li $t3,0
	While:
	beq $t3,6,Exit
	lw $t1,($t0)
	mul $t2,$t1,$t2
	
	addi $t0,$t0,4
	addi $t3,$t3,1
	j While
	
Exit:
	li $v0,1
	move $a0,$t2
	syscall
	
	li $v0,10
	syscall