.data
prompt: .asciiz "Enter a number: "
result: .asciiz "The result is: "
newline: .asciiz "\n"
# MAX NUMBER IS 46340, arithmetic overflow on ADD, 32 bit registers
.text
main:
	li $t2, 2 # constant used for multiplication later
	
	li $v0, 4
	la $a0, prompt	
	syscall	
	
	li $v0, 5
	syscall
	move $t0, $v0 #load int into t0
	
	addi $sp, $sp, -4
	sw $t0, 0($sp) #store int in stack
	
	jal mystery
	
	lw $t1, 0($sp) #retrieves int in the stack
	addi $sp, $sp, 4 
	
	li $v0, 4
	la $a0, result
	syscall
	li $v0, 1
	move $a0, $t1	
	syscall 	

	li $v0, 10 	
	syscall 	
	
# start of function mystery()
mystery:
	
	lw $a0, 0($sp) #retrieves number from stack
	addi $sp, $sp, 4 
	
	addi $sp, $sp, -4
	sw $ra, 0($sp) #store previous return
	
	beq $a0, $zero, THEN #n == 0
	
	subi $v0, $a0, 1 # v0 = n - 1
	
	# store n and n-1 into the stack
	addi $sp, $sp, -4 
	sw $a0, 0($sp) 
	
	addi $sp, $sp, -4 
	sw $v0, 0($sp) 
	
	jal mystery
	
	# retrieve mystery return value, mystery(n - 1), n
	lw $a1, 0($sp)
	addi $sp, $sp, 4
	
	lw $a0, 0($sp)
	addi $sp, $sp, 4 
	
	mult $t2, $a0
	mflo $a0	
	add $v0, $a1, $a0 
	subi $v0, $v0, 1  # v0 = $a1 + 2(a0) - 1
	
	# base case, just return and jump back
	THEN:   	
		lw $ra, 0($sp) #load return address
		sw $v0, 0($sp) #stores return value
	
	jr $ra 
