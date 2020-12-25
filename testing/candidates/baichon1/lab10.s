.data
array1: .word 5, 8, 3, 4, 7, 2
promptA: .asciiz "The Product of the array is: "


.globl main
.text
main: 
	li $t0, 0			#t0 = 0
	li $t1, 1			#t1 = product
	li $t7, 24			#t7 = 24
	la $t2, array1			#t2 stores array1 address
	while:
		beq $t0, $t7, END	#break when i == 24
		add $t3, $t2, $t0	#t3 = address(array1) + i
		lw $t4, 0($t3)		#t4 = array1[i]
		mul $t1, $t1, $t4	#t1 = t1 * t4
		addi $t0, $t0, 4	#i = i + 4
		j while
	END:
	
		#print promtA
		li $v0, 4			#get ready to print what is in $a0
		la $a0, promptA			#put the address of promtA into $a0
		syscall				#execute

		
		#print result $t1
		li $v0, 1
		move $a0, $t1
		syscall 
		
		
		li $v0, 10	#exit
		syscall
	
	
	
	
	
