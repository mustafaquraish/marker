.data 
# TODO: What are the following 5 lines doing?
array1: .word 5, 8, 3, 4, 7, 2
prompt: .asciiz "Product is: "
#t0 = counter
#t1 = max
#t2 = array start address
#t3 = current address
#t4 = product
.globl main
.text

main: 
   	# load counter
   	add $t0, $zero, $zero
   	# load max
   	addi $t1, $zero, 24
	#load array address
	la $t2, array1
	#init product counter
	li $t4, 1		      	
		

LOOP:
	#update counter location
	add $t3, $t2, $t0 	#t3 = start + counter
	lw $s4, 0($t3) 		#
	mult $t4, $s4
	mflo $t4
	addi $t0, $t0, 4 #counter ++
	bne $t0, $t1, LOOP #if counter < 24 loop
		
END:
#end loop here
    	
    	#Print Product
    	li $v0, 4
    	la $a0, prompt
    	syscall 
    	
    	li $v0, 1 #print int
	move $a0, $t4 
	syscall 
    	
	#EXIT
	li $v0, 10
	syscall
