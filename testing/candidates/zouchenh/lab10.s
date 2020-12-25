
.data
# TODO: What are the following 5 lines doing?
promptA: .asciiz "Enter the number of times you want to multiply: "
promptB: .asciiz "Enter an int: "
result: .asciiz "The result is = "
newline: .asciiz "\n"
int: .word 1
array1:    .word    5, 8, 3, 4, 7, 2



.globl main
.text

main: 




	#li $v0, 4		      
	#la $a0, promptA
	#syscall    

	#li $v0, 5
	#syscall 
	

	#move $t0, $v0
	

LOOPINIT:

    li $t0, 6
    li $t1, 0
    li $t2, 1
    la $s0, array1
    #li $t3, 0
    
    
    
    
	

WHILE:

	beq  $t1,$t0,DONE
	
	lw $t3, 0($s0)
	
	mul $t2, $t2, $t3
	
	addi $s0, $s0, 4

    	addi $t1,$t1, 1
    	
    	#addi $t3, $t3, 4
	
	#li $v0, 4		      
	#la $a0, promptB
	#syscall    


	#li $v0, 5
	#syscall 
	
	#move $t3, $v0

	#mul $t2, $t2, $t3
	

    	j WHILE

DONE:
	
	li $v0, 4
	la $a0, result
	syscall
	
	li $v0, 1
	move $a0, $t2	
	syscall
	
	li $v0, 4
	la $a0, newline
	syscall 

	li $v0, 10
	syscall
