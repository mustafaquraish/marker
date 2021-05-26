#include "functions.c"

#define MARKER_DEFAULT_MAIN
#include "marker.h"

// This will be run in a forked process
TEST_FORK(test_square) {
  if (square(5) != 25) {
    TEST_FAIL("square() test failed on %d\n", 5);
  }
}

// Test only passes if it finishes running. Code cannot
// fake a "pass" by doing exit(0) here:
TEST_FORK(test_exit_0) {
  exit(0);
}

// The following tests run on the same process...
//  (useful when you need to run something through valgrind / etc)
TEST(test_sum_of_squares) {
  if (sum_of_squares(3) != 14) {
    TEST_FAIL("sum_of_squares() test failed on %d\n", 3);
  }
}

// This test will timeout and fail...
TEST(test_sleep_10_sec) {
  sleep_10_sec();
}

// Expecting exit code 7
TEST(test_exit_with_7) {
  exit_with_7();
}