.data
array1: .word 5, 8, 3, 4, 7, 2
newline: .asciiz "\n"

.text
main:
    li      $s0, 6 # array length
    li      $s1, 0 # iterator
    la      $s2, array1 # array addresss
    li 		$s4, 1
    while_loop:
            beq         $s1, $s0, while_loop_exit

            li          $s3, 4
            mult        $s1, $s3
            mflo        $s3

            add         $s3, $s3, $s2

            lw          $a0, 0($s3)
            
            mult		 $s4, $a0
            mflo		 $s4

            addi        $s1, $s1, 1
            j           while_loop
    while_loop_exit:

   move $a0, $s4
	li          $v0, 1
    syscall 

	li $v0, 10 	
	syscall 
	
 	 
