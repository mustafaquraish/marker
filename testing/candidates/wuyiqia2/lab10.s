.data
#A + 42 and B - A

array1:   .word    5, 8, 3, 4, 7, 2

sumMsg: .asciiz "Sum = "
newline: .asciiz "\n"

.globl main
.text

main: 	
	add $t0, $zero, $zero
	addi $t2, $zero, 24  # 4*6=24
	la $t8, array1
	# set sum in to regisiter t1
	addi $t1, $zero, 1
	
	j LOOP

LOOP:
	beq $t0, $t2, END

	add $t4, $t8, $t0
	lw $s4, 0($t4)
	addi $t5, $s4, 0
	
	mult $t1, $t5
	
	mflo $t1
	
	addi $t0, $t0, 4
	j LOOP
	
END:
#print evenMsg
	li $v0, 4
	la $a0, sumMsg
	syscall
	
	li $v0, 1
	move $a0, $t1
	syscall
	
#stop program
	li $v0, 10
	syscall
	
#print newline
	#li $v0, 4 	
	#la $a0, newline 
	#syscall