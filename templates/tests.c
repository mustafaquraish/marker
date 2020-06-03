/**
 * This is a template for a basic testing file that can be used to test the
 * exercises / assignments. It is accompanied by the template `testsuite.csv`
 * file also found in the current directory.
 * 
 * (C) Mustafa Quraish, 2020
 */

#define __testing__   

/* Import student's code here! */

#include <assert.h>
#include <stdlib.h>
#include <stdio.h>

/* ------------------------------------------------------------------------- */
/*                              TEST CASES                                   */
/* ------------------------------------------------------------------------- */
/*     Each function is one test case. If the test case does not pass        */
/*     then the function should exit with a non-zero status. Using the       */
/*     <assert.h> library to perform the checks does this automatically.     */
/* ------------------------------------------------------------------------- */

void test_00() {
  assert(1 == 1);
  return;   // Passed
}

void test_01() {
  assert(2 + 2 == 4);
  return;   // Passed
}

void test_02() {
  assert(2 + 2 == 4);
  return;   // Passed
}

// Other test cases go here, including helper functions to check correctness
// For eg: compare_linked_lists(...)


/* ------------------------------------------------------------------------- */
/*                CHANGE THE VALUES HERE BASED ON YOUR TESTS                 */
/* ------------------------------------------------------------------------- */

// Change this to the number of tests you have
#define NUMTESTS 60


// Remove all the ones you don't need.
void (*TESTS[NUMTESTS])() = {
  test_00, test_01, test_02, test_03, test_04, 
  test_05, test_06, test_07, test_08, test_09, 
  test_10, test_11, test_12, test_13, test_14, 
  test_15, test_16, test_17, test_18, test_19, 
  test_20, test_21, test_22, test_23, test_24, 
  test_25, test_26, test_27, test_28, test_29,
  test_30, test_31, test_32, test_33, test_34, 
  test_35, test_36, test_37, test_38, test_39, 
  test_40, test_41, test_42, test_43, test_44, 
  test_45, test_46, test_47, test_48, test_49, 
  test_50, test_51, test_52, test_53, test_54, 
  test_55, test_56, test_57, test_58, test_59, 
};

// ----------------------------------------------------------------------------

int main(int argc, char *argv[]) {
  // If the executable is called with a valid test number as an argument, then
  // get and run only that test. Otherwise, run everything.
  if (argc > 1) {
    int test_num = atoi(argv[1]);
    if (test_num >= 0 && test_num < NUMTESTS) {
      void (*test_case)() = TESTS[test_num];
      test_case();  // Will exit if it fails
      return 0; // If we reach here, test case passed.
    } else {
      fprintf(stderr, "Test number is invalid. Running all...\n");
    }
  }
  // Run all the tests...
  for (int test_num = 0; test_num < NUMTESTS; test_num++) {
    void (*test_case)() = TESTS[test_num];
    test_case();    // Will exit if it fails
  }

  return 0;   // If we reach here, all test cases passed.
}
