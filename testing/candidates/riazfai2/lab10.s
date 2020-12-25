.data 
# TODO: What are the following 5 lines doing?
array1: .word 5, 2, 3, 4, 1, 2
newline: .asciiz "\n"
N: .word 5

.globl main
.text

main: 
	#initial number this will store our product
	li $t1, 1
	#initializing array[0] to t9
	la $t9, array1
	#4*6=24, 4 bytes per int, our array has 6 ints
	addi $t3, $zero, 24
	#zero into t2, which is my i
	add $t2, $zero, $zero
	
	LOOPINIT: # Many loops have an initialization section.
		  # Nothing
	WHILE: # The loop checks the condition, then evaluates the body.		
		add $t4, $t9, $t2 #t4 = array[t9] + i
		lw $s4, 0($t4) #make s4 equal to value of index
		move $t5, $s4 #move s4 into t5
		mul $t1, $t1, $t5 #t1 = t1 * t5
		addi $t2, $t2, 4 # i = i + 4
		bne $t2, $t3, WHILE #branch WHILE if t2<24
	
	#Print out t1
	li $v0, 1		      
	move $a0, $t1
	syscall 
	


