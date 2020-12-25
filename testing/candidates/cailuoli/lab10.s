.data
array: .word 1, 2, 3, 4, 5, 6

.globl main
.text

main:
li $t1, 0
li $t2, 0

while:
beq $t1, 24, end
lw $t3, array($t1)
addi $t1, $t1, 4
add $t2 ,$t2, $t3
j while

end:
li $v0, 1
move $a0, $t2
syscall

li $v0, 10
syscall