.data
array1:	.word	5, 8, 3, 4, 7, 2
productIs: .asciiz "Their product is: "
newLine: .asciiz "\n"

.globl main
.text

main:
# prod($t1) = 1;
	li $t1, 1
# nnumbers($t0) = 6;
	li $t0, 6
# p = array1;
	la $t3, array1
# while($t0 != 0) {
moreNumbers:
	beqz $t0, finish
	# curr = *p;
	lw $t2, 0($t3)
	# prod *= curr;
	mult $t1, $t2
	mflo $t1
	# $t0--;
	addi $t0, $t0, -1
	# p += 4;
	addi $t3, $t3, 4
# }
	j moreNumbers
finish:
# printf("%s%d\n", promptN);
	li $v0, 4
	la $a0, productIs
	syscall
	li $v0, 1
	move $a0, $t1
	syscall
	li $v0, 4
	la $a0, newLine
	syscall
# exit(0);
	li $v0, 10
	syscall
