.data
array1:        .word 5, 8, 3, 4, 7, 2
array1_size:   .word 6
ans_product:   .asciiz "Product: "

.globl main
.text

main:
	LOOPINIT:
		add $t0, $0, $0 # Offset
		li $t1, 4 # Offset per item
		lw $t2, array1_size # Size of array1
		mul $t1, $t1, $t2 # Max offset = offset_per * size

		li $t2, 1 # Product
		la $t3, array1 # array1 addess
	WHILE:
		bge $t0,$t1,END
	DO:
		add $t4, $t3, $t0 # Store address + offset in $t4
		lw $t5, 0($t4)    # Store value at $t4 in $t5
		mul $t2, $t2, $t5 # Accumulate product
		addi $t0, $t0, 4  # Update offset by word_size = 4

		j WHILE
	END:

	PRINT_PRODUCT:
		# Print 'Product: '
		li $v0, 4
		la $a0, ans_product
		syscall
		
		# Print the result ($t2):
		li $v0, 1
		move $a0, $t2
		syscall

EXIT:
	li $v0, 10
	syscall
